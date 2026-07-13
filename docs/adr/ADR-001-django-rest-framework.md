# Bản ghi Quyết định Kiến trúc

---

## ADR-001: Sử dụng Django REST Framework cho Backend API

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Hữu Công - Sinh viên thực hiện  
**Tags**: backend, api, framework

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Hệ thống cần một backend để quản lý người dùng, project, scan job, findings, AI report và knowledge base. Backend cũng cần cung cấp REST API cho frontend ReactJS.

**Hạn chế hiện tại**: Nếu tự xây dựng backend từ đầu hoặc dùng framework quá tối giản, việc triển khai authentication, ORM, serializer, routing, admin và permission sẽ mất nhiều thời gian.

**Yêu cầu đồ án**: Hệ thống cần có backend rõ ràng, dễ mở rộng, dễ kiểm thử và phù hợp với mô hình web application.

**Bất kỳ ràng buộc nào**: Dự án cần hoàn thành theo phạm vi MVP, ưu tiên tính ổn định, dễ demo và dễ viết báo cáo.

---

## Quyết định

Chúng tôi quyết định sử dụng **Django REST Framework** làm framework chính để xây dựng Backend API.

Backend API sẽ xử lý các chức năng chính như quản lý project, upload source code, tạo scan job, theo dõi trạng thái scan, xem findings, xem AI report và quản lý knowledge base phục vụ RAG.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Flask

**Ưu điểm:**
- Nhẹ, đơn giản, dễ bắt đầu.

**Nhược điểm:**
- Cần tự cấu hình nhiều thành phần như authentication, admin, serializer và permission.
- Không thuận tiện bằng Django khi hệ thống có nhiều model và quan hệ dữ liệu.

### Tùy chọn 2: FastAPI

**Ưu điểm:**
- Hiệu năng tốt, hỗ trợ async tốt.
- Phù hợp cho AI service hoặc microservice.

**Nhược điểm:**
- Cần tự thiết kế nhiều phần quản trị dữ liệu.
- Với đồ án hiện tại, Django phù hợp hơn vì có ORM, Admin và cấu trúc app rõ ràng.

### Tùy chọn 3: Django REST Framework

**Ưu điểm:**
- Tích hợp tốt với Django ORM.
- Có sẵn Django Admin để kiểm tra dữ liệu nhanh.
- Phù hợp với hệ thống có nhiều bảng như User, Project, ScanJob, ScanFinding và AIReport.
- Dễ triển khai API CRUD bằng serializer, viewset và router.

**Nhược điểm:**
- Nặng hơn Flask hoặc FastAPI.
- Cần nắm rõ cấu trúc app, serializer, viewset và permission.

---

## Kết quả Quyết định

Django REST Framework được chọn vì phù hợp với yêu cầu phát triển backend có nhiều model, quan hệ dữ liệu và API quản lý. Framework này giúp rút ngắn thời gian phát triển, hỗ trợ tốt cho đồ án và dễ mở rộng sang các chức năng scanner, RAG và dashboard.

---

## Hậu quả

### Tích cực

- Tăng tốc độ phát triển backend.
- Dễ quản lý dữ liệu bằng Django ORM.
- Có Django Admin để kiểm tra dữ liệu trong quá trình demo.
- Dễ tổ chức code theo từng app như `projects`, `scans`, `findings`, `ai_agents` và `knowledge_base`.

### Tiêu cực

- Cần cấu hình tương đối nhiều ở giai đoạn đầu.
- Có thể dư tính năng nếu hệ thống chỉ là API nhỏ.

### Trung tính / Ghi chú

- Backend cần giữ cấu trúc đơn giản, tránh tạo quá nhiều app hoặc model không cần thiết.
- Các thông tin phụ nên lưu vào `metadata`, `raw_data` hoặc `report_json` để tránh database quá phức tạp.

---

## Tham khảo

- Django REST Framework Documentation
- Django Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-003, ADR-004
