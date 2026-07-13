# Bản ghi Quyết định Kiến trúc

---

## ADR-009: Sử dụng local file storage cho source code upload trong MVP

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Hữu Công - Sinh viên thực hiện  
**Tags**: storage, upload, mvp

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Người dùng cần upload source code dạng file `.zip` để hệ thống tạo scan job và xử lý. File upload cần được lưu lại để worker có thể giải nén và chạy scanner.

**Hạn chế hiện tại**: Nếu dùng cloud storage ngay từ đầu, dự án sẽ cần thêm cấu hình bucket, credential và xử lý quyền truy cập, làm tăng độ phức tạp cho MVP.

**Yêu cầu đồ án**: Hệ thống cần upload được source code và worker cần truy cập được file để xử lý scan.

**Bất kỳ ràng buộc nào**: MVP chỉ cần chạy local hoặc Docker Compose, chưa cần triển khai storage cloud như AWS S3.

---

## Quyết định

Chúng tôi quyết định sử dụng **local file storage** trong giai đoạn MVP.

Django sẽ lưu file upload vào `MEDIA_ROOT`. Source code sau khi giải nén có thể lưu trong `STORAGE_ROOT` hoặc thư mục nội bộ dành cho từng scan job.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Lưu file cục bộ

**Ưu điểm:**
- Dễ triển khai.
- Phù hợp MVP.
- Không cần cấu hình cloud.
- Worker có thể truy cập file trực tiếp trong cùng môi trường triển khai.

**Nhược điểm:**
- Không phù hợp nếu triển khai production nhiều server.
- Cần quản lý xóa file sau khi scan.

### Tùy chọn 2: AWS S3 hoặc object storage

**Ưu điểm:**
- Phù hợp production.
- Dễ mở rộng dung lượng lưu trữ.

**Nhược điểm:**
- Cần cấu hình cloud, bucket và credential.
- Làm tăng độ phức tạp của đồ án.

### Tùy chọn 3: Lưu trực tiếp vào database

**Ưu điểm:**
- Tập trung dữ liệu trong database.

**Nhược điểm:**
- Không phù hợp với file source code lớn.
- Làm database nặng và khó quản lý backup/restore.

---

## Kết quả Quyết định

Local file storage được chọn cho MVP để đơn giản hóa quá trình upload và scan source code. Hướng này phù hợp với môi trường local/Docker Compose và có thể mở rộng sang object storage trong tương lai.

---

## Hậu quả

### Tích cực

- Dễ triển khai nhanh.
- Worker có thể truy cập file trực tiếp.
- Không phụ thuộc dịch vụ cloud.

### Tiêu cực

- Cần quản lý dung lượng file upload.
- Cần cơ chế dọn dẹp file cũ nếu hệ thống dùng lâu dài.

### Trung tính / Ghi chú

- MVP nên giới hạn định dạng `.zip`.
- Nên giới hạn dung lượng upload để tránh lỗi khi demo.

---

## Tham khảo

- Django FileField Documentation
- Docker Volume Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-004, ADR-008
