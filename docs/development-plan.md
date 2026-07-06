# Development Plan

This plan maps the 10-week roadmap to the GitHub Issues backlog.

## Week 1 - Planning & Architecture

Focus:

- Repository structure.
- System architecture.
- Database schema.

Related issues:

- #1 Initialize project repository structure
- #2 Design system architecture document
- #3 Design database schema

## Week 2 - Core Backend

Focus:

- User account APIs.
- Project management APIs.

Related issues:

- #4 Implement user sign-in API
- #5 Implement project management API

## Week 3 - Source Upload & Scan Job

Focus:

- Source code upload.
- Scan job creation.
- Scan job status tracking.

Related issues:

- #6 Implement source code upload API
- #7 Implement scan job creation
- #8 Implement scan job status tracking

## Week 4 - Scanner Integration

Focus:

- Celery worker.
- Redis queue.
- Semgrep integration.
- Dependency scanner integration.

Related issues:

- #9 Implement Celery worker for scan jobs
- #10 Integrate Semgrep scanner
- #11 Integrate dependency vulnerability scanner

## Week 5 - Result Normalization & Risk Scoring

Focus:

- Common finding schema.
- Normalizer for scanner outputs.
- Risk scoring engine.

Related issues:

- #12 Normalize scanner results
- #13 Implement risk scoring engine

## Week 6 - AI Code Analysis Agent

Focus:

- Security knowledge base.
- RAG retrieval.
- AI remediation report.

Related issues:

- #14 Build security knowledge base for RAG
- #15 Implement AI Code Analysis Agent

## Week 7 - Log Analysis & AI DevOps Agent

Focus:

- System log collection.
- Basic anomaly rules.
- Incident analysis by AI DevOps Agent.

Related issues:

- #16 Implement system log collection
- #17 Implement system health anomaly rules
- #18 Implement AI DevOps Agent for incident analysis

## Week 8 - Frontend Dashboard

Focus:

- Auth pages.
- Project/upload dashboard.
- Scan result dashboard.
- Incident dashboard.

Related issues:

- #19 Build authentication pages
- #20 Build project and upload dashboard
- #21 Build scan result dashboard
- #22 Build DevOps incident dashboard

## Week 9 - Docker, Testing & Optimization

Focus:

- Docker Compose.
- Basic API tests.
- Demo vulnerable projects.

Related issues:

- #23 Dockerize application
- #24 Add basic backend API tests
- #25 Prepare demo data and vulnerable sample projects

## Week 10 - Final Report & Demo

Focus:

- README.
- Setup guide.
- Demo script.
- Limitation and future work.

Related issues:

- #26 Write final documentation and demo script

## Definition of Done

A task is considered done when:

- Code is committed to a feature branch.
- The related issue is linked in the pull request.
- Local tests or manual verification are completed.
- Documentation is updated if needed.
- The pull request is reviewed and merged.
