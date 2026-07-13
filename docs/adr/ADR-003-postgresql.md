# Bản ghi Quyết định Kiến trúc

---

## ADR-003: Sử dụng PostgreSQL làm cơ sở dữ liệu chính

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Ngọc Anh Tú - Sinh viên thực hiện  
**Tags**: database, backend

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Hệ thống cần lưu trữ dữ liệu có quan hệ như User, Project, ScanJob, ScanFinding, AIReport, KnowledgeDocument và KnowledgeChunk.

**Hạn chế hiện tại**: Hệ thống không chỉ lưu dữ liệu quan hệ mà còn cần lưu dữ liệu linh hoạt dạng JSON như metadata scan, raw scanner result và report JSON.

**Yêu cầu đồ án**: Cơ sở dữ liệu cần ổn định, dễ tích hợp với Django ORM, hỗ trợ quan hệ dữ liệu rõ ràng và có thể mở rộng cho RAG trong tương lai.

**Bất kỳ ràng buộc nào**: Dự án cần chạy được ở môi trường local và Docker Compose.

---

## Quyết định

Chúng tôi quyết định sử dụng **PostgreSQL** làm hệ quản trị cơ sở dữ liệu chính cho hệ thống.

PostgreSQL sẽ lưu thông tin người dùng, project, scan job, findings, AI report, knowledge base và các trường JSON như `metadata`, `raw_data`, `report_json`.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: SQLite

**Ưu điểm:**
- Dễ dùng, không cần cài database server.
- Phù hợp thử nghiệm ban đầu.

**Nhược điểm:**
- Không phù hợp khi hệ thống cần triển khai nhiều container.
- Không mạnh bằng PostgreSQL cho dữ liệu quan hệ và JSON.

### Tùy chọn 2: MySQL

**Ưu điểm:**
- Phổ biến, ổn định.

**Nhược điểm:**
- PostgreSQL phù hợp hơn với nhu cầu lưu JSON và có khả năng mở rộng sang pgvector sau này.

### Tùy chọn 3: PostgreSQL

**Ưu điểm:**
- Hỗ trợ tốt dữ liệu quan hệ.
- Hỗ trợ JSONField tốt.
- Tương thích tốt với Django ORM.
- Có thể mở rộng sang pgvector cho RAG trong tương lai.

**Nhược điểm:**
- Cần cấu hình database user, password, port.
- Phức tạp hơn SQLite khi chạy local.

---

## Kết quả Quyết định

PostgreSQL được chọn vì phù hợp với hệ thống backend có nhiều bảng dữ liệu quan hệ, hỗ trợ JSON tốt và có khả năng mở rộng cho RAG/embedding trong tương lai.

---

## Hậu quả

### Tích cực

- Dữ liệu có cấu trúc rõ ràng.
- Hỗ trợ tốt cho Django ORM.
- Dễ mở rộng khi cần lưu embedding bằng pgvector.

### Tiêu cực

- Cần cấu hình môi trường database.
- Có thể gặp lỗi kết nối hoặc authentication nếu `.env` không đúng.

### Trung tính / Ghi chú

- Trong MVP, embedding có thể lưu tạm bằng `embedding_json`.
- Sau này có thể nâng cấp sang pgvector nếu cần semantic search tốt hơn.

---

## Tham khảo

- PostgreSQL Documentation
- Django Database Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-001, ADR-007
