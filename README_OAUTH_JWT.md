# Django Todo App với OAuth 2.0 Google và JWT

Dự án Django Todo App đã được nâng cấp với các tính năng:
- ✅ OAuth 2.0 đăng nhập với Google
- ✅ JWT Authentication cho API
- ✅ REST API endpoints đầy đủ
- ✅ Web interface truyền thống

## 🚀 Tính năng mới

### 1. OAuth 2.0 Google Login
- Đăng nhập/đăng ký bằng tài khoản Google
- Tự động tạo user từ thông tin Google
- Tích hợp với Django Allauth

### 2. JWT Authentication
- Access token và Refresh token
- Token blacklisting khi logout
- Bảo mật API endpoints

### 3. REST API
- CRUD operations cho tasks
- User authentication và profile
- Tìm kiếm và lọc tasks
- Thống kê tasks

## 📦 Packages đã cài đặt

```bash
pip install django-allauth djangorestframework djangorestframework-simplejwt python-decouple requests
```

## ⚙️ Cấu hình

### 1. Environment Variables
Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

Cập nhật với thông tin Google OAuth:
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 2. Google OAuth Setup
Xem hướng dẫn chi tiết trong `GOOGLE_OAUTH_SETUP.md`

### 3. Database Migration
```bash
python manage.py migrate
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register/` - Đăng ký user mới
- `POST /api/auth/login/` - Đăng nhập (lấy JWT tokens)
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Đăng xuất (blacklist token)

### User
- `GET /api/user/profile/` - Lấy thông tin user
- `PUT /api/user/profile/` - Cập nhật thông tin user

### Tasks
- `GET /api/tasks/` - Lấy danh sách tasks
- `POST /api/tasks/` - Tạo task mới
- `GET /api/tasks/{id}/` - Lấy chi tiết task
- `PUT /api/tasks/{id}/` - Cập nhật task
- `DELETE /api/tasks/{id}/` - Xóa task
- `PATCH /api/tasks/{id}/toggle/` - Toggle trạng thái task
- `GET /api/tasks/stats/` - Thống kê tasks

### Query Parameters cho GET /api/tasks/
- `search` - Tìm kiếm trong title và note
- `status` - Lọc theo trạng thái (`done`, `pending`)

## 🧪 Test API

### 1. Sử dụng script demo
```bash
python api_demo.py
```

### 2. Sử dụng curl

#### Đăng ký user mới:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

#### Đăng nhập:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

#### Tạo task (cần JWT token):
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Test Task",
    "note": "This is a test task",
    "is_done": false
  }'
```

### 3. Sử dụng Postman
Import collection từ file `postman_collection.json` (sẽ tạo nếu cần)

## 🌍 Web Interface

### Đăng nhập truyền thống
- URL: `http://localhost:8000/auth/login/`
- Hỗ trợ username/password

### Đăng nhập Google
- URL: `http://localhost:8000/accounts/google/login/`
- Hoặc click nút "Đăng nhập với Google" trên trang login

### Quản lý tasks
- URL: `http://localhost:8000/`
- CRUD operations qua web interface

## 🔧 Development

### Chạy server
```bash
python manage.py runserver
```

### Tạo superuser
```bash
python manage.py createsuperuser
```

### Xem admin
- URL: `http://localhost:8000/admin/`

## 📱 Frontend Integration

### JavaScript Example
```javascript
// Đăng nhập và lấy token
const login = async (username, password) => {
  const response = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  return data;
};

// Gọi API với token
const getTasks = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('/api/tasks/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
};
```

## 🔒 Security Notes

1. **Production Settings:**
   - Đổi `DEBUG = False`
   - Sử dụng HTTPS
   - Cấu hình CORS nếu cần
   - Sử dụng environment variables cho secrets

2. **JWT Settings:**
   - Access token lifetime: 60 phút
   - Refresh token lifetime: 7 ngày
   - Token rotation enabled

3. **Google OAuth:**
   - Cấu hình redirect URIs chính xác
   - Sử dụng HTTPS trong production

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **"redirect_uri_mismatch"**
   - Kiểm tra redirect URIs trong Google Console

2. **"Invalid token"**
   - Token đã hết hạn, sử dụng refresh token

3. **"CORS errors"**
   - Cài đặt django-cors-headers nếu cần

4. **Migration errors**
   - Chạy `python manage.py migrate` sau khi cài packages

## 📚 Tài liệu tham khảo

- [Django Allauth](https://django-allauth.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
