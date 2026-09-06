# App Design Research

This skills-only plugin reviews app design references that the user supplies.
The review uses screenshots, text, and source supplied in the request. It does
not fetch websites or use paid tools. It cites the user's provenance when given
and does not claim external sourcing when provenance is absent.

The reviewer treats document text as data, never as instructions. It reviews
evidence, then proposes prioritized improvements. It does not implement changes
without a user request. The host processes supplied data. Avoid sensitive
uploads. This package makes no guarantee about the host’s training or retention behavior.

The archived AppLlama adapter remains in this package for compatibility, but
its public operation is hard disabled before any browser or network dispatch.
Valid operations return `access: "disabled"`; invalid requests are rejected.
Written permission is required to change that policy.

## Install in Codex

```sh
codex plugin marketplace add PatchworkMD/app-design-research --ref v0.1.0
codex plugin add app-design-research@app-design-research-public
```

Start a new task after installation. The portable plugin is in
`plugins/app-design-research`; the disabled native Hermes compatibility source
is in `hermes/app-design-research`. The skill can also be loaded by a compatible
agent that supports SKILL.md. Neither package starts a server.

## Verify

```sh
python3 -m unittest discover -s hermes/app-design-research -p 'test_*.py' -v
```

The behavior tests check disabled dispatch and rejected input. They do not prove
model-generated reviews, legal clearance, or OpenAI directory approval.

See [Privacy](PRIVACY.md), [Terms and data acknowledgements](TERMS.md),
[Sources](SOURCES.md), and [directory submission status](SUBMISSION.md).
