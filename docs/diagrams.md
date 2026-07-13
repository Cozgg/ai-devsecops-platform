# Tổng hợp sơ đồ hệ thống

Tài liệu này tập hợp các sơ đồ chính dùng cho báo cáo đồ án **AI DevSecOps Platform**.

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

```mermaid
classDiagram
    class User {
        +id
        +username
        +email
        +password
        +is_staff
        +is_superuser
        +is_active
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
    }

    class AIReport {
        +id
        +scan_job
        +summary
        +risk_overview
        +recommendation
        +report_json
        +model_name
    }

    class KnowledgeDocument {
        +id
        +title
        +source_type
        +category
        +source_url
        +content
        +active
    }

    class KnowledgeChunk {
        +id
        +document
        +chunk_index
        +content
        +embedding_json
        +metadata
    }

    User "1" --> "many" Project : owns
    User "1" --> "many" ScanJob : creates
    Project "1" --> "many" ScanJob : has
    ScanJob "1" --> "many" ScanFinding : contains
    ScanJob "1" --> "1" AIReport : generates
    KnowledgeDocument "1" --> "many" KnowledgeChunk : splits_into
```

---

## 3. Sequence Diagram - Upload source code và scan

Sơ đồ tuần tự này mô tả use case cốt lõi: User upload source code, hệ thống tạo scan job, worker chạy scanner và sinh AI report.

```mermaid
sequenceDiagram
    actor User
    participant FE as React Frontend
    participant API as Django REST API
    participant DB as PostgreSQL
    participant FS as File Storage
    participant Redis as Redis Queue
    participant Worker as Celery Worker
    participant Scanner as Semgrep/Trivy
    participant KB as Knowledge Base
    participant LLM as AI Model API

    User->>FE: Chọn project và upload source .zip
    FE->>API: POST /api/scans/ kèm source_file
    API->>DB: Kiểm tra project và quyền truy cập
    API->>FS: Lưu file source upload
    API->>DB: Tạo ScanJob(status=PENDING)
    API->>Redis: Đẩy scan_job_id vào queue
    API-->>FE: Trả về scan_job_id

    Worker->>Redis: Nhận scan_job_id
    Worker->>DB: Cập nhật ScanJob(status=RUNNING)
    Worker->>FS: Đọc và giải nén source code
    Worker->>Worker: Detect language/framework
    Worker->>Scanner: Chạy scanner và nhận JSON result
    Scanner-->>Worker: Trả về raw findings
    Worker->>Worker: Normalize findings + risk scoring
    Worker->>DB: Lưu ScanFinding và metadata
    Worker->>KB: Truy xuất tài liệu liên quan cho RAG
    Worker->>LLM: Gửi findings + context để sinh AI report
    LLM-->>Worker: Trả về nội dung báo cáo
    Worker->>DB: Lưu AIReport
    Worker->>DB: Cập nhật ScanJob(status=COMPLETED)

    FE->>API: GET /api/scans/{id}/status/
    API->>DB: Đọc trạng thái scan job
    API-->>FE: Trả về status
    FE->>API: GET findings và AI report
    API->>DB: Đọc findings và AI report
    API-->>FE: Trả về kết quả phân tích
```

---

## 4. Activity Diagram - Scan flow

Sơ đồ hoạt động mô tả luồng xử lý scan job trong worker.

```mermaid
flowchart TD
    A([Bắt đầu]) --> B[User upload source code]
    B --> C[Backend validate file]
    C --> D{File hợp lệ?}
    D -- Không --> E[Trả lỗi validation]
    E --> Z([Kết thúc])

    D -- Có --> F[Lưu file vào storage]
    F --> G[Tạo ScanJob với status PENDING]
    G --> H[Đẩy job vào Redis queue]
    H --> I[Celery Worker nhận job]
    I --> J[Cập nhật status RUNNING]
    J --> K[Giải nén source code]
    K --> L[Detect language/framework]
    L --> M[Chạy Semgrep/Trivy/npm audit]
    M --> N{Scanner chạy thành công?}

    N -- Không --> O[Cập nhật status FAILED và lưu error_message]
    O --> Z

    N -- Có --> P[Normalize scanner result thành ScanFinding]
    P --> Q[Tính security score và risk level]
    Q --> R[Truy xuất Knowledge Base cho RAG]
    R --> S[Gọi AI Model để sinh AI report]
    S --> T{Sinh report thành công?}

    T -- Không --> U[Lưu findings, ghi lỗi AI vào metadata]
    U --> V[Cập nhật status COMPLETED]

    T -- Có --> W[Lưu AIReport]
    W --> V
    V --> Z
```

---

## 5. State Diagram - ScanJob

`ScanJob` là đối tượng có trạng thái rõ nhất trong hệ thống.

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> RUNNING: Worker nhận job
    RUNNING --> COMPLETED: Scan và AI report hoàn tất
    RUNNING --> FAILED: Lỗi validate/extract/scanner/worker
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
        STORAGE[(volume / media storage\nSource upload + extracted source)]
    end

    USER[User Browser] --> FE
    FE --> API
    API --> DB
    API --> STORAGE
    API --> REDIS
    WORKER --> REDIS
    WORKER --> DB
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
