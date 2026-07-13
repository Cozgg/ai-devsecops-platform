# Bản ghi Quyết định Kiến trúc

---

## ADR-007: Sử dụng LangChain và RAG cho AI Report

**Trạng thái**: Đã chấp nhận  
**Ngày**: 2026-07-13  
**Người quyết định**: Nguyễn Hữu Công - Sinh viên thực hiện  
**Tags**: ai, rag, langchain, report

---

## Ngữ cảnh

**Vấn đề kỹ thuật**: Kết quả từ scanner thường mang tính kỹ thuật và khó hiểu với người dùng chưa có nhiều kinh nghiệm bảo mật. Hệ thống cần giải thích findings, đánh giá mức độ ảnh hưởng và gợi ý hướng khắc phục.

**Hạn chế hiện tại**: Nếu chỉ hiển thị raw scanner result, người dùng phải tự đọc rule, severity và file lỗi. Nếu gọi trực tiếp AI model mà không có tài liệu tham chiếu, báo cáo có thể thiếu căn cứ hoặc không nhất quán.

**Yêu cầu đồ án**: Hệ thống cần có AI Agent hỗ trợ phân tích kết quả scan và sinh báo cáo dễ hiểu dựa trên dữ liệu findings và knowledge base.

**Bất kỳ ràng buộc nào**: MVP không train LLM từ đầu. Hệ thống ưu tiên dùng RAG để bổ sung ngữ cảnh cho AI report.

---

## Quyết định

Chúng tôi quyết định sử dụng **LangChain kết hợp RAG** để xây dựng AI Report Service.

RAG sẽ truy xuất thông tin liên quan từ knowledge base như OWASP, CWE, tài liệu scanner hoặc ghi chú nội bộ. LangChain sẽ hỗ trợ xây dựng pipeline gồm retrieval, prompt construction và gọi AI model để sinh báo cáo.

---

## Các Tùy chọn Đã Xem xét

### Tùy chọn 1: Không dùng AI

**Ưu điểm:**
- Đơn giản.
- Không phụ thuộc vào AI model.

**Nhược điểm:**
- Người dùng phải tự đọc findings kỹ thuật.
- Không thể hiện rõ yếu tố AI Agent trong đề tài.

### Tùy chọn 2: Gọi trực tiếp AI model không dùng RAG

**Ưu điểm:**
- Dễ triển khai hơn.
- Không cần xây knowledge base.

**Nhược điểm:**
- Kết quả có thể thiếu căn cứ.
- Khó kiểm soát nội dung trả lời.
- Không tận dụng được tài liệu bảo mật riêng của hệ thống.

### Tùy chọn 3: LangChain + RAG

**Ưu điểm:**
- Có thể kết hợp findings với tài liệu bảo mật liên quan.
- Giúp AI report có ngữ cảnh hơn.
- Dễ mở rộng sang agent workflow sau này.
- Phù hợp với mục tiêu đồ án về AI Agent.

**Nhược điểm:**
- Tăng độ phức tạp.
- Cần xây dựng KnowledgeDocument và KnowledgeChunk.
- Cần thiết kế prompt cẩn thận.

---

## Kết quả Quyết định

LangChain và RAG được chọn để sinh AI report từ findings. Hệ thống sẽ lấy findings, detected stack và knowledge base liên quan để tạo prompt, sau đó gọi AI model và lưu kết quả vào `AIReport`.

---

## Hậu quả

### Tích cực

- Báo cáo dễ hiểu hơn so với raw scanner result.
- Có thể giải thích lỗi theo ngữ cảnh.
- Có thể tham chiếu tài liệu bảo mật.
- Tăng tính học thuật và kỹ thuật cho đồ án.

### Tiêu cực

- Cần quản lý API key hoặc cấu hình AI model.
- Kết quả AI có thể chưa hoàn toàn chính xác.
- Cần kiểm soát prompt để tránh trả lời lan man.

### Trung tính / Ghi chú

- MVP có thể bắt đầu bằng keyword-based retrieval trước.
- Sau này có thể nâng cấp sang embedding và pgvector.
- Không train LLM từ đầu trong phạm vi MVP.

---

## Tham khảo

- LangChain Documentation
- RAG pattern
- OWASP Top 10
- CWE

---

## Ghi chú

---

**Cập nhật lần cuối**: 2026-07-13  
**ADRs Liên quan**: ADR-003, ADR-005
