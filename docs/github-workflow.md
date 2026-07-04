# GitHub Workflow

## Issue workflow

Use GitHub Issues as the main task tracker.

Suggested issue statuses in the Kanban board:

```text
Backlog → Ready → In Progress → Review → Done
```

## Branch naming

Use short and clear branch names:

```text
feature/<issue-number>-<short-name>
fix/<issue-number>-<short-name>
chore/<issue-number>-<short-name>
docs/<issue-number>-<short-name>
```

Examples:

```text
feature/6-source-upload-api
feature/10-semgrep-scanner
chore/23-docker-compose
```

## Commit message convention

Use simple conventional commits:

```text
feat: add source upload API
fix: handle scanner timeout
chore: add docker compose
docs: update architecture document
test: add scan job tests
```

## Pull request rules

Each pull request should include:

- Summary of changes.
- Related issue number.
- Testing steps.
- Screenshots if UI changes are included.

Example:

```text
Closes #6
```

## Suggested labels

Create these labels manually in GitHub if they are not available:

```text
type: feature
type: bug
type: docs
type: chore
area: backend
area: frontend
area: scanner
area: ai-agent
area: devops
area: database
area: rag
priority: high
priority: medium
priority: low
```

## Suggested milestones

Create these milestones manually:

```text
Week 1 - Planning & Architecture
Week 2 - Core Backend
Week 3 - Source Upload & Scan Job
Week 4 - Scanner Integration
Week 5 - Result Normalization & Risk Scoring
Week 6 - AI Code Analysis Agent
Week 7 - Log Analysis & DevOps Agent
Week 8 - Dashboard
Week 9 - Docker, Testing & Optimization
Week 10 - Final Report & Demo
```

## Recommended repository settings

Recommended GitHub settings before implementation:

- Enable Issues.
- Enable Projects.
- Use squash merge for pull requests.
- Protect `main` branch when the project becomes stable.
- Require pull request review before merging if working in a team.
- Add secrets for deployment or AI API keys only in GitHub Secrets, never in code.
