# Hướng Dẫn Public Website "Toán Vui Cho Bé" trên Server Riêng (VPS)

Tài liệu này hướng dẫn bạn triển khai ứng dụng trên máy chủ riêng (VPS/Dedicated Server) đã cài sẵn MongoDB và có tên miền.

Giả định:
- Hệ điều hành Server: **Linux (Ubuntu/CentOS)** hoặc **Windows Server**.
- Đã cài đặt **Python 3.9+**.
- Đã cài đặt **MongoDB**.
- Đã có tên miền (ví dụ: `toanvuichobe.com`).

---

## 1. Kiến trúc Triển khai
Chúng ta sẽ sử dụng mô hình sau:
- **Nginx**: Làm Web Server chính.
    - Phục vụ file Frontend (HTML/CSS/JS) tại `/`.
    - Reverse Proxy các request `/api` tới Backend đang chạy ở port 5000.
- **Backend**: Chạy dưới dạng Service (systemd hoặc nssm) tại `localhost:5000`.
- **Database**: MongoDB chạy tại `localhost:27017`.

---

## 2. Setup Backend trên Server

1.  **Copy mã nguồn**: Upload thư mục `backend` lên server (ví dụ tại `/var/www/simon/backend`).
2.  **Cài đặt môi trường**:
    ```bash
    cd /var/www/simon/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Cấu hình .env**:
    - Tạo file `.env` từ `.env.example`.
    - `MONGODB_URI=mongodb://localhost:27017` (Vì Mongo chạy ngay trên server này).
    - `JWT_SECRET_KEY`: (Điền key bảo mật).

4.  **Chạy thử**:
    ```bash
    python -m uvicorn app.main:app --port 5000
    ```
    Nếu chạy ok thì tắt đi và cấu hình chạy ngầm (Daemon).

5.  **Cấu hình chạy ngầm (Systemd - Linux)**:
    - Tạo file `/etc/systemd/system/simon-backend.service`:
      ```ini
      [Unit]
      Description=Simon Math API
      After=network.target

      [Service]
      User=root
      WorkingDirectory=/var/www/simon/backend
      Environment="PATH=/var/www/simon/backend/venv/bin"
      ExecStart=/var/www/simon/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 5000
      Restart=always

      [Install]
      WantedBy=multi-user.target
      ```
    - Start service:
      ```bash
      sudo systemctl enable simon-backend
      sudo systemctl start simon-backend
      ```

---

## 3. Setup Frontend & Nginx

1.  **Copy mã nguồn**: Upload thư mục `frontend` lên server (ví dụ tại `/var/www/simon/frontend`).
2.  **Cấu hình API URL**:
    - Mở file `/var/www/simon/frontend/js/api.js`.
    - Sửa dòng `const PRODUCTION_API_URL` thành:
      ```javascript
      // Vì dùng Nginx proxy cùng domain, ta chỉ cần trỏ về /api
      const PRODUCTION_API_URL = '/api'; 
      ```
      *(Lưu ý: Nếu cấu hình Nginx chuẩn như dưới đây, frontend sẽ tự hiểu gọi vào chính domain hiện tại)*

3.  **Cấu hình Nginx**:
    - Tạo config file (ví dụ `/etc/nginx/sites-available/simon`):
      ```nginx
      server {
          listen 80;
          server_name toanvuichobe.com www.toanvuichobe.com;

          # Frontend (Static Files)
          location / {
              root /var/www/simon/frontend;
              index index.html;
              try_files $uri $uri/ /index.html;
              add_header Cache-Control "no-cache";
          }

          # Backend API (Reverse Proxy)
          location /api {
              proxy_pass http://127.0.0.1:5000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
          }
      }
      ```
    - Kích hoạt và Restart Nginx:
      ```bash
      sudo ln -s /etc/nginx/sites-available/simon /etc/nginx/sites-enabled/
      sudo systemctl restart nginx
      ```

---

## 4. Kiểm tra
1.  Truy cập website: `http://toanvuichobe.com`.
2.  Thử đăng ký/đăng nhập. Yêu cầu sẽ đi từ `Browser` -> `Nginx (port 80)` -> `Proxy /api` -> `Backend (port 5000)` -> `MongoDB`.

Chúc mừng bạn đã làm chủ hoàn toàn hệ thống! 🎉
