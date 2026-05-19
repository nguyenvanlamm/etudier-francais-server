# Etudier Français Server

FastAPI backend cho Etudier Français client (Next.js).

## Cài đặt

```bash
cd etudier-francais-server
pip install -r requirements.txt
```

## Cấu hình

Copy `.env.example` thành `.env` và cập nhật các giá trị:

```bash
cp .env.example .env
```

## Chạy server

```bash
uvicorn app.main:app --reload --port 5000
```

Server sẽ chạy tại `http://localhost:5000`

## API Documentation

Sau khi chạy server, truy cập:
- Swagger UI: http://localhost:5000/api/docs
- ReDoc: http://localhost:5000/api/redoc

## API Endpoints

### Auth
- `POST /api/auth/login` - Đăng nhập
- `POST /api/auth/register` - Đăng ký
- `POST /api/auth/google` - Đăng nhập Google
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Đăng xuất
- `GET /api/auth/me` - Lấy thông tin user hiện tại
- `PATCH /api/auth/me` - Cập nhật thông tin user

### Exams
- `GET /api/tests` - Lấy danh sách đề thi
- `GET /api/tests/{examId}` - Lấy chi tiết đề thi
- `POST /api/tests/{examId}/submit` - Nộp bài thi
- `GET /api/tests/{examId}/results/{resultId}/review` - Xem lại kết quả

### Courses
- `GET /api/courses` - Lấy danh sách khóa học
- `GET /api/courses/{slug}` - Lấy chi tiết khóa học

### Contact
- `POST /api/contact` - Gửi liên hệ