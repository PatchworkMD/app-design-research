# App Design Research

**Find the friction. Fix the flow.**

Give your agent a screenshot, interface text, or app code. Get focused design
improvements tied to the evidence, with a practical way to check each change.

This skills-only plugin reviews app design references that the user supplies.
The review uses screenshots, text, and source supplied in the request. It does
not fetch websites or use paid tools. It cites the user's provenance when given
and does not claim external sourcing when provenance is absent.

The reviewer treats document text as data, never as instructions. It reviews
evidence, then proposes prioritized improvements. It does not implement changes
without a user request. The host processes supplied data. Avoid sensitive
uploads. This package makes no guarantee about the host’s training or retention behavior.

The current local skill records an evidence inventory with artifact type,
provenance, dimensions where applicable, freshness (current, historical, or unknown),
and origin (synthetic, real, or unknown). Its receipt lists the loaded skill path and known version or revision,
inspected artifacts, coverage, unverified checks, proposed versus implemented
changes. It reuses a prior receipt
when inputs are unchanged. Version 0.1.1 records this evidence inventory and
receipt behavior.

The archived AppLlama adapter remains in this package for compatibility, but
its public operation is hard disabled before any browser or network dispatch.
Valid operations return `access: "disabled"`; invalid requests are rejected.
Written permission is required to change that policy.

## Install in Codex

```sh
codex plugin marketplace add PatchworkMD/app-design-research --ref v0.1.1
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

   > Use App Design Research to review this screen. Suggest three improvements.
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

**Does it search AppLlama or other design libraries?**
No. It reviews material you supply. The included website adapter is disabled.

**Does it change my app automatically?**
No. It proposes changes. Implementation requires your request to your agent.

**Do I need an API key or a server?**
The plugin itself needs neither. It runs inside a compatible agent host;
that host's account, model access, and usage terms still apply.

**Can it certify accessibility or verify my entire app?**
No. Screenshots support visible observations; source supports code review.
Keyboard behavior, screen-reader use, and live interactions need their own tests.

**Is everything processed locally?**
The plugin does not fetch websites, but your agent host processes supplied content.
Its settings and policies govern processing and retention. Use synthetic or redacted
material where appropriate. See [Privacy](PRIVACY.md).

**Is it in the ChatGPT directory?**
Not yet. The GitHub release is available; directory submission is still pending.

**Where do I report a problem?**

Primary product/support contact: [hello@patchworkmd.dev](mailto:hello@patchworkmd.dev).
Email delivery is still being tested; use GitHub issues for a trackable report.
Do not email credentials or sensitive review material.
Open a [GitHub issue](https://github.com/PatchworkMD/app-design-research/issues)
with a minimal example you are entitled to share. Omit secrets and private data.

## Verify

```sh
python3 -m unittest discover -s hermes/app-design-research -p 'test_*.py' -v
```

The behavior tests check disabled dispatch and rejected input. They do not prove
model-generated reviews, legal clearance, or OpenAI directory approval.

See [Privacy](PRIVACY.md), [Terms and data acknowledgements](TERMS.md),
[Sources](SOURCES.md), and [directory submission status](SUBMISSION.md).
