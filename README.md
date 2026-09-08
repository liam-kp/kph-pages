
## Setup (required on every fresh clone)

```bash
./scripts/bootstrap.sh
```

Points git at `.githooks/`, activating the PII guard (`scripts/check_pii.sh`). This branch is
**public** and GitHub Pages serves from it, so a commit here publishes to the open web. The guard
blocks any staged file containing a phone number or WhatsApp lid. If it blocks a file, move the file
out of the repo — never weaken the check.
