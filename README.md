# AI DevSecOps Platform

## Mô tả

**AI DevSecOps Platform** là nền tảng hỗ trợ phân tích mã nguồn, phát hiện rủi ro bảo mật và sinh báo cáo gợi ý khắc phục bằng AI Agent.

Hệ thống cho phép người dùng tạo project, upload source code, tạo scan job, chạy scanner như Semgrep/Trivy hoặc npm audit, chuẩn hóa findings, tính mức độ rủi ro và sử dụng LangChain kết hợp RAG để sinh báo cáo AI dễ hiểu hơn so với raw scanner result.

Mục tiêu của đồ án là xây dựng một MVP có thể chạy local bằng Docker Compose, phục vụ demo luồng DevSecOps cơ bản:

```text
Upload source code
→ Create scan job
→ Worker xử lý bất đồng bộ
→ Run scanner
→ Normalize findings
→ Risk scoring
→ RAG + LangChain
→ AI report
```

---

## Công nghệ sử dụng

- **Backend**: Django REST Framework
- **Frontend**: ReactJS
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Background Worker**: Celery
- **Scanner**: Semgrep, Trivy hoặc npm audit
- **AI/RAG**: LangChain + RAG
- **Container**: Docker + Docker Compose
- **Development Workflow**: GitHub Issues, Pull Requests, ADRs

---

## Phạm vi MVP

MVP tập trung vào các chức năng chính:

1. Quản lý người dùng cơ bản bằng Django Auth.
2. Quản lý project source code.
3. Upload source code dạng `.zip`.
4. Tạo và theo dõi scan job.
5. Xử lý scan job bất đồng bộ bằng Celery + Redis.
6. Detect ngôn ngữ/framework cơ bản.
7. Chạy Semgrep và dependency scanner.
8. Chuẩn hóa scanner result thành `ScanFinding`.
9. Tính security score và risk level.
10. Sinh AI report bằng LangChain + RAG.
11. Hiển thị project, scan result, findings và AI report trên frontend.

Các phần được xem là mở rộng sau MVP:

- Log analysis và incident analysis.
- Prometheus, Grafana, Loki.
- pgvector cho semantic search.
- LangGraph cho agent workflow phức tạp.
- AWS EC2/Lightsail deployment.
- Kubernetes hoặc auto-scaling.

---

## Kiến trúc

Hệ thống được thiết kế theo hướng web application có xử lý bất đồng bộ:

```text
React Frontend
      ↓
Django REST API
      ↓
PostgreSQL / Redis / File Storage
      ↓
Celery Worker
      ↓
Scanner Runtime + LangChain/RAG + AI Model API
```

Các sơ đồ kiến trúc và mô hình hóa hệ thống nằm trong thư mục `docs/`:

- [C4 Architecture](docs/C4.md)
- [Database Design](docs/database-design.md)
- [Use Case](docs/use-case.md)
- [System Diagrams](docs/diagrams.md)
- [Architecture Decision Records](docs/adr/)

---

## Cấu trúc thư mục dự kiến

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
├── frontend/
├── docs/
│   ├── adr/
│   ├── C4.md
│   ├── database-design.md
│   ├── use-case.md
│   └── diagrams.md
│
├── samples/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Cài đặt và chạy

### Yêu cầu hệ thống

- Git
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis
- Docker & Docker Compose, khuyến khích cho giai đoạn demo

---

### Cách 1: Chạy local trong giai đoạn phát triển

#### 1. Clone project

```bash
git clone https://github.com/Cozgg/ai-devsecops-platform.git
cd ai-devsecops-platform
```

#### 2. Cấu hình backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Tạo file `.env` từ `.env.example` nếu đã có:

```bash
cp ../.env.example ../.env
```

#### 3. Chạy migration

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Chạy backend

```bash
python manage.py runserver
```

Backend mặc định chạy tại:

```text
http://localhost:8000
```

#### 5. Chạy frontend

```bash
cd ../frontend
npm install
npm run dev
```

Frontend mặc định chạy tại:

```text
http://localhost:5173
```

---

### Cách 2: Chạy bằng Docker Compose

Docker Compose sẽ được sử dụng ở giai đoạn MVP/demo để chạy nhiều service cùng lúc:

```text
backend
frontend
postgres
redis
celery_worker
```

Lệnh dự kiến:

```bash
docker compose up --build
```

> Ghi chú: Docker Compose nên được hoàn thiện sau khi backend API và Celery worker chạy ổn ở môi trường local.

---

## Demo chức năng dự kiến

Các chức năng cần có ảnh chụp hoặc video demo khi hoàn thiện:

### 1. Quản lý Project

User có thể tạo project source code, xem danh sách project và xem chi tiết project.

### 2. Upload Source Code

User upload source code dạng `.zip`, hệ thống tạo `ScanJob` với trạng thái `PENDING`.

### 3. Scan Job Processing

Celery Worker xử lý scan job, giải nén source code, detect ngôn ngữ/framework, chạy scanner và cập nhật trạng thái job.

### 4. Findings Dashboard

User xem danh sách findings theo severity, file path, line number và scanner name.

### 5. AI Report

User xem báo cáo AI gồm summary, risk overview và recommendation.

### 6. Knowledge Base

Admin quản lý tài liệu bảo mật phục vụ RAG như OWASP, CWE, scanner docs hoặc ghi chú nội bộ.

---

## Tài liệu

- [C4 Architecture](docs/C4.md)
- [Database Design](docs/database-design.md)
- [Use Case](docs/use-case.md)
- [System Diagrams](docs/diagrams.md)
- [ADRs](docs/adr/)
- [Development Plan](docs/development-plan.md)
- [GitHub Workflow](docs/github-workflow.md)

---

## Quy trình phát triển

1. Chọn issue từ GitHub Issues.
2. Tạo branch mới từ `main`.
3. Code hoặc viết tài liệu theo phạm vi của issue.
4. Mở Pull Request.
5. Review, test và merge.

Quy ước đặt tên branch:

```text
feature/short-feature-name
docs/short-document-name
chore/short-task-name
fix/short-bug-name
```

Ví dụ:

```text
docs/project-documentation-structure
feature/project-api
feature/scan-upload-api
```

---

## Trạng thái hiện tại

Dự án đang ở giai đoạn xây dựng MVP:

- Đã khởi tạo cấu trúc backend cơ bản.
- Đã có model MVP cho User, Project, ScanJob, ScanFinding, AIReport, KnowledgeDocument và KnowledgeChunk.
- Đã có C4 architecture và ADR cho các quyết định kỹ thuật chính.
- Bước tiếp theo là hoàn thiện database design, use case, API cơ bản cho Project và ScanJob upload.
