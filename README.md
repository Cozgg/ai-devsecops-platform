# AI DevSecOps Platform

## Mô tả

**AI DevSecOps Platform** là nền tảng hỗ trợ quản lý project source code, upload mã nguồn dạng `.zip`, tạo scan job bất đồng bộ và sinh báo cáo bảo mật bằng AI.

Mục tiêu dài hạn của hệ thống là xây dựng một MVP DevSecOps có thể:

```text
Upload source code
→ Create scan job
→ Worker xử lý bất đồng bộ
→ Extract source code
→ Detect language/framework
→ Run scanner như Semgrep/Trivy/npm audit
→ Normalize findings
→ Risk scoring
→ AI/RAG report
→ Hiển thị kết quả trên dashboard
```

Ở trạng thái hiện tại, dự án chưa phải là full platform hoàn chỉnh. Repository đang ở giai đoạn **backend MVP foundation**, đã có API nền tảng, upload scan job, Celery worker giả lập và scaffold AI Report.

---

## Trạng thái hiện tại

| Hạng mục | Trạng thái | Ghi chú |
|---|---:|---|
| Backend Django REST Framework | ✅ Đã có | Đã có cấu trúc app chính |
| Model nền tảng | ✅ Đã có | User, Project, ScanJob, ScanFinding, AIReport, KnowledgeDocument, KnowledgeChunk |
| Project API | ✅ Đã có | Tạo, xem danh sách, xem chi tiết project |
| Upload `.zip` tạo `ScanJob` | ✅ Đã có | Upload source file và tạo job trạng thái `PENDING` |
| Redis + Celery worker | ✅ Đã có | Worker nhận job và cập nhật trạng thái |
| Worker simulation | ✅ Đã có | `PENDING → RUNNING → COMPLETED` |
| AI Report scaffold | ✅ Đã có | Có endpoint generate/get report, hiện dùng logic mock/deterministic |
| Source extraction | ❌ Chưa có | Chưa giải nén zip thật |
| Detect language/framework | ❌ Chưa có | Sẽ làm sau bước extract |
| Semgrep/Trivy/npm audit runner | ❌ Chưa có | Chưa scan source code thật |
| Normalize scanner result | ❌ Chưa có | Chưa sinh `ScanFinding` tự động từ scanner |
| Risk scoring thật | ❌ Chưa có | Hiện mới có risk overview trong report mock |
| AI API thật | ❌ Chưa có | Chưa gọi OpenAI/Gemini thật |
| LangChain/RAG thật | ❌ Chưa có | Knowledge base mới là model nền |
| Frontend dashboard | ❌ Chưa có | `frontend/` là hướng phát triển tiếp |
| Docker Compose | ❌ Chưa có | Mới có ADR/kế hoạch, chưa có file `docker-compose.yml` |
| Tests thực tế | ❌ Chưa có | Cần bổ sung sau từng feature |

---

## Công nghệ sử dụng

### Đã sử dụng trong code hiện tại

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Background Worker**: Celery
- **Auth**: Django Auth / Custom User
- **File Upload**: Django media storage
- **Documentation**: Markdown, C4, ERD, UML, ADR

### Dự kiến tích hợp ở các bước sau

- **Scanner**: Semgrep, Trivy, npm audit
- **AI/RAG**: OpenAI hoặc Gemini API, LangChain, RAG
- **Frontend**: ReactJS
- **Container**: Docker Compose
- **Observability**: Prometheus, Grafana, Loki
- **Deployment**: AWS EC2/Lightsail/RDS/S3 trong giai đoạn mở rộng

---

## Luồng hiện tại đã chạy được

Hiện tại repository đã chạy được luồng bất đồng bộ tối thiểu:

```text
User upload source .zip
        ↓
Django REST API validate file
        ↓
Tạo ScanJob(status=PENDING)
        ↓
Đẩy scan_job_id vào Celery queue
        ↓
Celery Worker nhận task
        ↓
Cập nhật ScanJob(status=RUNNING)
        ↓
Giả lập xử lý scan
        ↓
Cập nhật ScanJob(status=COMPLETED)
        ↓
Ghi metadata.worker vào database
```

Ví dụ metadata sau khi worker simulation chạy thành công:

