"""Portable App Design Research adapter with browser access disabled."""

from __future__ import annotations

import json
import hashlib
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

HOST = "appllama.io"
ROOT = "https://appllama.io"
MAX_SNAPSHOT_CHARS = 12_000
MAX_ACCESSIBLE_LINKS = 10
MAX_SEARCH_POLLS = 3
SEARCH_POLL_DELAY_SECONDS = 0.5
DEFAULT_IMAGE_LIMIT = 6
DEFAULT_CORPUS_LIMIT = 20
MAX_CORPUS_LIMIT = 100
MAX_CORPUS_FILE_BYTES = 16 * 1024 * 1024
IMAGE_HOSTS = {"appllama.io", "cloud.appllama.io"}
SKILLS = ["app-design-review"]
OPERATIONS = {
    "inspect_app": "/apps/",
    "browse_apps": "/",
    "browse_screens": "/screens",
    "browse_flows": "/flows",
    "browse_elements": "/elements",
    "search_apps": "/",
    "search_screens": "/screens",
    "search_flows": "/flows",
    "search_elements": "/elements",
    "inspect_reference": None,
    "offline_corpus": None,
    "capabilities": None,
}
SEARCH_CONTROLS = {
    "search_apps": "Search every app",
    "search_screens": "Search screens by name",
    "search_flows": "Search every flow",
    "search_elements": "Filter element families",
}
PUBLIC_REFERENCE_PREFIXES = ("/apps/", "/screens/", "/flows/", "/elements/")

TOOL_SCHEMA = {
    "name": "app_design_research",
    "description": "Query an explicitly supplied local AppLlama evidence corpus; website access stays disabled.",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {"type": "string", "enum": list(OPERATIONS)},
            "task": {"type": "string", "description": "Research task scope."},
            "query": {"type": "string", "description": "Research intent or browser search text."},
            "url": {"type": "string", "description": "Optional public AppLlama URL."},
            "corpus_path": {"type": "string", "description": "Absolute path to a supplied local evidence corpus."},
            "limit": {"type": "integer", "minimum": 1, "maximum": 100},
            "include_images": {
                "type": "boolean",
                "description": "Include accessible image metadata. Defaults true for inspect operations and false otherwise.",
            },
            "image_limit": {"type": "integer", "minimum": 1, "maximum": 6},
        },
        "required": ["operation", "task", "query"],
    },
}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _error(message: str, *, operation: str = "") -> str:
    return _json({"source_url": None, "operation": operation, "access": "invalid_request", "error": message,
                  "observed_snapshot_text": "", "accessible_links": [], "limitation_flags": ["input_rejected"],
                  "skills": SKILLS})


def validate_url(url: str, operation: str) -> tuple[bool, str]:
    if not isinstance(url, str) or len(url) > 2048 or any(ord(c) < 33 for c in url):
        return False, "Invalid URL."
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != HOST or parsed.port is not None:
            return False, "URL must use exact https://appllama.io host without credentials or port."
    except ValueError:
        return False, "Malformed URL."
    if parsed.query or parsed.fragment or "%" in parsed.path or "\\" in parsed.path:
        return False, "Encoded paths, queries, and fragments are not supported."
    path = parsed.path or "/"
    if any(part in (".", "..") for part in path.split("/")):
        return False, "Path traversal is not allowed."
    if operation in ("browse_apps", "search_apps"):
        allowed = path == "/"
    elif operation in ("browse_screens", "search_screens", "browse_flows", "search_flows",
                       "browse_elements", "search_elements"):
        prefix = OPERATIONS[operation]
        allowed = path == prefix or path.startswith(prefix + "/")
    elif operation == "inspect_app":
        allowed = path.startswith("/apps/") and len(path.split("/")) >= 4
    elif operation == "inspect_reference":
        allowed = any(path.startswith(prefix) and len(path) > len(prefix) for prefix in PUBLIC_REFERENCE_PREFIXES)
    else:
        allowed = path == "/"
    if not allowed:
        return False, "URL is outside this operation's public page paths."
    return True, url


def _target(args: dict[str, Any], operation: str) -> tuple[bool, str]:
    supplied = args.get("url")
    if supplied is not None:
        if not isinstance(supplied, str) or not supplied:
            return False, "url must be a non-empty string."
        return validate_url(supplied, operation)
    if operation in ("inspect_app", "inspect_reference"):
        return False, operation + " requires a source URL."
    path = OPERATIONS.get(operation)
    return True, ROOT + (path if path is not None else "/")


