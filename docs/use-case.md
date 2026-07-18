# Phân tích Use Case

Tài liệu này mô tả actor và các use case chính của **AI DevSecOps Platform** trong phạm vi MVP. Nội dung được đồng bộ theo sơ đồ use case vẽ bằng Astah, trong đó hệ thống tập trung vào hai nhóm người dùng chính: **User** và **Admin**.

---

## 1. Phạm vi use case MVP

Use case diagram ở giai đoạn MVP chỉ mô tả các chức năng mà người dùng tương tác trực tiếp với hệ thống.

Các thành phần kỹ thuật như **Semgrep**, **Trivy**, **npm audit**, **Celery Worker**, **Redis** hoặc **AI Model API** không được đưa thành actor chính trong sơ đồ use case này vì người dùng không thao tác trực tiếp với các thành phần đó. Những thành phần này được mô tả chi tiết hơn trong C4 Diagram, Sequence Diagram và Activity Diagram.

---

## 2. Actor

| Actor | Mô tả |
|---|---|
| User | Người dùng thông thường, có thể đăng nhập, quản lý project, upload source code, xem trạng thái scan và xem report của chính mình |
| Admin | Người quản trị hệ thống, kế thừa các chức năng của User và có thêm quyền quản lý người dùng, quản lý knowledge base |

Trong MVP, phân quyền Admin/User được triển khai dựa trên cơ chế mặc định của Django:

- Admin: `is_staff=True` hoặc `is_superuser=True`.
- User thường: `is_staff=False`, `is_superuser=False`.

Quan hệ giữa actor:

```text
Admin kế thừa User
```

Điều này có nghĩa là Admin có thể thực hiện các chức năng của User, đồng thời có thêm các chức năng quản trị.

---

## 3. Danh sách use case