```json
{
  "source_file_name": "test-source.zip",
  "worker": {
    "processed": true,
    "mode": "simulation",
    "message": "Celery worker processed this scan job successfully."
  }
}
```

---

## Luồng AI Report hiện tại

AI Report hiện mới là scaffold để chuẩn bị cho bước gọi AI API thật.

Luồng hiện tại:

```text
ScanJob
↓
Lấy ScanFinding nếu đã có
↓
Nếu chưa có ScanFinding thì dùng mock findings
↓
Build report_json bằng logic backend
↓
Lưu AIReport
```

Endpoint hiện có:

```text
POST /api/ai-reports/scans/<scan_job_id>/generate/
GET  /api/ai-reports/scans/<scan_job_id>/
```

Ghi chú: phần này **chưa gọi OpenAI/Gemini API thật** và **chưa dùng LangChain/RAG thật**.

---

## Kiến trúc tổng quan

```text
Client / API Consumer
        ↓
Django REST API
        ↓
PostgreSQL
        ↓
Redis Queue
        ↓
Celery Worker
        ↓
Scanner Services / AI Report Services
```

Ở hiện tại, `Scanner Services` mới dừng ở mức simulation. Các bước source extraction, Semgrep/Trivy/npm audit và AI/RAG thật sẽ được bổ sung dần trong các branch tiếp theo.

Tài liệu kiến trúc và mô hình hóa nằm trong thư mục `docs/`:

- [C4 Architecture](docs/C4.md)
- [Database Design](docs/database-design.md)
- [Use Case](docs/use-case.md)
- [System Diagrams](docs/diagrams.md)
- [Architecture Decision Records](docs/adr/)
- [Development Plan](docs/development-plan.md)
- [GitHub Workflow](docs/github-workflow.md)

---

## Cấu trúc thư mục hiện tại

```text
ai-devsecops-platform/
├── backend/
│   ├── accounts/
│   ├── projects/
│   ├── scans/
│   ├── findings/
│   ├── ai_agents/
│   ├── knowledge_base/
│   ├── common/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── docs/
│   ├── adr/
│   ├── C4.md
│   ├── database-design.md
│   ├── use-case.md
│   └── diagrams.md
│
├── frontend/          # Dự kiến phát triển sau
├── worker/            # Dự kiến nếu tách worker riêng
├── samples/           # Dự kiến chứa sample source code
├── .env.example
└── README.md
```

---

## Cài đặt và chạy local

### 1. Clone project

```bash
git clone https://github.com/Cozgg/ai-devsecops-platform.git
cd ai-devsecops-platform
```

### 2. Tạo file môi trường

```bash
cp .env.example .env
```

Nếu chạy Redis bằng Docker riêng trên máy local, nên dùng:

```env
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

Nếu sau này chạy toàn bộ bằng Docker Compose, hostname Redis có thể đổi thành `redis`.

### 3. Cài backend

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Cài dependencies:

```bash
pip install -r requirements.txt
```

### 4. Chạy database migration

```bash
python manage.py check
python manage.py migrate
python manage.py createsuperuser
```

### 5. Chạy Redis bằng Docker

Vì hiện chưa có `docker-compose.yml`, có thể chạy Redis riêng:

```bash
docker run --name ai-devsecops-redis -p 6379:6379 -d redis:7
```

Nếu container đã tồn tại:

```bash
docker start ai-devsecops-redis
```

### 6. Chạy Django server

Terminal 1:

```bash
cd backend
python manage.py runserver
```

Backend chạy tại:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

### 7. Chạy Celery worker

Terminal 2:

Windows:

```bash
cd backend
celery -A config worker -l info -P solo
```

Linux/macOS:

```bash
cd backend
celery -A config worker -l info
```

Nếu worker chạy đúng, log sẽ có task:

```text
[tasks]
  . scans.tasks.run_scan_job
```

---



## Tài liệu liên quan

- [C4 Architecture](docs/C4.md)
- [Database Design](docs/database-design.md)
- [Use Case](docs/use-case.md)
- [System Diagrams](docs/diagrams.md)
- [ADRs](docs/adr/)
- [Development Plan](docs/development-plan.md)
- [GitHub Workflow](docs/github-workflow.md)
