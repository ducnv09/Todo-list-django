# Hướng dẫn thiết lập Google OAuth 2.0

## Bước 1: Tạo Google Cloud Project

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới hoặc chọn project hiện có
3. Đảm bảo project được chọn ở thanh navigation trên cùng

## Bước 2: Kích hoạt Google+ API

1. Trong Google Cloud Console, đi tới **APIs & Services** > **Library**
2. Tìm kiếm "Google+ API" hoặc "People API"
3. Click vào API và nhấn **Enable**

## Bước 3: Tạo OAuth 2.0 Credentials

1. Đi tới **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Nếu chưa có OAuth consent screen, bạn sẽ được yêu cầu tạo:
   - Chọn **External** user type
   - Điền thông tin cơ bản: App name, User support email, Developer contact
   - Thêm scopes: `../auth/userinfo.email`, `../auth/userinfo.profile`
   - Thêm test users nếu cần

## Bước 4: Cấu hình OAuth Client

1. Chọn **Web application** làm Application type
2. Đặt tên cho OAuth client
3. Thêm **Authorized redirect URIs**:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
4. Click **Create**

## Bước 5: Lấy Client ID và Client Secret

1. Sau khi tạo, bạn sẽ thấy popup với Client ID và Client Secret
2. Copy cả hai giá trị này
3. Hoặc có thể xem lại trong danh sách Credentials

## Bước 6: Cấu hình trong Django

1. Tạo file `.env` từ `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Cập nhật file `.env` với thông tin thực tế:
   ```
   GOOGLE_CLIENT_ID=your_actual_client_id
   GOOGLE_CLIENT_SECRET=your_actual_client_secret
   ```

3. Cài đặt python-decouple để đọc file .env:
   ```bash
   pip install python-decouple
   ```

4. Cập nhật settings.py để sử dụng environment variables:
   ```python
   from decouple import config
   
   SOCIALACCOUNT_PROVIDERS['google']['APP'] = {
       'client_id': config('GOOGLE_CLIENT_ID'),
       'secret': config('GOOGLE_CLIENT_SECRET'),
       'key': ''
   }
   ```

## Bước 7: Chạy Migration và Test

1. Chạy migrations:
   ```bash
   python manage.py migrate
   ```

2. Tạo superuser nếu chưa có:
   ```bash
   python manage.py createsuperuser
   ```

3. Chạy server:
   ```bash
   python manage.py runserver
   ```

4. Truy cập http://localhost:8000 và test đăng nhập Google

## Lưu ý quan trọng

- Đảm bảo redirect URIs trong Google Console khớp chính xác với domain bạn sử dụng
- Trong production, thay đổi redirect URIs thành domain thực tế
- Không commit file `.env` vào git (đã có trong .gitignore)
- Trong production, sử dụng environment variables thay vì file .env

## Troubleshooting

### Lỗi "redirect_uri_mismatch"
- Kiểm tra lại redirect URIs trong Google Console
- Đảm bảo URL chính xác, bao gồm cả protocol (http/https)

### Lỗi "invalid_client"
- Kiểm tra Client ID và Client Secret
- Đảm bảo OAuth consent screen đã được cấu hình

### Lỗi "access_denied"
- Kiểm tra OAuth consent screen status
- Đảm bảo user được thêm vào test users (nếu app chưa published)
