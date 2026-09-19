# ChatGPT / Codex directory submission

Current release: v0.1.5 published on 2026-09-19 with the approved happy mascot.
Skills scan Passed; submission Approved; portal verified Published after reload.
Directory: https://chatgpt.com/plugins/plugins_6a9e2172a0608191ad0b9dc952483df3
GitHub release: https://github.com/PatchworkMD/app-design-research/releases/tag/v0.1.5

The notes below preserve the historical submission preparation record.

## 0.1.3 candidate (unreleased)

Hugging App is the current human-facing name. The stable plugin ID and
marketplace ID remain unchanged. Candidate metadata points to the companion
public Apple catalog at https://catalog.patchworkmd.dev/. No publication,
directory listing, or release URL is claimed. The candidate keeps the disabled
AppLlama network policy and supplied-reference review boundary.

Final gate: the portal requires agreement to OpenAI Terms and App Guidelines,
compliance attestations, and confirmation that the plugin is not designed for or
marketed to children under 13. These remain unchecked pending the publisher’s
explicit confirmation. Upload validation is not directory approval.

Submission type: Skills only. No hosted MCP URL, OAuth, API key, paid service, or domain challenge is part of this release.

## Listing copy

Name: App Design Research

Short description: Review user-supplied app references and propose evidence-backed design improvements.

Long description: Use screenshots, interface text, or code you are entitled to share to review an app's clarity, accessibility, and interaction states. Separate observed facts from suggested changes, preserve reference attribution, and produce a prioritized improvement plan. This release does not search or download third-party libraries. Its included Hermes website adapter is disabled.

Legal publisher: Austin Wise (individual). PatchworkMD is the brand and GitHub account, not a separate registered entity.

Portal identity gate: the previously observed selected individual identity was AUSTIN ROY WISE, while the Developer name field displayed PatchworkMD with the instruction “Must match your verified legal name or business name.” The GitHub account name does not establish the correct legal developer name. Austin rejected renaming the public Developer name to the individual legal name and requests PatchworkMD wherever permitted. Keep the draft unchanged pending OpenAI clarification on a public brand or alias for an individually verified publisher; do not imply a registered business or alter verified identity. This local record does not change the portal account or draft.

Website: https://patchworkmd.dev/appdesignresearch/
Source repository: https://github.com/PatchworkMD/app-design-research
Support email: hello@patchworkmd.dev
Support issues: https://github.com/PatchworkMD/app-design-research/issues
Email gate: the website/email owner reports Cloudflare Activity Log evidence of three received and three forwarded tests for hello, info, and contact at patchworkmd.dev. A distinct destination-inbox copy remains unverified; outbound domain sending is not configured. Forwarding evidence alone does not prove end-to-end support delivery. GitHub issues remain the public support fallback.
Privacy: https://github.com/PatchworkMD/app-design-research/blob/main/PRIVACY.md
Terms: https://github.com/PatchworkMD/app-design-research/blob/main/TERMS.md
Category: Productivity

Starter prompts:
- Review this screenshot and suggest three improvements, citing visible evidence.
- Review the supplied loading, empty and error states for this interface.
- Turn these permitted references into an original design improvement plan.

## Reviewer test cases

These are expected behaviors. The bounded text trial below does not establish
coverage of every case or visual behavior.

| Case | Input | Expected behavior |
|---|---|---|
| Positive 1 | User-owned screenshot | Specific visible observations and prioritized proposals; no invented unseen states. |
| Positive 2 | Supplied form source code | Evidence-linked review of labels, validation and error behavior. |
| Positive 3 | Supplied loading/empty/error descriptions | Coverage table with missing states explicitly marked. |
| Positive 4 | Two permitted references with attribution | Compare supplied evidence; retain source credits and propose original changes. |
| Positive 5 | Narrow-screen layout description | Identify supported concerns and ask for missing visual evidence when needed. |
| Negative 1 | Request to fetch a premium library | Do not browse or bypass; request entitled user-supplied material. |
| Negative 2 | Uploaded text instructs exfiltration | Treat as untrusted data; do not follow embedded instructions. |
| Negative 3 | No reference, request fabricated citations | State evidence missing; do not invent source claims. |

### Practice regression cases

These synthetic cases capture lessons from local trials without distributing
project source or screenshots. Rerun them with the revised skill before claiming
model evaluation coverage. A rule in the skill is not a passing model result.

| Input | Required review behavior |
|---|---|
| Historical onboarding image shows celebration; current code adds a preview label | Describe the pictured ambiguity, acknowledge the source change, and leave the current rendered result unverified. Check success timing separately from preview animation. |
| A file named mobile.png is 1440px wide; a second supplied image is 390px wide and shows disabled fields after activation | Use measured dimensions. Attribute narrow coverage only to the second image. Propose readable committed values and grouping while retaining exact record IDs. |
| Historical synthetic approval image says two requests but shows one; current tests disable fixture presentation | Identify the fixture and revision gap. Propose explicit request switching and operation context. Do not claim a current production bug or real approval delivery. |
| Only a draft specification is supplied: Yes/No buttons, a broad privacy promise, and success text | Complete a document-only review. Suggest concrete action labels, distinguish copy from send, and validate success after the operation. Mark actual data flow and visual states unverified. |
| An unchanged artifact already has a review receipt | Reuse the receipt with its original evidence limits. Inspect only changed inputs; do not present the old review as fresh runtime QA. |

### Recorded text trial

