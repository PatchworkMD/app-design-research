"""Build the skills-only submission archive using an explicit file allowlist."""
from pathlib import Path
import hashlib
import zipfile

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins" / "app-design-research"
files = [(plugin / ".codex-plugin/plugin.json", ".codex-plugin/plugin.json"),
         (plugin / "skills/app-design-review/SKILL.md", "skills/app-design-review/SKILL.md"),
         (plugin / "assets/icon.svg", "assets/icon.svg")]
files += [(root / name, name) for name in ("LICENSE", "PRIVACY.md", "TERMS.md", "SOURCES.md")]
out = root / "dist"
out.mkdir(exist_ok=True)
archive = out / "app-design-research-skills-v0.1.0.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for source, name in files:
        item = zipfile.ZipInfo(name, date_time=(2026, 9, 6, 0, 0, 0))
        item.compress_type = zipfile.ZIP_DEFLATED
        item.external_attr = 0o644 << 16
        z.writestr(item, source.read_bytes())
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(out / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n")
print(f"Built {archive.name}: {len(files)} files; sha256={digest}")
