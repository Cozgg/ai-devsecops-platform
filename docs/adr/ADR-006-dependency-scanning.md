# Bản ghi Quyết định Kiến trúc

---

## ADR-006: Sử dụng Trivy hoặc npm audit cho phân tích dependency

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Ngọc Anh Tú - Sinh viên thực hiện  
**Tags**: dependency, vulnerability, scanner

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Ngoài lỗi trong source code, project phần mềm còn có thể gặp rủi ro từ thư viện bên thứ ba. Các file như `package.json`, `package-lock.json`, `requirements.txt` hoặc `pyproject.toml` có thể chứa dependency bị lỗi bảo mật.

**Hạn chế hiện tại**: Nếu chỉ phân tích source code bằng Semgrep, hệ thống chưa bao phủ đầy đủ các rủi ro đến từ thư viện và package version.

**Yêu cầu đồ án**: Hệ thống cần thể hiện hướng DevSecOps bằng cách kiểm tra cả source code và dependency của project.

**Bất kỳ ràng buộc nào**: MVP cần ưu tiên công cụ dễ tích hợp, xuất được JSON và có thể chạy trong worker.

---

## Quyết định

Chúng tôi quyết định sử dụng **Trivy hoặc npm audit** để phân tích dependency vulnerability.

Trong MVP, hệ thống ưu tiên sử dụng `npm audit` cho project Node.js/ReactJS. Trivy có thể được tích hợp sau để phân tích dependency tổng quát hơn và hỗ trợ mở rộng sang container security.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Chỉ dùng Semgrep

**Ưu điểm:**
- Đơn giản, ít công cụ hơn.

**Nhược điểm:**
- Không bao phủ tốt các lỗ hổng dependency.
- Thiếu phần phân tích package vulnerability.

### Tùy chọn 2: npm audit

**Ưu điểm:**
- Có sẵn trong hệ sinh thái Node.js.
- Phù hợp với project JavaScript/ReactJS.
- Dễ chạy với `package.json` và `package-lock.json`.

**Nhược điểm:**
- Chủ yếu áp dụng cho npm project.
- Không phù hợp cho nhiều hệ sinh thái khác.

### Tùy chọn 3: Trivy

**Ưu điểm:**
- Hỗ trợ phân tích vulnerability cho dependency và container image.
- Phù hợp mở rộng DevSecOps.
- Có thể xuất JSON.

**Nhược điểm:**
- Cần thêm công cụ ngoài.
- Tích hợp có thể phức tạp hơn npm audit trong MVP.

---

## Kết quả Quyết định

Hệ thống sẽ hỗ trợ dependency scanning bằng npm audit hoặc Trivy. Trong giai đoạn đầu, có thể ưu tiên npm audit cho project JavaScript/Node.js, sau đó mở rộng Trivy để phân tích dependency đa dạng hơn và hỗ trợ container security.

---

## Hậu quả

### Tích cực

- Phát hiện được rủi ro từ thư viện bên thứ ba.
- Bổ sung cho Semgrep để phân tích bảo mật toàn diện hơn.
- Tăng giá trị DevSecOps của hệ thống.

### Tiêu cực

- Cần normalize thêm một loại output khác.
- Có thể có sự khác nhau về format giữa npm audit và Trivy.

### Trung tính / Ghi chú

- Các kết quả dependency scanning vẫn lưu chung vào `ScanFinding`.
- Trường `scanner_name` có thể là `semgrep`, `trivy` hoặc `npm_audit`.

---

## Tham khảo

- Trivy Documentation
- npm audit Documentation
- OWASP Dependency-Check concept

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-005
