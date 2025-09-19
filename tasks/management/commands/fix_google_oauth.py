from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config


class Command(BaseCommand):
    help = 'Fix Google OAuth configuration - remove duplicates and update site'

    def handle(self, *args, **options):
        # Lấy thông tin từ environment variables
        client_id = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR(
                    'Vui lòng cấu hình GOOGLE_CLIENT_ID và GOOGLE_CLIENT_SECRET trong file .env'
                )
            )
            return
        
        # Xóa tất cả Google OAuth apps hiện có
        google_apps = SocialApp.objects.filter(provider='google')
        count = google_apps.count()
        if count > 0:
            google_apps.delete()
            self.stdout.write(
                self.style.WARNING(f'Đã xóa {count} Google OAuth app(s) trùng lặp')
            )
        
        # Cập nhật site domain
        site = Site.objects.get(pk=1)
        site.domain = 'localhost:8000'
        site.name = 'Django Todo App'
        site.save()
        self.stdout.write(
            self.style.SUCCESS(f'Đã cập nhật site: {site.domain}')
        )
        
        # Tạo Google OAuth app mới
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        
        # Liên kết app với site
        google_app.sites.add(site)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Google OAuth đã được cấu hình lại thành công!\n'
                f'Client ID: {client_id[:20]}...\n'
                f'Site: {site.domain}\n'
                f'App ID: {google_app.id}'
            )
        )