| Mã use case | Tên use case | Actor chính | Mức ưu tiên MVP | Ghi chú |
|---|---|---|---|---|
| UC01 | Đăng nhập | Admin, User | Cao | Xác thực người dùng trước khi sử dụng hệ thống |
| UC02 | Quản lý project | User | Cao | Tạo, xem, cập nhật và xóa mềm project |
| UC03 | Upload source code | User | Cao | Upload file `.zip`; hệ thống tạo scan job ở phía backend |
| UC04 | Xem trạng thái | User | Cao | Theo dõi trạng thái scan job: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED` |
| UC05 | Xem report | User | Cao | Gộp xem kết quả phân tích và xem báo cáo AI |
| UC06 | Quản lý người dùng | Admin | Trung bình | Admin quản lý tài khoản người dùng qua trang quản trị |
| UC07 | Quản lý knowledge base | Admin | Trung bình | Admin quản lý tài liệu bảo mật phục vụ RAG |

---

## 4. Use Case Diagram

<img width="741" height="505" alt="image" src="https://github.com/user-attachments/assets/b18b8353-a6dc-4717-9a46-88104e0a3d6a" />

Ghi chú:

- `Xem report` trong sơ đồ được hiểu là bao gồm cả **xem kết quả phân tích scanner** và **xem báo cáo AI**.
- `Upload source code` là hành động người dùng nhìn thấy. Về mặt xử lý nội bộ, hệ thống sẽ lưu file upload và tạo `ScanJob` để xử lý bất đồng bộ.
- `Semgrep`, `Trivy`, `Celery Worker`, `Redis` và `AI Model API` không được thể hiện trong use case diagram này vì đây là các thành phần kỹ thuật nội bộ hoặc hệ thống phụ trợ.

---

## 5. Đặc tả use case quan trọng

### 5.1. UC01 - Đăng nhập

| Trường | Nội dung |
|---|---|
| Use case ID | UC01 |
| Tên use case | Đăng nhập |
| Actor chính | Admin, User |
| Actor phụ | Không có |
| Mô tả vắn tắt | Người dùng đăng nhập để sử dụng các chức năng của hệ thống |
| Tiền điều kiện | Người dùng đã có tài khoản trong hệ thống |
| Hậu điều kiện | Người dùng được xác thực và truy cập được các chức năng theo quyền |

**Luồng hoạt động chính:**

1. Người dùng truy cập trang đăng nhập.
2. Người dùng nhập thông tin tài khoản.
3. Hệ thống kiểm tra thông tin xác thực.
4. Nếu hợp lệ, hệ thống cho phép người dùng truy cập dashboard.
5. Hệ thống xác định quyền của người dùng dựa trên `is_staff` hoặc `is_superuser`.

**Luồng ngoại lệ:**

- Sai username hoặc password.
- Tài khoản không hoạt động.
- Người dùng chưa đăng nhập nhưng truy cập API yêu cầu xác thực.

---

### 5.2. UC02 - Quản lý project

| Trường | Nội dung |
|---|---|
| Use case ID | UC02 |
| Tên use case | Quản lý project |
| Actor chính | User |
| Actor phụ | Admin |
| Mô tả vắn tắt | Người dùng tạo và quản lý project source code của mình |
| Tiền điều kiện | Người dùng đã đăng nhập |
| Hậu điều kiện | Project được tạo, cập nhật hoặc xóa mềm trong hệ thống |

**Luồng hoạt động chính:**

1. User truy cập trang quản lý project.
2. Hệ thống hiển thị danh sách project thuộc về user.
3. User nhập thông tin project mới.
4. Hệ thống kiểm tra dữ liệu đầu vào.
5. Hệ thống tạo project và gán `owner` là user hiện tại.
6. Hệ thống trả về thông tin project vừa tạo.

**Luồng thay thế:**

- User cập nhật tên hoặc mô tả project.
- User xóa project. Hệ thống thực hiện soft delete bằng `active=False`.
- Admin có thể xem hoặc kiểm tra project trong phạm vi quản trị hệ thống.

**Luồng ngoại lệ:**

- User chưa đăng nhập.
- Dữ liệu không hợp lệ.
- User truy cập project không thuộc quyền sở hữu của mình.

---

### 5.3. UC03 - Upload source code

| Trường | Nội dung |
|---|---|
| Use case ID | UC03 |
| Tên use case | Upload source code |
| Actor chính | User |
| Actor phụ | Không thể hiện trực tiếp trong use case diagram |
| Mô tả vắn tắt | User upload source code dạng `.zip` để hệ thống tạo scan job và xử lý phân tích mã nguồn |
| Tiền điều kiện | User đã đăng nhập và đã có project |
| Hậu điều kiện | File source code được lưu và `ScanJob` được tạo với trạng thái `PENDING` |

**Luồng hoạt động chính:**

1. User chọn project cần scan.
2. User upload source code dạng `.zip`.
3. Backend API kiểm tra quyền truy cập project.
4. Backend API kiểm tra định dạng file upload.
5. Backend API lưu file vào `MEDIA_ROOT`.
6. Backend API tạo `ScanJob` với trạng thái `PENDING`.
7. Hệ thống trả về `scan_job_id` cho user.
8. Sau đó, Celery Worker sẽ xử lý scan job ở background.

**Luồng thay thế:**

- Nếu chưa tích hợp Celery Worker, hệ thống chỉ tạo `ScanJob(PENDING)` để kiểm thử upload API.
- Nếu hệ thống đã tích hợp worker, scan job sẽ được đẩy vào queue để xử lý bất đồng bộ.

**Luồng ngoại lệ:**

- File không đúng định dạng `.zip`.
- User chưa chọn project.
- User không có quyền truy cập project.
- File upload vượt quá giới hạn dung lượng.
- Lỗi lưu file hoặc lỗi tạo scan job.

---

### 5.4. UC04 - Xem trạng thái

| Trường | Nội dung |
|---|---|
| Use case ID | UC04 |
| Tên use case | Xem trạng thái |
| Actor chính | User |
| Actor phụ | Không có |
| Mô tả vắn tắt | User xem trạng thái hiện tại của scan job sau khi upload source code |
| Tiền điều kiện | User đã tạo scan job hoặc có quyền xem scan job |
| Hậu điều kiện | User biết scan job đang chờ, đang chạy, hoàn tất hay thất bại |

**Luồng hoạt động chính:**

1. User mở chi tiết scan job.
2. Frontend gọi API lấy trạng thái scan job.
3. Backend kiểm tra quyền truy cập scan job.
4. Backend trả về trạng thái hiện tại: `PENDING`, `RUNNING`, `COMPLETED` hoặc `FAILED`.
5. Frontend hiển thị trạng thái cho user.

**Luồng ngoại lệ:**

- Scan job không tồn tại.
- User không có quyền xem scan job.
- Scan job bị lỗi và có `error_message`.

---

### 5.5. UC05 - Xem report

| Trường | Nội dung |
|---|---|
| Use case ID | UC05 |
| Tên use case | Xem report |
| Actor chính | User |
| Actor phụ | Không thể hiện trực tiếp trong use case diagram |
| Mô tả vắn tắt | User xem kết quả phân tích mã nguồn và báo cáo AI sau khi scan hoàn tất |
| Tiền điều kiện | Scan job đã hoàn tất hoặc đã có dữ liệu phân tích |
| Hậu điều kiện | User xem được danh sách rủi ro, mức độ nghiêm trọng, tổng quan rủi ro và gợi ý khắc phục |

**Luồng hoạt động chính:**

1. User mở trang report của scan job.
2. Frontend gọi API lấy kết quả phân tích.
3. Backend kiểm tra quyền truy cập scan job.
4. Backend trả về danh sách findings nếu đã có.
5. Backend trả về AI report nếu đã được sinh.
6. Frontend hiển thị report gồm findings, severity, file path, dòng code, summary, risk overview và recommendation.

**Luồng thay thế:**

- Nếu chỉ có findings nhưng chưa có AI report, hệ thống vẫn hiển thị findings trước.
- Nếu không phát hiện lỗi, hệ thống hiển thị report với trạng thái không có finding nghiêm trọng.

**Luồng ngoại lệ:**

- Scan job chưa hoàn tất.
- Report chưa được sinh.
- User không có quyền xem scan job.
- Lỗi trong quá trình sinh báo cáo AI.

---

### 5.6. UC06 - Quản lý người dùng

| Trường | Nội dung |
|---|---|
| Use case ID | UC06 |
| Tên use case | Quản lý người dùng |
| Actor chính | Admin |
| Actor phụ | Không có |
| Mô tả vắn tắt | Admin quản lý tài khoản người dùng trong hệ thống |
| Tiền điều kiện | Admin đã đăng nhập |
| Hậu điều kiện | Thông tin người dùng được xem, tạo, cập nhật hoặc vô hiệu hóa theo quyền quản trị |

**Luồng hoạt động chính:**

1. Admin truy cập trang quản trị người dùng.
2. Hệ thống hiển thị danh sách người dùng.
3. Admin xem thông tin chi tiết người dùng.
4. Admin tạo, cập nhật hoặc vô hiệu hóa tài khoản nếu cần.
5. Hệ thống lưu thay đổi.

**Luồng ngoại lệ:**

- Người thao tác không phải Admin.
- Dữ liệu người dùng không hợp lệ.
- Tài khoản cần cập nhật không tồn tại.

---

### 5.7. UC07 - Quản lý knowledge base

| Trường | Nội dung |
|---|---|
| Use case ID | UC07 |
| Tên use case | Quản lý knowledge base |
| Actor chính | Admin |
| Actor phụ | RAG Service |
| Mô tả vắn tắt | Admin thêm và quản lý tài liệu bảo mật dùng cho RAG |
| Tiền điều kiện | Admin đã đăng nhập |
| Hậu điều kiện | KnowledgeDocument và KnowledgeChunk được tạo hoặc cập nhật |

**Luồng hoạt động chính:**

1. Admin truy cập trang quản lý knowledge base.
2. Admin thêm tài liệu mới như OWASP, CWE, tài liệu scanner hoặc ghi chú nội bộ.
3. Hệ thống lưu `KnowledgeDocument`.
4. Hệ thống tách tài liệu thành nhiều `KnowledgeChunk`.
5. RAG Service sử dụng các chunk này để truy xuất context khi sinh report.

**Luồng thay thế:**

- Admin cập nhật hoặc vô hiệu hóa một tài liệu cũ.
- Admin phân loại tài liệu theo `source_type` hoặc `category`.

**Luồng ngoại lệ:**

- Nội dung tài liệu rỗng.
- Admin nhập sai loại `source_type`.
- Người thao tác không có quyền Admin.

---

## 6. Ghi chú đồng bộ với các tài liệu khác

- Luồng `Upload source code -> Xem trạng thái -> Xem report` là luồng nghiệp vụ chính của hệ thống.
- Chi tiết xử lý kỹ thuật của scanner, queue, worker và AI report được mô tả trong `docs/diagrams.md` bằng Sequence Diagram và Activity Diagram.
- Thiết kế database liên quan đến các use case này được mô tả trong `docs/database-design.md`.
- Kiến trúc tổng thể của các thành phần kỹ thuật được mô tả trong `docs/C4.md`.
