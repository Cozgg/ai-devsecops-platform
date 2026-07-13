# Architecture Decision Records (ADR)

Thư mục này lưu các bản ghi quyết định kiến trúc cho đồ án **AI DevSecOps Platform**.

Mỗi ADR mô tả một quyết định kỹ thuật quan trọng, bao gồm bối cảnh, lựa chọn đã xem xét, quyết định cuối cùng và hậu quả của quyết định đó.

## Danh sách ADR

| ADR | Quyết định | Trạng thái |
|---|---|---|
| [ADR-001](ADR-001-django-rest-framework.md) | Sử dụng Django REST Framework cho Backend API | Đã chấp nhận |
| [ADR-002](ADR-002-reactjs.md) | Sử dụng ReactJS cho Frontend | Đã chấp nhận |
| [ADR-003](ADR-003-postgresql.md) | Sử dụng PostgreSQL làm cơ sở dữ liệu chính | Đã chấp nhận |
| [ADR-004](ADR-004-celery-redis.md) | Sử dụng Celery và Redis cho xử lý bất đồng bộ | Đã chấp nhận |
| [ADR-005](ADR-005-semgrep.md) | Sử dụng Semgrep cho phân tích mã nguồn tĩnh | Đã chấp nhận |
| [ADR-006](ADR-006-dependency-scanning.md) | Sử dụng Trivy hoặc npm audit cho phân tích dependency | Đã chấp nhận |
| [ADR-007](ADR-007-langchain-rag.md) | Sử dụng LangChain và RAG cho AI Report | Đã chấp nhận |
| [ADR-008](ADR-008-docker-compose.md) | Sử dụng Docker Compose cho môi trường triển khai local | Đã chấp nhận |
| [ADR-009](ADR-009-local-file-storage.md) | Sử dụng local file storage cho source code upload trong MVP | Đã chấp nhận |

## Quy ước đặt tên

```text
ADR-XXX-ten-quyet-dinh.md
```

Ví dụ:

```text
ADR-005-semgrep.md
```
