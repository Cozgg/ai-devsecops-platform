# Tổng hợp sơ đồ hệ thống

Tài liệu này tập hợp các sơ đồ chính dùng cho báo cáo đồ án **AI DevSecOps Platform**.

Nội dung trong tài liệu này được đối chiếu với các model backend hiện tại của hệ thống, bao gồm:

```text
accounts.User
projects.Project
scans.ScanJob
findings.ScanFinding
ai_agents.AIReport
knowledge_base.KnowledgeDocument
knowledge_base.KnowledgeChunk
```

Các sơ đồ nên đưa vào Chương 3 của báo cáo:

- C4 Architecture Diagram: mô tả kiến trúc tổng thể.
- Use Case Diagram: mô tả chức năng hệ thống theo actor.
- ERD: mô tả cơ sở dữ liệu.
- UML Class Diagram: mô tả các entity/model chính.
- Sequence Diagram: mô tả trình tự xử lý use case upload source và scan.
- Activity Diagram: mô tả luồng xử lý scan job.
- State Diagram: mô tả trạng thái của `ScanJob`.
- Deployment Diagram: mô tả triển khai bằng Docker Compose.

---

## 1. Tài liệu liên quan

| Sơ đồ | File |
|---|---|
| C4 Level 1, 2, 3 | [`docs/C4.md`](C4.md) |
| Use Case | [`docs/use-case.md`](use-case.md) |
| ERD / Database Design | [`docs/database-design.md`](database-design.md) |

---

## 2. UML Class Diagram

Sơ đồ lớp tập trung vào các entity/model chính của hệ thống. Không đưa serializer, viewset hoặc service nhỏ vào sơ đồ này để tránh rối.

Các model `Project` và `KnowledgeDocument` kế thừa `ActiveTimeStampedModel`, nên có thêm các field `active`, `created_date`, `updated_date`. Các model `ScanJob`, `ScanFinding`, `AIReport` và `KnowledgeChunk` kế thừa `TimeStampedModel`, nên có thêm `created_date`, `updated_date`.

```mermaid
classDiagram
    class AbstractUser {
        <<Django AbstractUser>>
        +id
        +username
        +password
        +email
        +first_name
        +last_name
        +is_staff
        +is_superuser
        +is_active
        +last_login
        +date_joined
    }

    class User {
        +db_table = accounts_user
        +__str__()
    }

    class TimeStampedModel {
        <<abstract>>
        +created_date
        +updated_date
    }

    class ActiveTimeStampedModel {
        <<abstract>>
        +active
    }

    class Project {
        +id
        +owner
        +name
        +description
        +active
        +created_date
        +updated_date
    }

    class ScanJob {
        +id
        +project
        +created_by
        +source_file
        +status
        +scan_type
        +error_message
        +metadata
        +started_at
        +finished_at
        +created_date
        +updated_date
    }

    class ScanFinding {
        +id
        +scan_job
        +scanner_name
        +title
        +severity
        +description
        +file_path
        +line_number
        +code_snippet
        +status
        +raw_data
        +created_date
        +updated_date
    }

    class AIReport {
        +id
        +scan_job
        +summary
        +risk_overview
        +recommendation
        +report_json
        +model_name
        +created_date
        +updated_date
    }

    class KnowledgeDocument {
        +id
        +title
        +source_type
        +category
        +source_url
        +content
        +active
        +created_date
        +updated_date
    }

    class KnowledgeChunk {
        +id
        +document
        +chunk_index
        +content
        +embedding_json
        +metadata
        +created_date
        +updated_date
    }

    AbstractUser <|-- User
    TimeStampedModel <|-- ActiveTimeStampedModel
    ActiveTimeStampedModel <|-- Project
    TimeStampedModel <|-- ScanJob
    TimeStampedModel <|-- ScanFinding
    TimeStampedModel <|-- AIReport
    ActiveTimeStampedModel <|-- KnowledgeDocument
    TimeStampedModel <|-- KnowledgeChunk

    User "1" --> "many" Project : owns
    User "1" --> "many" ScanJob : creates
    Project "1" --> "many" ScanJob : has
    ScanJob "1" --> "many" ScanFinding : contains
    ScanJob "1" --> "1" AIReport : generates
    KnowledgeDocument "1" --> "many" KnowledgeChunk : splits_into
```

