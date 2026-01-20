# Hướng Dẫn Public Website "Toán Vui Cho Bé"

Tài liệu này sẽ hướng dẫn bạn đưa website từ máy tính cá nhân lên mạng Internet để ai cũng có thể truy cập được.

Chúng ta sẽ sử dụng bộ 3 dịch vụ "Miễn Phí & Ngon" nhất hiện nay:
1.  **MongoDB Atlas**: Chứa cơ sở dữ liệu (Cloud).
2.  **Render.com**: Chạy Backend (Python FastAPI).
3.  **Vercel**: Chạy Frontend (Giao diện web).

---

## Bước 1: Chuẩn bị Github
Đảm bảo mã nguồn dự án của bạn đã được đẩy lên **GitHub**.
Nếu chưa, hãy tạo repository mới và push toàn bộ code lên đó (bao gồm thư mục `backend` và `frontend`).

---

## Bước 2: Tạo Database trên MongoDB Atlas (Nếu chưa có)
Vì khi chạy online, backend không thể kết nối tới máy tính local của bạn, nên ta cần một Database trên mây.

1.  Truy cập [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) và đăng nhập.
2.  Tạo một **Cluster** mới (chọn gói **M0 FREE**).
3.  Trong phần **Network Access**, chọn "Allow Access from Anywhere" (0.0.0.0/0) để server Render có thể kết nối vào.
4.  Trong phần **Database Access**, tạo một user mới (ví dụ: `simon_admin`) và nhớ mật khẩu.
5.  Lấy chuỗi kết nối (Connection String):
    *   Nhấn **Connect** -> **Connect your application**.
    *   Copy chuỗi dạng: `mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/?retryWrites=true&w=majority`
    *   Thay `<username>` và `<password>` bằng thông tin bạn vừa tạo.
    *   **Lưu chuỗi này lại**, chúng ta sẽ cần nó ở Bước 3.

---

## Bước 3: Deploy Backend lên Render.com

1.  Truy cập [Render.com](https://render.com/) và đăng nhập bằng tài khoản GitHub.
2.  Nhấn **New +** -> **Web Service**.
3.  Chọn repository GitHub **simon**.
4.  Điền các thông tin sau:
    *   **Name**: `simon-backend` (hoặc tên tùy thích).
    *   **Region**: Singapore (cho gần Việt Nam).
    *   **Root Directory**: `backend` (Rất quan trọng! Vì code python nằm trong thư mục này).
    *   **Environment**: Python 3.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
    *   **Instance Type**: Free.
5.  Kéo xuống phần **Environment Variables**, bấm **Add Environment Variable** để thêm các biến sau:
    *   `MONGODB_URI`: Dán chuỗi kết nối MongoDB Atlas ở Bước 2 vào đây.
    *   `MONGODB_DB_NAME`: `simon_math`
    *   `JWT_SECRET_KEY`: (Copy key trong file .env local hoặc tạo key mới bất kỳ).
    *   `PYTHON_VERSION`: `3.9.0` (Hoặc phiên bản python bạn muốn, Render mặc định hỗ trợ 3.7+).
6.  Nhấn **Create Web Service**.

⏳ Chờ khoảng vài phút để Render cài đặt và khởi động. Khi nào thấy dấu tick xanh ✅ và chữ **Live** là thành công.
Copy URL của backend vừa tạo (ví dụ: `https://simon-backend.onrender.com`).

---

## Bước 4: Cập nhật Frontend và Deploy lên Vercel

### 4.1 Cập nhật URL Backend
1.  Quay lại VS Code trên máy.
2.  Mở file `frontend/js/api.js`.
3.  Tìm dòng `const PRODUCTION_API_URL = ...`
4.  Thay thế URL giả bằng URL thật bạn vừa copy từ Render (nhớ thêm `/api` ở cuối).
    *   Ví dụ: `const PRODUCTION_API_URL = 'https://simon-backend.onrender.com/api';`
5.  **Quan trọng:** Commit và Push thay đổi này lên GitHub.

### 4.2 Deploy lên Vercel
1.  Truy cập [Vercel.com](https://vercel.com/) và đăng nhập bằng GitHub.
2.  Nhấn **Add New...** -> **Project**.
3.  Import repository GitHub **simon**.
4.  Trong phần cài đặt **Build & Output Settings**:
    *   **Root Directory**: Nhấn Edit và chọn thư mục `frontend`. (Quan trọng: Vì ta chỉ muốn deploy folder frontend).
5.  Nhấn **Deploy**.

⏳ Vercel chạy cực nhanh, chỉ mất khoảng 30 giây là xong.
Sau khi xong, Vercel sẽ cấp cho bạn một tên miền (ví dụ: `simon-math.vercel.app`).

---

## Bước 5: Tận hưởng
Truy cập vào tên miền Vercel cấp. Bây giờ bạn có thể gửi link này cho mọi người, cho bé dùng trên iPad, điện thoại thoải mái mà không cần bật máy tính của bạn nữa!

Chúc bạn thành công! 🚀
