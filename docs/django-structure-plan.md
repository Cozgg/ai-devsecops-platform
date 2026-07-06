# Django Structure Plan

This project will follow a Django REST Framework structure similar to the previous `course-app` project, but adapted for AI DevSecOps.

## Why use this structure

The previous project used a classic Django layout:

```text
ecourceapis/
├── manage.py
├── ecourseapis/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── courses/
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

For this platform, we will keep the same simple style:

```text
backend/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/
│   ├── projects/
│   ├── scans/
│   ├── findings/
│   ├── ai_agents/
│   ├── knowledge_base/
│   ├── incidents/
│   └── system_logs/
├── common/
│   ├── models.py
│   ├── permissions.py
│   ├── pagination.py
│   └── utils.py
└── requirements.txt
```

## Django apps

### accounts

Handles:

- User model
- Authentication
- User profile
- Role/permission later if needed

### projects

Handles:

- Project management
- Source upload metadata
- Project language/framework information

### scans

Handles:

- Scan job lifecycle
- Scan status
- Scan steps
- Worker task trigger

### findings

Handles:

- Normalized scanner findings
- Severity
- File path and line number
- Recommendation metadata

### ai_agents

Handles:

- AI Code Analysis Agent
- AI DevOps Agent
- Prompt templates
- Agent execution records

### knowledge_base

Handles:

- RAG documents
- Chunks
- Embeddings metadata
- Source references

### incidents

Handles:

- System incident records
- Anomaly detection results
- AI incident analysis

### system_logs

Handles:

- Backend logs
- Worker logs
- Scanner logs
- Job-related logs

## Worker structure

Long-running tasks should not run inside API requests.

```text
worker/
├── celery_app.py
├── tasks/
│   ├── scan_tasks.py
│   ├── ai_tasks.py
│   └── log_tasks.py
├── scanners/
│   ├── semgrep_runner.py
│   ├── trivy_runner.py
│   └── bandit_runner.py
├── normalizers/
│   ├── semgrep_normalizer.py
│   ├── trivy_normalizer.py
│   └── bandit_normalizer.py
└── services/
    ├── risk_score_service.py
    ├── rag_service.py
    └── incident_service.py
```

## Frontend structure

```text
frontend/
├── src/
│   ├── app/
│   ├── pages/
│   ├── components/
│   ├── features/
│   │   ├── auth/
│   │   ├── projects/
│   │   ├── scans/
│   │   ├── findings/
│   │   └── incidents/
│   ├── services/
│   └── utils/
└── package.json
```

## Important difference from the old project

Do not hardcode secrets in `settings.py`.

Use environment variables through `.env` and `.env.example`:

```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "false") == "true"
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

## Recommended API style

Use Django REST Framework ViewSets and routers for simple CRUD APIs:

```python
router = routers.DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("source-uploads", SourceUploadViewSet)
router.register("scan-jobs", ScanJobViewSet)
router.register("findings", FindingViewSet)
router.register("incidents", IncidentViewSet)
```

For special actions, use custom DRF actions:

```python
POST /api/projects/{id}/upload-source/
POST /api/scan-jobs/{id}/start/
GET  /api/scan-jobs/{id}/status/
POST /api/ai/code-analysis/
POST /api/ai/incident-analysis/
```

## MVP implementation order

1. Create Django project under `backend/`.
2. Create apps: `accounts`, `projects`, `scans`, `findings`.
3. Add PostgreSQL settings through environment variables.
4. Add DRF + Swagger/OpenAPI.
5. Implement project CRUD.
6. Implement source upload metadata.
7. Implement scan job model and status API.
8. Add Celery worker after API skeleton works.