### 2.1. Giá trị enum quan trọng

Các field dạng trạng thái trong backend dùng `TextChoices` để giới hạn giá trị hợp lệ.

| Model | Field | Giá trị |
|---|---|---|
| `ScanJob` | `status` | `PENDING`, `RUNNING`, `COMPLETED`, `FAILED` |
| `ScanJob` | `scan_type` | `SAST`, `DEPENDENCY`, `FULL` |
| `ScanFinding` | `severity` | `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `ScanFinding` | `status` | `OPEN`, `FIXED`, `IGNORED` |
| `KnowledgeDocument` | `source_type` | `OWASP`, `CWE`, `SEMGREP_DOC`, `TRIVY_DOC`, `CUSTOM_NOTE`, `RUNBOOK` |

Ghi chú: `accounts.User` kế thừa `AbstractUser` của Django. Một số field mặc định như `groups` và `user_permissions` vẫn tồn tại theo Django Auth, nhưng không đưa vào sơ đồ chính để giữ diagram gọn và tập trung vào nghiệp vụ MVP.

---

## 3. Sequence Diagram - Upload source code và scan

Sơ đồ tuần tự này mô tả use case cốt lõi: User upload source code, hệ thống tạo `ScanJob`, worker chạy scanner và sinh AI report.

Trong backend hiện tại, API upload tạo `ScanJob` với:

```text
source_file -> lưu file upload
status -> PENDING
scan_type -> SAST / DEPENDENCY / FULL
metadata.source_file_name -> tên file upload
```

```mermaid
sequenceDiagram
    actor User
    participant FE as React Frontend
    participant API as Django REST API
    participant DB as PostgreSQL
    participant FS as File Storage
    participant Redis as Redis Queue
    participant Worker as Celery Worker
    participant Scanner as Semgrep/Trivy/npm audit
    participant KB as Knowledge Base
    participant LLM as AI Model API

    User->>FE: Chọn project và upload source .zip
    FE->>API: POST /api/scans/ với project_id, source_file, scan_type
    API->>DB: Kiểm tra Project.owner và quyền truy cập
    API->>FS: Lưu source_file vào media/source_uploads/
    API->>DB: Tạo ScanJob(status=PENDING, metadata.source_file_name)
    API->>Redis: Đẩy scan_job_id vào queue
    API-->>FE: Trả về ScanJob(id, status=PENDING)

    Worker->>Redis: Nhận scan_job_id
    Worker->>DB: Cập nhật ScanJob(status=RUNNING, started_at)
    Worker->>FS: Đọc source_file và giải nén source code
    Worker->>Worker: Detect language/framework và lưu vào metadata
    Worker->>Scanner: Chạy scanner và nhận JSON result
    Scanner-->>Worker: Trả về raw findings
    Worker->>Worker: Normalize findings + tính risk metadata
    Worker->>DB: Lưu ScanFinding và cập nhật ScanJob.metadata
    Worker->>KB: Truy xuất KnowledgeDocument/KnowledgeChunk cho RAG
    Worker->>LLM: Gửi findings + context để sinh AI report
    LLM-->>Worker: Trả về summary, risk_overview, recommendation
    Worker->>DB: Lưu AIReport(report_json, model_name)
    Worker->>DB: Cập nhật ScanJob(status=COMPLETED, finished_at)

    FE->>API: GET /api/scans/{id}/status/
    API->>DB: Đọc ScanJob.status
    API-->>FE: Trả về status, error_message, started_at, finished_at
    FE->>API: GET report / findings theo scan job
    API->>DB: Đọc ScanFinding và AIReport
    API-->>FE: Trả về kết quả phân tích