def _decode_result(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (ValueError, TypeError):
            raise ValueError("Browser returned malformed JSON.") from None
    if not isinstance(raw, dict):
        raise ValueError("Browser returned a non-object result.")
    return raw


def _access_error(message: str) -> str:
    lowered = message.casefold()
    if any(x in lowered for x in ("unauthorized", "sign in", "login", "authentication", "401")):
        return "auth_required"
    if any(x in lowered for x in ("paywall", "subscription required", "upgrade required")):
        return "paywall"
    if any(x in lowered for x in ("cannot connect", "connection refused", "unavailable", "not found", "404")):
        return "unavailable"
    return "browser_error"


def _result(operation: str, source: str | None, access: str, *, error: str | None = None,
            text: str = "", links: list[dict[str, str]] | None = None, flags: list[str] | None = None,
            truncated: bool = False) -> str:
    result = {"operation": operation, "source_url": source, "access": access,
              "observed_snapshot_text": text, "accessible_links": links or [],
              "limitation_flags": flags or [], "snapshot_truncated": truncated, "skills": SKILLS}
    if error:
        result["error"] = error[:1000]
    return _json(result)


def _snapshot_text(result: dict[str, Any]) -> str:
    text = result.get("snapshot")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("No readable browser snapshot.")
    return text


def _search_ref(snapshot: str, label: str) -> str | None:
    match = re.search(rf'^\s*- textbox "{re.escape(label)}" \[(e\d+)\]:', snapshot, re.MULTILINE)
    return match.group(1) if match else None


def _control_contains_query(snapshot: str, label: str, query: str) -> bool:
    lines = snapshot.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.match(rf'^(\s*)- textbox "{re.escape(label)}" \[e\d+\]:', line)), None)
    if start is None:
        return False
    indent = len(lines[start]) - len(lines[start].lstrip())
    node = [lines[start]]
    for line in lines[start + 1:]:
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        node.append(line)
    expected = query.strip().casefold()
    for line in node:
        match = re.match(r'^\s*- text:\s*(.*)$', line)
        if match and match.group(1).strip().casefold() == expected:
            return True
        match = re.match(r'^\s*(?:value|/value):\s*(.*)$', line)
        if match and match.group(1).strip().casefold() == expected:
            return True
    return False


def _search_busy(snapshot: str) -> bool:
    return any(re.search(pattern, snapshot, re.IGNORECASE | re.MULTILINE) for pattern in (
        r'^\s*- progressbar\b',
        r'^\s*- status(?:\s+"[^"]*loading[^"]*"|:\s*loading)',
        r'^\s*- text:\s*(?:loading|searching)(?:\.{0,3})?\s*$',
        r'^\s*(?:aria-busy|busy):\s*true\s*$',
    ))


def _is_public_reference_url(candidate: str) -> tuple[bool, str]:
    if candidate.startswith("/") and not candidate.startswith("//"):
        if any(part in (".", "..") for part in candidate.split("/")):
            return False, ""
        absolute = urljoin(ROOT, candidate)
    elif candidate.startswith(ROOT + "/"):
        absolute = candidate
    else:
        return False, ""
    valid, _ = validate_url(absolute, "inspect_reference")
    return valid, absolute if valid else ""


