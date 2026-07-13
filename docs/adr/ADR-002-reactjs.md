# Bản ghi Quyết định Kiến trúc

---

## ADR-002: Sử dụng ReactJS cho Frontend

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Ngọc Anh Tú - Sinh viên thực hiện  
**Tags**: frontend, ui, web

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Hệ thống cần giao diện web để người dùng tạo project, upload source code, theo dõi trạng thái scan, xem findings và đọc AI report.

**Hạn chế hiện tại**: Nếu dùng HTML/CSS/JavaScript thuần, việc quản lý trạng thái, chia component và mở rộng dashboard sẽ khó hơn khi số lượng màn hình tăng lên.

**Yêu cầu đồ án**: Frontend cần dễ demo, dễ kết nối với REST API và thể hiện được luồng nghiệp vụ chính của hệ thống.

**Bất kỳ ràng buộc nào**: MVP ưu tiên giao diện rõ chức năng hơn là thiết kế quá phức tạp.

---

## Quyết định

Chúng tôi quyết định sử dụng **ReactJS** để xây dựng frontend dashboard cho hệ thống.

Frontend sẽ cung cấp các màn hình chính như đăng nhập/đăng ký, danh sách project, chi tiết project, upload source code, danh sách scan job, bảng findings và trang AI report.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: HTML/CSS/JavaScript thuần

**Ưu điểm:**
- Đơn giản, không cần nhiều thư viện.

**Nhược điểm:**
- Khó quản lý state khi giao diện có nhiều màn hình.
- Khó mở rộng dashboard.

### Tùy chọn 2: VueJS

**Ưu điểm:**
- Dễ học, cấu trúc rõ ràng.

**Nhược điểm:**
- Dự án ưu tiên ReactJS do phổ biến, dễ tìm tài liệu và phù hợp với định hướng frontend dashboard.

### Tùy chọn 3: ReactJS

**Ưu điểm:**
- Phổ biến, cộng đồng lớn.
- Phù hợp xây dựng dashboard.
- Dễ kết nối REST API.
- Có nhiều thư viện UI hỗ trợ.

**Nhược điểm:**
- Cần quản lý component và state hợp lý.
- Nếu không kiểm soát tốt, frontend dễ bị rối.

---

## Kết quả Quyết định

ReactJS được chọn để xây dựng giao diện người dùng vì phù hợp với dashboard web, dễ kết nối với Django REST API và thuận tiện khi mở rộng thêm các màn hình theo dõi scan, findings và AI report.

---

## Hậu quả

### Tích cực

- Giao diện linh hoạt, dễ chia component.
- Phù hợp với frontend dạng dashboard.
- Dễ tích hợp bảng dữ liệu, form upload và trang báo cáo.

### Tiêu cực

- Cần thêm bước build frontend.
- Cần cấu hình CORS giữa frontend và backend.

### Trung tính / Ghi chú

- MVP frontend chỉ cần rõ chức năng, chưa cần quá đẹp.
- Ưu tiên hoàn thành backend API trước khi làm frontend.

---

## Tham khảo

- React Documentation
- Django REST Framework Documentation

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-001