```

Ghi chú: các bước từ Redis, Celery Worker, scanner và AI report là luồng kiến trúc mục tiêu. Nếu chưa tích hợp worker, hệ thống dừng ở bước tạo `ScanJob(status=PENDING)` sau khi upload.

---

## 4. Activity Diagram - Scan flow

Sơ đồ hoạt động mô tả luồng xử lý scan job trong worker. Các kết quả như `severity_count`, `total_findings`, `extract_path`, `detected_stack`, `security_score` hoặc `risk_level` nên lưu trong `ScanJob.metadata` vì backend hiện chưa có field riêng cho các giá trị này.

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[User upload source code .zip]
    B --> C[Backend validate source_file]
    C --> D{File hợp lệ?}
    D -- Không --> E[Trả lỗi validation]
    E --> Z([Kết thúc])

    D -- Có --> F[Lưu source_file vào media/source_uploads/]
    F --> G[Tạo ScanJob với status PENDING]
    G --> H[Lưu metadata.source_file_name]
    H --> I[Đẩy scan_job_id vào Redis queue]
    I --> J[Celery Worker nhận job]
    J --> K[Cập nhật status RUNNING và started_at]
    K --> L[Giải nén source code]
    L --> M[Lưu extract_path vào metadata]
    M --> N[Detect language/framework]
    N --> O[Lưu detected_stack vào metadata]
    O --> P[Chạy Semgrep/Trivy/npm audit]
    P --> Q{Scanner chạy thành công?}

    Q -- Không --> R[Cập nhật status FAILED, error_message và finished_at]
    R --> Z

    Q -- Có --> S[Normalize scanner result thành ScanFinding]
    S --> T[Tính severity_count, total_findings, security_score, risk_level]
    T --> U[Lưu risk metadata vào ScanJob.metadata]
    U --> V[Truy xuất KnowledgeDocument và KnowledgeChunk]
    V --> W[Gọi AI Model để sinh AI report]
    W --> X{Sinh report thành công?}

    X -- Không --> Y[Lưu findings, ghi lỗi AI vào metadata]
    Y --> AA[Cập nhật status COMPLETED và finished_at]

    X -- Có --> AB[Lưu AIReport]
    AB --> AA
    AA --> Z
```

---

## 5. State Diagram - ScanJob

`ScanJob` là đối tượng có trạng thái rõ nhất trong hệ thống. Field `status` trong backend hiện có 4 giá trị: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`.

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> RUNNING: Worker nhận job
    RUNNING --> COMPLETED: Scan hoàn tất
    RUNNING --> FAILED: Lỗi extract/scanner/worker
    PENDING --> FAILED: Lỗi khởi tạo job hoặc file không hợp lệ
    FAILED --> [*]
    COMPLETED --> [*]
```

---

## 6. Deployment Diagram - Docker Compose local

Trong MVP, hệ thống được triển khai local bằng Docker Compose để dễ demo, dễ debug và mô phỏng kiến trúc thực tế.

```mermaid
flowchart TB
    subgraph PC[PC Local / Docker Host]
        FE[frontend container\nReact + Nginx hoặc Vite]
        API[backend container\nDjango REST Framework]
        DB[(postgres container\nPostgreSQL)]
        REDIS[(redis container\nRedis Broker)]
        WORKER[celery_worker container\nCelery + Scanner Services]
        MEDIA[(media volume\nsource_file upload)]
        STORAGE[(storage volume\nextracted source + scanner output)]
    end

    USER[User Browser] --> FE
    FE --> API
    API --> DB
    API --> MEDIA
    API --> REDIS
    WORKER --> REDIS
    WORKER --> DB
    WORKER --> MEDIA
    WORKER --> STORAGE
    WORKER --> SCANNER[Semgrep / Trivy / npm audit]
    WORKER --> LLM[AI Model API]
```

---

## 7. Ghi chú sử dụng trong báo cáo

- C4 dùng cho mục **3.2 Kiến trúc hệ thống**.
- Use Case dùng cho mục **3.3 Phân tích sơ đồ use case hệ thống**.
- Class Diagram, Sequence Diagram, Activity Diagram và State Diagram dùng cho mục **3.4 Mô hình hoá hệ thống**.
- ERD dùng cho mục **3.5 Thiết kế cơ sở dữ liệu hệ thống**.
- Deployment Diagram dùng cho mục **3.7.1 Triển khai hệ thống**.
- Các diagram trong tài liệu này phản ánh model backend hiện tại. Nếu sau này thêm field thật như `security_score`, `risk_level`, `language`, `framework` hoặc bảng `SourceUpload`, cần cập nhật lại diagram tương ứng.
