# 0.1.6 candidate

- Replace the build-and-ship wording with the plugin's supplied-reference review workflow.
- Clarify evidence, validation steps, iPhone scope, and user-controlled implementation.
- Keep the approved Hugging App mascot as both the logo and composer icon.

# 0.1.5

- Approved happy phone-hugging mascot shared with the catalog.
- Build & Ship IOS Apps listing and native iPhone guidance.

# Changelog

## 0.1.3 candidate (unreleased)

- Rename the human-facing plugin to Hugging App while retaining the stable `app-design-research` plugin and marketplace IDs.
- Point the homepage to the companion public Apple catalog at https://catalog.patchworkmd.dev/.
- Clarify supplied-reference review and preserve the disabled AppLlama network policy.

## 0.1.2

- Add iPhone-only iOS implementation guidance: SwiftUI/UIKit, WidgetKit, ActivityKit, accessibility and per-change runtime checks.
- Add `references/ios-design.md` and `references/appllama-public-contract.md`, bundled by `build_bundle.py` and covered by a `--check` verification mode.
- Add `offline_corpus`: searches an explicitly supplied local archive only, returns bounded matches and observed-revenue labels, reports catalog/detail coverage separately, performs no network requests.
- Website dispatch stays hard disabled; no Appllama MCP calls, no paywall bypass, no live fetch.

## 0.1.1

- Distinguish historical, synthetic, source-only and visually inspected evidence.
- Return up to three findings with validation steps and reusable review receipts.
- Add setup instructions, FAQ and a synthetic text-review example.
- Include required directory icon references and versioned deterministic bundles.
- Keep network research disabled; the separate Hermes compatibility source remains unchanged.

## 0.1.0

- Initial supplied-reference design review plugin.
