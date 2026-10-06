<img src="plugins/app-design-research/assets/icon.png" width="72" height="72" alt="Hugging App logo">

# Hugging App

Review supplied app references and turn observed problems into testable changes.

Give your agent a screenshot, interface text, or app code. Get focused design
improvements tied to the evidence, with a practical way to check each change.

[Public Apple catalog](https://catalog.patchworkmd.dev/) ·
[Install v0.1.5](https://github.com/PatchworkMD/app-design-research/releases/tag/v0.1.5) ·
[Report an issue](https://github.com/PatchworkMD/app-design-research/issues)

## What you get

- Up to three prioritized improvements with supporting evidence and validation steps.
- Reviews of supplied screenshots, interface text, or source code.
- A clear record of what was inspected and what remains unverified.
- Reference attribution when supplied, and reusable receipts for unchanged inputs.
- iPhone-focused guidance for original SwiftUI/UIKit screens, WidgetKit widgets,
  and ActivityKit Live Activities, with exact-device runtime checks.

Version 0.1.5 records each input's provenance, freshness, and origin, plus image
dimensions when inspected. Reviews distinguish current evidence from historical
or synthetic examples. Document text is treated as data, not instructions.

The plugin proposes changes; your agent implements them only when you request it.
It does not fetch websites or use paid tools. Your host processes the material you
supply, under its own training and retention policies. Use redacted or synthetic
inputs when appropriate.

The iOS workflow covers iOS targets on iPhone only. It excludes iPadOS, watchOS,
visionOS, and macOS. Supplied Appllama research is treated as evidence;
the documented MCP contract is local reference material, not a live integration.

The archived AppLlama adapter remains in this package for compatibility, but
its public operation is hard disabled before any browser or network dispatch.
Website operations return `access: "disabled"`; invalid requests are rejected.
The `offline_corpus` operation searches an explicitly supplied local archive,
returns bounded matches and observed revenue labels, and reports catalog and
detail coverage separately. It performs no network requests.
Written permission is required to change that policy.

## Install in Codex

```sh
codex plugin marketplace add PatchworkMD/app-design-research --ref v0.1.5
codex plugin add app-design-research@app-design-research-public
```

Start a new task after installation. The portable plugin is in
`plugins/app-design-research`; the disabled native Hermes compatibility source
is in `hermes/app-design-research`. The skill can also be loaded by a compatible
agent that supports SKILL.md. Neither package starts a server.

## Your first review

1. Install the plugin and start a new task.
2. Attach a screenshot you can share, paste interface text, or supply relevant code.
3. Explain what the user is trying to do and ask:

   > Use Hugging App to review this screen. Suggest three improvements.
   > Cite the evidence for each and tell me how to test it. Mark unseen states
   > as unverified.

4. Review the proposals. Ask your coding agent to implement the changes you want.

For useful results, include loading, empty, error, and success states when available.
A text or code review is useful even without screenshots.

## Example: a draft confirmation screen

A fresh agent trial of the v0.1.1 candidate used this synthetic text input:

> A confirmation screen has Yes and No buttons. Yes copies a draft to the
> clipboard. It displays “Copied!” before the write finishes and clears the
> draft if copying fails. It says “Nothing leaves your phone until you say yes.”

The review identified three improvements:

- Show success after the clipboard write succeeds, and test rejected writes.
- Preserve the draft on failure so the user can retry.
- Check the actual data flow before making the privacy promise.

This is a condensed text-only trial result, not a screenshot or live app test.
The agent explicitly left visual, accessibility, and runtime behavior unverified.
This trial does not establish live app behavior or directory approval.

## FAQ

**Does it search the public Apple catalog or AppLlama?**

It reviews material you supply. The public Apple catalog is a companion reference
for supplied material. It can search an explicitly supplied local archive with
`offline_corpus`. Live website access remains disabled.

**Does it change my app automatically?**

No. It proposes changes. Implementation requires your request to your agent.

**Do I need an API key or a server?**

The plugin needs neither. It runs inside your agent host, so that host's
account, model access, and usage terms apply.

**Can it certify accessibility or verify my entire app?**

No. Screenshots support visible observations; source supports code review.
Keyboard behavior, screen-reader use, and live interactions need their own tests.

**Is everything processed locally?**

The plugin does not fetch websites, but your agent host processes supplied content.
Its settings and policies govern processing and retention. Use synthetic or redacted
material where appropriate. See [Privacy](PRIVACY.md).

**Is it in the ChatGPT directory?**

The ChatGPT directory has a published Hugging App listing. The latest release status is recorded in SUBMISSION.md.

**Where do I report a problem?**

Primary product/support contact: [hello@patchworkmd.dev](mailto:hello@patchworkmd.dev).
Email delivery is still being tested; use GitHub issues for a trackable report.
Do not email credentials or sensitive review material.
Open a [GitHub issue](https://github.com/PatchworkMD/app-design-research/issues)
with a minimal example you are entitled to share. Omit secrets and private data.

## Development checks

```sh
python3 -m unittest discover -s hermes/app-design-research -p 'test_*.py' -v
```

The behavior tests check disabled dispatch and rejected input. They do not prove
model-generated reviews, legal clearance, or OpenAI directory approval.

See [Privacy](PRIVACY.md), [Terms and data acknowledgements](TERMS.md),
[Sources](SOURCES.md), and [directory submission status](SUBMISSION.md).
