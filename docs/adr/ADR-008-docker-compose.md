# Bản ghi Quyết định Kiến trúc

---

## ADR-008: Sử dụng Docker Compose cho môi trường triển khai local

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Hữu Công - Sinh viên thực hiện  
**Tags**: deployment, docker, devops

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Hệ thống gồm nhiều thành phần như Backend API, PostgreSQL, Redis, Celery Worker và Frontend. Nếu chạy thủ công từng thành phần, quá trình cài đặt và demo dễ bị lỗi môi trường.

**Hạn chế hiện tại**: Mỗi máy có thể có phiên bản Python, Node.js, PostgreSQL hoặc Redis khác nhau, gây khó khăn khi chạy lại dự án.

**Yêu cầu đồ án**: Hệ thống cần có cách triển khai đơn giản, có thể chạy lại được và phù hợp với môi trường local hoặc server nhỏ.

**Bất kỳ ràng buộc nào**: Không dùng Kubernetes trong MVP vì quá phức tạp so với phạm vi đồ án.

---

## Quyết định

Chúng tôi quyết định sử dụng **Docker Compose** để cấu hình và chạy các service chính của hệ thống.

Docker Compose sẽ quản lý Backend API, PostgreSQL, Redis, Celery Worker, Frontend và các biến môi trường cần thiết.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Chạy thủ công từng service

**Ưu điểm:**
- Dễ hiểu ở giai đoạn đầu.
- Không cần viết Dockerfile ngay.

**Nhược điểm:**
- Dễ lỗi môi trường.
- Khó demo trên máy khác.
- Khó quản lý nhiều service cùng lúc.

### Tùy chọn 2: Docker Compose

**Ưu điểm:**
- Chạy nhiều service bằng một lệnh.
- Phù hợp với kiến trúc backend, database, redis, worker và frontend.
- Dễ demo và tái lập môi trường.

**Nhược điểm:**
- Cần viết Dockerfile và docker-compose.yml.
- Cần hiểu volume, network và biến môi trường.

### Tùy chọn 3: Kubernetes

**Ưu điểm:**
- Phù hợp hệ thống lớn.
- Hỗ trợ scale và orchestration mạnh.

**Nhược điểm:**
- Quá phức tạp cho MVP.
- Không phù hợp thời gian thực hiện đồ án.

---

## Kết quả Quyết định

Docker Compose được chọn để triển khai hệ thống ở môi trường local/demo. Giải pháp này giúp đơn giản hóa việc chạy nhiều service và phù hợp với mục tiêu DevOps của đề tài.

---

## Hậu quả

### Tích cực

- Dễ chạy toàn bộ hệ thống.
- Dễ demo.
- Giảm lỗi do khác biệt môi trường.
- Phù hợp với backend, database, redis, worker và frontend.

### Tiêu cực

- Cần thêm thời gian cấu hình Dockerfile.
- Máy local cần đủ RAM để chạy nhiều container.

### Trung tính / Ghi chú

- Docker Compose nên được làm sau khi backend API và worker chạy ổn.
- Không cần dùng Kubernetes trong phạm vi MVP.

---

## Tham khảo

- Docker Documentation
- Docker Compose Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-001, ADR-003, ADR-004
