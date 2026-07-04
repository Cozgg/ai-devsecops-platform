# AI DevSecOps Platform

AI DevSecOps Platform is a graduation-project-oriented platform for source code risk analysis, security scanning, AI-assisted remediation, log analysis, and basic system anomaly monitoring.

## Project goals

- Manage user projects and uploaded source code.
- Run asynchronous scan jobs using background workers.
- Integrate security scanners such as Semgrep, Trivy, Bandit, or npm audit.
- Normalize scanner results into a common finding format.
- Calculate risk/security scores for each scan.
- Use an AI Code Analysis Agent with RAG to explain findings and suggest remediation.
- Collect backend/worker/scanner logs.
- Use an AI DevOps Agent to analyze incidents and suggest basic operational actions.

## Planned tech stack

- Frontend: ReactJS
- Backend API: FastAPI or Django REST Framework
- Worker: Celery
- Queue/Broker: Redis
- Database: PostgreSQL
- Vector database: PostgreSQL + pgvector
- AI Agent: LangChain or LangGraph
- Scanner tools: Semgrep, Trivy, Bandit, npm audit
- DevOps: Docker Compose, GitHub Actions, optional AWS deployment

## Initial repository structure

```text
ai-devsecops-platform/
├── frontend/
├── backend/
├── worker/
├── docs/
├── samples/
├── docker-compose.yml
├── .env.example
└── README.md
```

## MVP scope

The first MVP focuses on:

1. Project management.
2. Source code upload.
3. Scan job lifecycle.
4. Background scan worker.
5. Semgrep/dependency scanner integration.
6. Result normalization.
7. Risk scoring.
8. AI/RAG remediation report.
9. Basic log collection.
10. Rule-based anomaly detection.

## Development workflow

1. Pick an issue from the GitHub Issues backlog.
2. Create a feature branch from `main`.
3. Implement the feature.
4. Open a pull request.
5. Review, test, and merge.

Suggested branch naming:

```text
feature/issue-number-short-name
chore/issue-number-short-name
fix/issue-number-short-name
```

Example:

```text
feature/6-source-upload-api
```

## Documentation

- System architecture: `docs/architecture.md`
- Development plan: `docs/development-plan.md`
- GitHub workflow: `docs/github-workflow.md`

## Status

Planning phase. See GitHub Issues for the 10-week roadmap.
