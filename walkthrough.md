# Hướng dẫn Kiểm tra và Chạy Dự án "Toán Vui Cho Bé" (FastAPI + MongoDB Local)

Tài liệu này sẽ hướng dẫn bạn từng bước để kiểm tra, cài đặt môi trường và chạy dự án.

## 1. Kiểm tra Môi trường (Prerequisites)

Dự án yêu cầu cài đặt **Python** (phiên bản 3.9 trở lên) và **MongoDB** trên máy local.

### Bước 1: Kiểm tra Python
Mở **Windows Search** (phím Windows + S), gõ `cmd` và mở **Command Prompt**. Gõ lệnh sau:
```bash
py --version
```
*   Nếu hiện ra phiên bản (ví dụ `Python 3.11.x`), bạn đã sẵn sàng.

### Bước 2: Kiểm tra MongoDB đang chạy
Mở **MongoDB Compass** và kiểm tra kết nối tới `mongodb://localhost:27017`. Nếu kết nối thành công, MongoDB đã sẵn sàng.

Hoặc mở Command Prompt và gõ:
```bash
mongosh
```
Nếu thấy MongoDB shell mở ra, MongoDB đang chạy tốt.

## 2. Cấu hình Backend

### Bước 1: Tạo file .env
1. Mở thư mục `backend` trong dự án
2. Copy file `.env.example` thành `.env`:
   ```bash
   copy .env.example .env
   ```
3. Mở file `.env` và thay đổi `JWT_SECRET_KEY`:
   - Tạo secret key bằng Python:
     ```bash
     py -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
   - Copy kết quả và thay thế vào `JWT_SECRET_KEY` trong file `.env`

## 3. Cài đặt Thư viện Backend

1.  Mở thư mục dự án trong terminal (hoặc VS Code).
2.  Di chuyển vào thư mục backend:
    ```bash
    cd backend
    ```
3.  Cài đặt các gói thư viện cần thiết:
    ```bash
    py -m pip install -r requirements.txt
    ```

## 4. Khởi động Backend Server

Tại thư mục `backend`, chạy lệnh:
```bash
py -m uvicorn app.main:app --reload --port 5000
```
Hoặc nếu chạy trực tiếp file main (nếu có cấu hình):
```bash
py app/main.py
```

Nếu thành công, bạn sẽ thấy thông báo server đang chạy, thường là tại `http://127.0.0.1:5000`.

**Kiểm tra nhanh API:**
Mở trình duyệt và truy cập: [http://localhost:5000/docs](http://localhost:5000/docs)
Bạn sẽ thấy trang Swagger UI hiển thị danh sách các API (Auth, Quiz). Điều này chứng tỏ Backend đã hoạt động.

## 5. Chạy Frontend

1.  Mở thư mục `frontend` trong VS Code.
### Cách 1: Sử dụng Live Server (VS Code Extension)
1.  Click chuột phải vào file `index.html`.
2.  Chọn **"Open with Live Server"**. (Lưu ý: Port mặc định của Live Server là 5500, nhưng mã nguồn đã cấu hình để frontend chạy ở port nào cũng gọi được API port 5000).

### Cách 2: Sử dụng Python HTTP Server (Khuyên dùng nếu không có VS Code Extensions)
1.  Mở terminal tại thư mục `frontend`:
    ```bash
    cd frontend
    ```
2.  Chạy lệnh:
    ```bash
    py -m http.server 8000
    ```
3.  Mở trình duyệt: [http://localhost:8000](http://localhost:8000)

**LƯU Ý QUAN TRỌNG:** Không mở trực tiếp file bằng cách double-click (đường dẫn `file:///...`) vì trình duyệt sẽ chặn gọi API do chính sách bảo mật (CORS/URL Protocol). Bắt buộc phải chạy qua localhost.

## 6. Quy trình Kiểm tra Chức năng (End-to-End Testing)

Hãy thực hiện các bước sau trên giao diện web để đảm bảo mọi thứ hoạt động trơn tru:

1.  **Đăng ký tài khoản mới:**
    *   Nhấn nút **Login** (hoặc Đăng nhập) góc phải trên.
    *   Chọn "Đăng ký ngay".
    *   Nhập tên bé, email và mật khẩu.
    *   Nhấn Đăng ký.
    *   *Kỳ vọng*: Thông báo thành công, modal đóng lại, và trên thanh menu hiện tên của bé (ví dụ: "Bé Bi").

2.  **Làm bài kiểm tra:**
    *   Chọn một bài tập (ví dụ: Cộng Trừ).
    *   Nhấn **Bắt đầu**.
    *   Làm vài câu hỏi và nhấn **Nộp bài**.
    *   *Kỳ vọng*: Kết quả hiện ra, có số sao và điểm số. Dữ liệu này sẽ được lưu vào MongoDB local.

3.  **Kiểm tra Lưu trữ:**
    *   Reload lại trang web (F5).
    *   *Kỳ vọng*: Bạn vẫn đang ở trạng thái đăng nhập (tên bé vẫn hiện).
    *   Vào mục **Lịch sử** (trong bài tập vừa làm).
    *   *Kỳ vọng*: Thấy dòng lịch sử bài làm vừa rồi.

4.  **Kiểm tra Database trong MongoDB Compass:**
    *   Mở MongoDB Compass
    *   Kết nối tới `mongodb://localhost:27017`
    *   Bạn sẽ thấy database `simon_math` xuất hiện với các collections: `users`, `quiz_results`

## 7. Xử lý sự cố thường gặp

*   **Lỗi kết nối MongoDB**: 
    - Kiểm tra MongoDB service có đang chạy không (mở MongoDB Compass hoặc gõ `mongosh`)
    - Đảm bảo `MONGODB_URI` trong file `.env` là `mongodb://localhost:27017`
    - Nếu MongoDB có authentication, cập nhật connection string: `mongodb://username:password@localhost:27017`
*   **Database chưa xuất hiện**: Database `simon_math` sẽ tự động được tạo khi có dữ liệu đầu tiên (sau khi đăng ký user đầu tiên)
*   **Lỗi CORS**: Nếu frontend không gọi được API, kiểm tra console log (F12) xem có lỗi CORS đỏ không. Backend đã cấu hình CORS, nhưng cần đảm bảo `allow_origins=["*"]` trong `main.py`.

Chúc bạn có trải nghiệm vui vẻ với ứng dụng!