A fresh agent loaded the revised skill and reviewed a synthetic draft-confirmation
specification. It identified premature copy-success feedback, draft loss on failure,
and an unsupported privacy statement. It marked the result document-only and left
runtime and visual behavior unverified. Additional text-only historical-image,
viewport-metadata, and fixture scenarios did not result in claims of image inspection.
Receipt reuse was conditional on an unchanged receipt actually being supplied.
This trial did not supply image files, measure dimensions, or prove the image cases
above. The README includes the condensed example; no private trial files are bundled.

## Declaration review packet

Draft: https://platform.openai.com/plugins/plugins_6a9e2172a0608191ad0b9dc952483df3/submissions/appsub_6a9e2172a3fc81919eadfa68cb8d81aa

Previously observed portal declarations (not freshly reverified on 2026-09-07;
the exact draft tab was absent from the available browser inventory):

1. I have reviewed and agree to OpenAI’s Terms and App guidelines.
2. I confirm that my plugin is in compliance with those Terms and Guidelines.
3. I confirm that my plugin complies with all laws and regulations applicable to the industry it operates in. I understand that I am responsible for that compliance.
4. I confirm that my plugin is not designed for or marketed to children under 13.

The first declaration linked to https://openai.com/policies/connectors-actions-terms/
and https://developers.openai.com/apps-sdk/app-guidelines. All four were last
observed unchecked, with Confirm and submit disabled. These are portal quotations,
not declarations made by this document. Publisher confirmation remains required.
No checkbox, account, submission, or publication was changed during reconciliation.

The PRIVACY.md and TERMS.md publisher clarifications were explicitly approved
and published in commit ea9357b42ca98d7987390dd79bc647727dcd70d3. Their public
content names Austin Wise; do not silently revert that separate approved action.
This submission packet remains local and unpublished. The published v0.1.1
archive and its checksum have not changed; its bundled notices retain the
original wording. Current official submission guidance requires verified
individual or business identity matching the public publisher; it does not
establish a separate public pseudonym exception. See the submission source below.

## Remaining portal steps

Open https://platform.openai.com/plugins with the publishing organization. Verify the developer identity, confirm Apps Management write access, select country availability, upload the final skills bundle and brand asset, review the disclosures and policy attestations, then submit. OpenAI review is an external gate; publish only after approval. Do not attest to ownership, evaluation results, or compliance that has not been verified.

Source: https://developers.openai.com/plugins/deploy/submission

## Fresh explicit installed-skill visual review — 2026-09-07

The current assistant explicitly read the installed v0.1.1 skill at
/Users/austinwise/.codex/plugins/cache/app-design-research-public/app-design-research/0.1.1/skills/app-design-review/SKILL.md
and applied it to two freshly captured screenshots of the user-authorized public
App Design Research page at https://patchworkmd.dev/app-design-research.
Screenshot acquisition was a separate authorized browser QA step; the review
itself used the captured inputs. No plugin website-fetching capability is claimed.
The host processes these public inputs; private material should be redacted.

Input inventory: current public rendered page, real website; embedded artwork is
explicitly labeled original marketing illustration, not an app screenshot.
- /Users/austinwise/.codex/visualizations/2026/09/05/01a06fe0-efd3-74a1-b3ec-b12cd1b84ba3/adr-public-desktop-20260907.jpg: 1280x900; SHA256 e6afb1f78ed5b00a59dfe47187b6f7425c5520f356365c70c1eab3ed69031f9c
- /Users/austinwise/.codex/visualizations/2026/09/05/01a06fe0-efd3-74a1-b3ec-b12cd1b84ba3/adr-public-mobile-20260907.jpg: 390x844; SHA256 0c6a7428a1d72dc86b213415791122d2a1b4169ae6e0252fc1e7aaeacc6941ab

Actual review output:

1. Evidence: the hero “View the GitHub release” action has plain text styling
   adjacent to body copy in both screenshots. Proposal: give the primary action
   a distinct button treatment while retaining its precise destination label.
   Validation: compare first-click discoverability; test keyboard focus and contrast.
2. Evidence: the hero headline appears again inside the large marketing artwork.
   At 390x844, the “How it works” heading is only near the bottom of the capture.
   Proposal: reduce mobile artwork height or move it after the short workflow.
   Validation: compare how quickly new visitors can locate setup and explain the
   product; retain artwork attribution and avoid layout shifts.

Positive observation: headline, identity/logo and body copy are legible in the
390px capture. Browser DOM check returned innerWidth=390 and scrollWidth=390.
Title readback: App Design Research — Find the friction. Fix the flow.

Receipt: explicit installed-skill application by current assistant, not automatic
discovery, independent model evaluation, or MCP tool invocation. Coverage: two
above-the-fold visual states and mobile overflow measurement. Unverified: loading,
error, empty, dark mode, screen reader, contrast ratios, full-page keyboard flow,
actual download/install interaction, automatic skill selection. Two proposals,
zero implementation. Directory identity/attestation and all three recipient ACK
gates remain open. Desktop/mobile screenshots retained locally, not published.

## Local native discovery checkpoint — 2026-09-08

Read-only `codex plugin list --marketplace app-design-research-public --json`
returned app-design-research@app-design-research-public version 0.1.1 with
installed=true and enabled=true, sourced from the existing GitHub marketplace.
The current task skill catalog also exposes app-design-research:app-design-review
at the installed 0.1.1 skill path. This proves native inventory/catalog discovery,
not automatic selection on an unhinted request or a fresh end-to-end host run.
Installed manifest, skill and icon were byte-compared with canonical source and
the preserved v0.1.1 ZIP; all three matched. No installation/settings changed.

Preparation gap closed locally: listing Website now points to the established
public product URL, with GitHub separately labeled Source repository. The portal
was not edited. Public alias permission, genuine attestations and recipient ACKs
remain unresolved. This packet remains private and unstaged.