def _accessible_links(snapshot: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[str] = set()
    lines = snapshot.splitlines()
    for index, line in enumerate(lines):
        match = re.match(
            r'^(\s*)- (?:link "([^"]+)"(?: \[e\d+\])?:?|\'link "([^"]+)"(?: \[e\d+\])?\':)\s*$',
            line,
        )
        if not match:
            continue
        indent = len(match.group(1))
        label = (match.group(2) or match.group(3)).strip()
        candidate = None
        for child in lines[index + 1:]:
            if not child.strip():
                continue
            if len(child) - len(child.lstrip()) <= indent:
                break
            url_match = re.match(r'^\s*-?\s*/url:\s*(\S+)\s*$', child)
            if url_match:
                candidate = url_match.group(1)
            break
        if not candidate or not label:
            continue
        valid, absolute = _is_public_reference_url(candidate)
        if not valid or absolute in seen:
            continue
        lowered_label = label.casefold()
        if any(term in lowered_label for term in ("locked screen", "blurred")):
            continue
        seen.add(absolute)
        links.append({"label": label, "url": absolute})
        if len(links) == MAX_ACCESSIBLE_LINKS:
            break
    return links


def _is_truncated(snapshot: str) -> bool:
    return len(snapshot) > MAX_SNAPSHOT_CHARS or bool(re.search(r'\[\.\.\. \d+ more lines truncated\b', snapshot))


def _image_options(args: dict[str, Any], operation: str) -> tuple[bool, bool, int | str]:
    supplied = args.get("include_images")
    if supplied is not None and not isinstance(supplied, bool):
        return False, False, "include_images must be a boolean."
    include = supplied if supplied is not None else operation in ("inspect_app", "inspect_reference")
    limit = args.get("image_limit", DEFAULT_IMAGE_LIMIT)
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 6:
        return False, include, "image_limit must be an integer from 1 to 6."
    return True, include, limit


def _visible_image_alts(snapshot: str) -> set[str]:
    return {match.group(1) for match in re.finditer(r'^\s*- img "([^"]+)"', snapshot, re.MULTILINE)
            if match.group(1)}


def _valid_image_src(src: Any) -> bool:
    if not isinstance(src, str) or not src or len(src) > 8192 or any(ord(char) < 33 for char in src):
        return False
    try:
        parsed = urlsplit(src)
        return (parsed.scheme == "https" and parsed.hostname in IMAGE_HOSTS and parsed.netloc == parsed.hostname
                and parsed.username is None and parsed.password is None and parsed.port is None and bool(parsed.path))
    except ValueError:
        return False


def _image_evidence(raw: Any, snapshot: str, source_page: str, limit: int) -> tuple[str, list[dict[str, Any]], list[str], str | None]:
    try:
        payload = _decode_result(raw)
    except ValueError as exc:
        return "malformed", [], ["images_response_malformed"], str(exc)
    if payload.get("success") is not True or payload.get("error"):
        message = str(payload.get("error") or "Image extraction did not report success.")
        return "unavailable", [], ["images_unavailable"], message
    raw_images = payload.get("images")
    if not isinstance(raw_images, list):
        return "malformed", [], ["images_response_malformed"], "Browser image response has no images list."

    flags: list[str] = []
    if payload.get("truncated") is True or payload.get("has_more_unknown") is True:
        flags.append("native_images_truncated")
    visible_alts = _visible_image_alts(snapshot)
    eligible: list[dict[str, Any]] = []
    seen: set[str] = set()
    for image in raw_images:
        if not isinstance(image, dict):
            continue
        src, alt = image.get("src"), image.get("alt")
        width, height = image.get("width"), image.get("height")
        if (not isinstance(alt, str) or not alt or alt not in visible_alts or not _valid_image_src(src)
                or isinstance(width, bool) or not isinstance(width, int) or width < 0
                or isinstance(height, bool) or not isinstance(height, int) or height < 0):
            continue
        lowered = alt.casefold()
        if "locked" in lowered or "blurred" in lowered or "appllama" in lowered:
            continue
        if src in seen:
            continue
        seen.add(src)
        eligible.append({"src": src, "alt": alt, "width": width, "height": height, "source_page": source_page})
    if len(eligible) > limit:
        flags.append("image_limit_applied")
    images = eligible[:limit]
    return ("observed" if images else "empty"), images, flags, None


def _capabilities() -> str:
    return _json({"operation": "capabilities", "access": "disabled", "skills": SKILLS,
                  "implemented": [], "companion_skill": "app-design-review",
                  "disabled_operations": list(OPERATIONS),
                  "network_operations": "disabled_before_dispatch",
                  "not_implemented": ["browser_page_inspection", "browser_search_input",
                                       "accessible_public_reference_links", "accessible_image_metadata",
                                       "server_search", "semantic_search", "paid_vision"],
                  "paid_mcp": False, "full_parity": False})


def _corpus_error(message: str) -> str:
    return _error(message, operation="offline_corpus")


def _safe_corpus_root(value: Any) -> tuple[Path | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, "corpus_path must be a non-empty absolute path."
    raw = value.strip()
    candidate = Path(raw)
    if not candidate.is_absolute() or ".." in candidate.parts:
        return None, "corpus_path must be absolute and contain no path traversal."
    try:
        root = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        return None, "corpus_path does not resolve to a readable directory."
    if not root.is_dir() or root.is_symlink():
        return None, "corpus_path must resolve to a directory without symlinks."
    current = candidate
    while current != current.parent:
        if current.is_symlink():
            return None, "corpus_path cannot contain symlinked directories."
        current = current.parent
    return root, None


def _read_corpus_json(root: Path, name: str) -> tuple[Any, dict[str, Any], str | None]:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        return None, {}, f"Corpus file path is invalid: {name}."
    path = root / relative
    if path.is_symlink() or not path.is_file():
        return None, {}, f"Corpus is missing required file: {name}."
    try:
        if path.stat().st_size > MAX_CORPUS_FILE_BYTES:
            return None, {}, f"Corpus file is too large: {name}."
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeDecodeError, ValueError):
        return None, {}, f"Corpus file is not readable JSON: {name}."
    if not isinstance(value, dict):
        return None, {}, f"Corpus file must contain a JSON object: {name}."
    return value, {"path": name, "sha256": hashlib.sha256(raw).hexdigest(), "byte_count": len(raw)}, None


def _observed_revenue(text: str) -> dict[str, str]:
    match = re.search(r"\$(?:\d+(?:\.\d+)?)(?:[KMB])?/mo\b", text)
    if not match:
        return {"status": "unavailable", "reason": "No explicit revenue amount exists in the supplied catalog text."}
    return {"status": "observed", "label": match.group(0), "basis": "observed app card text"}


def _catalog_corpus(root: Path, catalog: dict[str, Any], catalog_file: dict[str, Any],
                    manifest: dict[str, Any] | None, manifest_file: dict[str, Any] | None,
                    args: dict[str, Any], limit: int) -> str:
    raw_apps = catalog.get("apps")
    if not isinstance(raw_apps, dict) or not isinstance(catalog.get("complete"), bool):
        return _corpus_error("The browser catalog has an unsupported schema.")
    query = args["query"].strip().casefold()
    apps: list[dict[str, Any]] = []
    for path, item in raw_apps.items():
        if not _valid_observed_app_path(path) or not isinstance(item, dict):
            return _corpus_error("The browser catalog contains an invalid app record.")
        url = item.get("url", ROOT + path)
        text = item.get("text", "")
        if not isinstance(url, str) or not isinstance(text, str):
            return _corpus_error("The browser catalog contains an invalid app record.")
        if query not in " ".join((path, url, text)).casefold():
            continue
        revenue = _observed_revenue(text)
        apps.append({"path": path, "source_url": url, "text": text[:MAX_SNAPSHOT_CHARS],
                     "analytics": {"revenue": revenue}})
        if len(apps) >= limit:
            break
    assets: list[dict[str, Any]] = []
    if manifest is not None:
        raw_assets = manifest.get("assets")
        if not isinstance(raw_assets, list):
            return _corpus_error("assets-manifest.json has an unsupported schema.")
        for item in raw_assets:
            if not isinstance(item, dict):
                return _corpus_error("assets-manifest.json contains a non-object asset.")
            searchable = " ".join(str(item.get(key, "")) for key in ("asset_id", "kind", "name", "page", "path", "url"))
            if query not in searchable.casefold():
                continue
            assets.append({key: item[key] for key in (
                "asset_id", "kind", "name", "page", "path", "url", "source", "source_path", "status", "sha256", "byte_count"
            ) if key in item})
            if len(assets) >= limit:
                break
    observed_revenue = next((a["analytics"]["revenue"] for a in apps
                             if a["analytics"]["revenue"]["status"] == "observed"),
                            {"status": "unavailable", "reason": "No explicit revenue amount exists in the supplied catalog text."})
    coverage = {"asset_observations": len(manifest.get("assets", [])) if manifest else 0,
                "asset_files": len({x.get("sha256") for x in manifest.get("assets", [])
                                     if isinstance(x, dict) and x.get("sha256")}) if manifest else 0,
                "app_paths_observed": len(raw_apps), "catalog_complete": catalog["complete"],
                "catalog_records_complete": catalog["complete"], "details_complete": False,
                "detail_complete": False, "query_limit": limit}
    files = [catalog_file]
    if manifest_file:
        files.insert(0, manifest_file)
    flags = ["network_access_disabled", "offline_corpus_only", "details_incomplete"]
    if observed_revenue["status"] != "observed":
        flags.append("revenue_unavailable")
    return _json({"operation": "offline_corpus", "access": "offline", "source_url": ROOT + "/",
                  "query": args["query"].strip(), "assets": assets, "apps": apps,
                  "analytics": {"revenue": observed_revenue},
                  "catalog_complete": catalog["complete"], "details_complete": False,
                  "provenance": {"corpus_path": str(root), "files": files, "source": "browser-catalog"},
                  "coverage": coverage, "limitation_flags": flags, "skills": SKILLS})


def _valid_observed_app_path(path: Any) -> bool:
    if not isinstance(path, str) or not path.startswith("/apps/") or any(part in (".", "..") for part in path.split("/")):
        return False
    valid, _ = validate_url(ROOT + path, "inspect_app")
    return valid


def _offline_corpus(args: dict[str, Any]) -> str:
    root, error = _safe_corpus_root(args.get("corpus_path"))
    if error:
        return _corpus_error(error)
    limit = args.get("limit", DEFAULT_CORPUS_LIMIT)
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_CORPUS_LIMIT:
        return _corpus_error(f"limit must be an integer from 1 to {MAX_CORPUS_LIMIT}.")
    catalog_path = root / "downloads" / "appllama-browser-catalog-complete.json"
    if catalog_path.is_file() and not catalog_path.is_symlink():
        catalog, catalog_file, error = _read_corpus_json(root, "downloads/appllama-browser-catalog-complete.json")
        if error:
            return _corpus_error(error)
        manifest = manifest_file = None
        if (root / "assets-manifest.json").exists():
            manifest, manifest_file, error = _read_corpus_json(root, "assets-manifest.json")
            if error:
                return _corpus_error(error)
        return _catalog_corpus(root, catalog, catalog_file, manifest, manifest_file, args, limit)
    manifest, manifest_file, error = _read_corpus_json(root, "assets-manifest.json")
    if error:
        return _corpus_error(error)
    observed, observed_file, error = _read_corpus_json(root, "appllama-apps-observed-20260915.json")
    if error:
        return _corpus_error(error)
    if not isinstance(manifest.get("assets"), list) or not isinstance(manifest.get("schema_version"), int):
        return _corpus_error("assets-manifest.json has an unsupported schema.")
    if not isinstance(observed.get("source"), str) or not isinstance(observed.get("appPaths"), list):
        return _corpus_error("The observed apps JSON has an unsupported schema.")
    if not isinstance(observed.get("complete"), bool):
        return _corpus_error("The observed apps JSON must declare complete as a boolean.")
    app_paths = observed["appPaths"]
    if any(not _valid_observed_app_path(path) for path in app_paths):
        return _corpus_error("The observed apps JSON contains an invalid app path.")
    observed_count = observed.get("observedApps")
    if not isinstance(observed_count, (int, list)) or isinstance(observed_count, bool):
        return _corpus_error("The observed apps JSON has an invalid observedApps value.")
    if isinstance(observed_count, int) and observed_count != len(app_paths):
        return _corpus_error("observedApps does not match appPaths coverage.")
    query = args["query"].strip().casefold()
    assets = []
    for item in manifest["assets"]:
        if not isinstance(item, dict):
            return _corpus_error("assets-manifest.json contains a non-object asset.")
        searchable = " ".join(str(item.get(key, "")) for key in ("asset_id", "kind", "name", "page", "path", "url"))
        if query not in searchable.casefold():
            continue
        assets.append({key: item[key] for key in (
            "asset_id", "kind", "name", "page", "path", "url", "source", "source_path", "status", "sha256", "byte_count"
        ) if key in item})
        if len(assets) >= limit:
            break
    apps = []
    for path in app_paths:
        if query not in path.casefold():
            continue
        apps.append({"path": path, "source_url": observed["source"], "analytics": {"revenue": {
            "status": "unavailable", "reason": "No revenue field exists in the supplied observed apps JSON."
        }}})
        if len(apps) >= limit:
            break
    coverage = {
        "asset_observations": len(manifest["assets"]),
        "asset_files": len({item.get("sha256") for item in manifest["assets"] if isinstance(item, dict) and item.get("sha256")}),
        "app_paths_observed": len(app_paths),
        "apps_complete": observed["complete"],
        "query_limit": limit,
    }
    return _json({
        "operation": "offline_corpus", "access": "offline", "source_url": observed["source"],
        "query": args["query"].strip(), "assets": assets, "apps": apps,
        "analytics": {"revenue": {"status": "unavailable", "reason": "The supplied packet has no revenue observations."}},
        "provenance": {"corpus_path": str(root), "files": [manifest_file, observed_file], "source": observed["source"]},
        "coverage": coverage, "limitation_flags": ["network_access_disabled", "offline_corpus_only", "revenue_unavailable"],
        "skills": SKILLS,
    })


def app_design_research(args: dict, **kwargs) -> str:
    if not isinstance(args, dict):
        return _error("Arguments must be an object.")
    operation = args.get("operation")
    if not isinstance(operation, str) or operation not in OPERATIONS:
        return _error("Unknown operation.")
    for key in ("task", "query"):
        value = args.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > 2000:
            return _error(key + " must contain 1 to 2000 characters.", operation=operation)
    image_options_valid, include_images, image_limit = _image_options(args, operation)
    if not image_options_valid:
        return _error(str(image_limit), operation=operation)
    ok, target = _target(args, operation)
    if not ok:
        return _error(target, operation=operation)
    if operation == "capabilities":
        return _capabilities()
    if operation == "offline_corpus":
        return _offline_corpus(args)
    # Public release policy: browser and all network dispatch stay unreachable.
    return _result(operation, target, "disabled",
                   error="Public AppLlama access is disabled; written permission is required.",
                   flags=["network_access_disabled", "written_permission_required"])
