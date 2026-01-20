# Implementation Plan: FastAPI + MongoDB Cloud Web Application

## Tổng quan

Xây dựng backend Python **FastAPI** (high performance) với **MongoDB Cloud** để hỗ trợ ứng dụng "Toán Vui Cho Bé". Hệ thống sử dụng kiến trúc bất đồng bộ (Async/Await) và xác thực người dùng qua JWT.

## User Review Required

> [!IMPORTANT]
> **MongoDB Cloud**: Chúng ta sẽ không chạy MongoDB container local nữa. Bạn cần cung cấp Connection String từ MongoDB Atlas (Cloud) vào file `.env`.

> [!NOTE]
> **API Documentation**: FastAPI tự động tạo docs tại `/docs` (Swagger UI), rất tiện lợi cho việc kiểm thử API.

## Proposed Changes

### Infrastructure & Configuration

#### [MODIFY] [docker-compose.yml](file:///e:/GitHub/simon/docker-compose.yml)
- **Remove**: MongoDB service (dùng Cloud).
- **Service `backend`**: Chạy với command uvicorn (dev mode).
- **Service `frontend`**: Serve static files (nginx hoặc simple server).

#### [MODIFY] [.env](file:///e:/GitHub/simon/.env)
- `MONGODB_URL`: Connection string tới MongoDB Atlas.
- `JWT_SECRET_KEY`: Khóa bí mật cho token.
- `JWT_ALGORITHM`: `HS256`.

---

### Backend Application (FastAPI)

#### [MODIFY] [backend/requirements.txt](file:///e:/GitHub/simon/backend/requirements.txt)
- `fastapi`, `uvicorn`: Core framework & server.
- `motor`: Async MongoDB driver.
- `pydantic`, `pydantic-settings`: Data validation & settings.
- `python-jose[cryptography]`, `passlib[bcrypt]`: Auth & Security.
- `python-multipart`: Form handling.

#### [Structure] Cấu trúc Backend
- `app/main.py`: Entry point, CORS, Exception handlers.
- `app/config.py`: Load env settings với Pydantic.
- `app/utils/deps.py`: Dependency Injection (Get current user, DB connection).

#### [NEW/MODIFY] [backend/app/schemas/](file:///e:/GitHub/simon/backend/app/schemas/)
Pydantic models để validate request/response:
- `user.py`: `UserCreate`, `UserLogin`, `UserResponse`.
- `quiz.py`: `QuizSubmit`, `QuizHistory`.

#### [NEW/MODIFY] [backend/app/models/](file:///e:/GitHub/simon/backend/app/models/)
Logic tương tác database (Motor):
- `user.py`: CRUD operations cho User.
- `quiz.py`: CRUD operations cho Quiz result.

#### [MODIFY] [backend/app/routes/](file:///e:/GitHub/simon/backend/app/routes/)
- `auth.py`: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`.
- `quiz.py`: `/api/quiz/submit`, `/api/quiz/history`.
- `stats.py`: `/api/stats/leaderboard`.

---

### Frontend Updates

#### [MODIFY] [frontend/index.html](file:///e:/GitHub/simon/frontend/index.html)
- Giữ nguyên giao diện.
- Di chuyển sang sử dụng `api.js` mới tương thích với FastAPI response format.

#### [NEW] [frontend/js/api.js](file:///e:/GitHub/simon/frontend/js/api.js)
- Axios hoặc Native Fetch wrapper.
- Handle Interceptor để tự động đính kèm JWT Token.

---

## Verification Plan

### 1. Setup Environment
- Tạo file `.env` với `MONGODB_URL` thực tế.
- Cài đặt requirements: `pip install -r backend/requirements.txt`.

### 2. Backend Verification
- Chạy server: `uvicorn backend.app.main:app --reload`.
- Truy cập `http://localhost:8000/docs`.
- Test API `POST /api/auth/register` qua Swagger UI.
- Test API `POST /api/auth/login` -> nhận Token.

### 3. Frontend Integration
- Mở `index.html`.
- Đăng nhập -> Kiểm tra Token lưu trong localStorage.
- Chơi game -> Kiểm tra API `POST /api/quiz/submit` thành công.
- Reload trang -> Kiểm tra thông tin User vẫn hiển thị (Persistence).
