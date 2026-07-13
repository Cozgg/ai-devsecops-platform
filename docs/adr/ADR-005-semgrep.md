# Bản ghi Quyết định Kiến trúc

---

## ADR-005: Sử dụng Semgrep cho phân tích mã nguồn tĩnh

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Ngọc Anh Tú - Sinh viên thực hiện  
**Tags**: scanner, sast, security

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Hệ thống cần phát hiện rủi ro trong source code như lỗi bảo mật, cấu hình không an toàn, hardcoded secret hoặc các pattern code nguy hiểm.

**Hạn chế hiện tại**: Việc tự xây dựng scanner từ đầu sẽ tốn nhiều thời gian và khó đảm bảo độ chính xác trong phạm vi đồ án.

**Yêu cầu đồ án**: Hệ thống cần có chức năng phân tích mã nguồn và tạo findings để AI Agent có dữ liệu đầu vào cho quá trình giải thích, đánh giá và gợi ý khắc phục.

**Bất kỳ ràng buộc nào**: MVP ưu tiên tích hợp scanner có sẵn, xuất được JSON và chạy được trong worker.

---

## Quyết định

Chúng tôi quyết định sử dụng **Semgrep** làm công cụ phân tích mã nguồn tĩnh trong hệ thống.

Celery Worker sẽ gọi Semgrep CLI để scan source code đã upload. Kết quả Semgrep trả về dạng JSON sẽ được hệ thống chuẩn hóa và lưu thành `ScanFinding`.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Tự xây scanner

**Ưu điểm:**
- Có thể tùy chỉnh hoàn toàn theo ý muốn.

**Nhược điểm:**
- Rất khó triển khai chính xác.
- Tốn nhiều thời gian.
- Không phù hợp với phạm vi đồ án MVP.

### Tùy chọn 2: Bandit

**Ưu điểm:**
- Phù hợp với Python.
- Dễ dùng cho project Python.

**Nhược điểm:**
- Chủ yếu tập trung vào Python.
- Không đủ linh hoạt nếu hệ thống cần hỗ trợ thêm JavaScript/Node.js.

### Tùy chọn 3: Semgrep

**Ưu điểm:**
- Hỗ trợ nhiều ngôn ngữ.
- Phù hợp phân tích mã nguồn tĩnh.
- Có thể xuất kết quả JSON.
- Dễ tích hợp vào worker bằng CLI.
- Có nhiều rule bảo mật sẵn có.

**Nhược điểm:**
- Kết quả có thể có false positive.
- Cần normalize kết quả trước khi lưu vào database.

---

## Kết quả Quyết định

Semgrep được chọn làm scanner chính cho source code. Hệ thống không thay thế Semgrep mà sử dụng Semgrep như scanner engine, sau đó bổ sung các bước normalize findings, risk scoring và AI explanation bằng LangChain/RAG.

---

## Hậu quả

### Tích cực

- Không cần tự xây scanner từ đầu.
- Có thể phát hiện nhiều rủi ro source code phổ biến.
- Kết quả JSON dễ xử lý.
- Phù hợp với kiến trúc scan job.

### Tiêu cực

- Cần cài Semgrep trong môi trường worker.
- Cần xử lý false positive.
- Cần ánh xạ severity/rule từ Semgrep sang format riêng của hệ thống.

### Trung tính / Ghi chú

- MVP sẽ chạy Semgrep ở chế độ static scan, không thực thi source code người dùng.
- Các thông tin chi tiết như rule ID, CWE, OWASP nếu có sẽ lưu vào `ScanFinding.raw_data`.

---

## Tham khảo

- Semgrep Documentation
- OWASP Top 10
- CWE

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-004, ADR-007
