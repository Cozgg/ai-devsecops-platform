# Bản ghi Quyết định Kiến trúc

---

## ADR-004: Sử dụng Celery và Redis cho xử lý bất đồng bộ

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Hữu Công - Sinh viên thực hiện  
**Tags**: async, queue, worker, backend

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Quá trình scan source code có thể mất nhiều thời gian vì hệ thống cần giải nén file, detect ngôn ngữ/framework, chạy scanner, chuẩn hóa findings, tính risk score và sinh AI report.

**Hạn chế hiện tại**: Nếu xử lý trực tiếp trong request API, người dùng sẽ phải chờ lâu và API dễ bị timeout.

**Yêu cầu đồ án**: Hệ thống cần tách luồng request-response khỏi các tác vụ nền tốn thời gian để đảm bảo API phản hồi nhanh.

**Bất kỳ ràng buộc nào**: MVP cần chạy được trong Docker Compose với cấu hình đơn giản.

---

## Quyết định

Chúng tôi quyết định sử dụng **Celery** để xử lý các tác vụ nền và **Redis** làm message broker.

Django REST API sẽ tạo `ScanJob` và đẩy job vào Redis queue. Celery Worker nhận job và thực hiện các bước xử lý scan ở background.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Xử lý đồng bộ trong API

**Ưu điểm:**
- Dễ triển khai.
- Không cần thêm worker hoặc message broker.

**Nhược điểm:**
- API phản hồi chậm.
- Dễ timeout khi scan project lớn.
- Không phù hợp với tác vụ scanner và AI report.

### Tùy chọn 2: Celery + RabbitMQ

**Ưu điểm:**
- RabbitMQ mạnh về message queue.
- Phù hợp với hệ thống lớn.

**Nhược điểm:**
- Cấu hình phức tạp hơn.
- Với MVP, RabbitMQ có thể làm hệ thống nặng không cần thiết.

### Tùy chọn 3: Celery + Redis

**Ưu điểm:**
- Dễ triển khai với Docker Compose.
- Phù hợp với MVP.
- Redis có thể dùng làm broker cho Celery.
- Cấu hình đơn giản hơn RabbitMQ.

**Nhược điểm:**
- Không mạnh bằng RabbitMQ trong các use case message queue phức tạp.
- Cần chạy thêm Redis container.

---

## Kết quả Quyết định

Celery và Redis được chọn để xử lý scan job bất đồng bộ. Cách này giúp API phản hồi nhanh, tách riêng luồng xử lý scanner khỏi request-response và phù hợp với kiến trúc Backend API + Worker của hệ thống.

---

## Hậu quả

### Tích cực

- API tạo scan job phản hồi nhanh.
- Worker có thể xử lý các tác vụ scan tốn thời gian.
- Dễ mở rộng số lượng worker sau này.
- Phù hợp với Docker Compose.

### Tiêu cực

- Hệ thống cần thêm Redis và Celery Worker.
- Cần quản lý trạng thái job như `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`.

### Trung tính / Ghi chú

- MVP chỉ cần một worker.
- Sau này có thể thêm retry, timeout và monitoring cho Celery task.

---

## Tham khảo

- Celery Documentation
- Redis Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-001, ADR-008
