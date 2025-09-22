---
name: Bug report
about: Create a report to help us improve the FastAPI base project
title: "[BUG] "
labels: bug
assignees: ""
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

Steps to reproduce the behavior:

1. Set up environment with '...'
2. Run command '....'
3. Access endpoint '....'
4. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

What actually happened instead.

## Environment Information

**Docker Environment:**

- Docker version: [e.g. 20.10.7]
- Docker Compose version: [e.g. 1.29.2]
- OS: [e.g. Ubuntu 20.04, Windows 10, macOS Big Sur]

**Local Development (if applicable):**

- Python version: [e.g. 3.13.0]
- uv version: [e.g. 0.4.0]
- OS: [e.g. Ubuntu 20.04, Windows 10, macOS Big Sur]

**API/Application:**

- FastAPI version: [from pyproject.toml]
- Database: PostgreSQL [version if known]
- Redis: [version if known]

## Error Logs

If applicable, add error logs or stack traces:

```
Paste error logs here
```

## Screenshots

If applicable, add screenshots to help explain your problem.

## Additional Context

- Is this a regression (worked in a previous version)?
- Any recent changes to configuration?
- Any workarounds you've found?

## Configuration

**Environment Variables (remove sensitive data):**

```
DEBUG=True
ENV=dev
# Add other relevant env vars
```

**Docker Compose services running:**

- [ ] fastapi-base
- [ ] db (PostgreSQL)
- [ ] redis
- [ ] celery
- [ ] beat
