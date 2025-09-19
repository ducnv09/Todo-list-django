#!/usr/bin/env python3
"""
Demo script để test API endpoints với JWT authentication
Chạy script này để test các API endpoints sau khi setup xong
"""

import requests
import json
from datetime import datetime

# Base URL của API
BASE_URL = "http://localhost:8000/api"

class TodoAPIDemo:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()
    
    def register_user(self, username, email, password):
        """Đăng ký user mới"""
        url = f"{self.base_url}/auth/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password
        }
        
        response = self.session.post(url, json=data)
        print(f"Register Response: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            self.access_token = result.get('access')
            self.refresh_token = result.get('refresh')
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            print(f"✅ Đăng ký thành công! User: {result['user']['username']}")
            return True
        else:
            print(f"❌ Đăng ký thất bại: {response.text}")
            return False
    
    def login_user(self, username, password):
        """Đăng nhập user"""
        url = f"{self.base_url}/auth/login/"
        data = {
            "username": username,
            "password": password
        }
        
        response = self.session.post(url, json=data)
        print(f"Login Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result.get('access')
            self.refresh_token = result.get('refresh')
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            print(f"✅ Đăng nhập thành công! User: {result.get('user', {}).get('username', 'Unknown')}")
            return True
        else:
            print(f"❌ Đăng nhập thất bại: {response.text}")
            return False
    
    def get_user_profile(self):
        """Lấy thông tin profile user"""
        url = f"{self.base_url}/user/profile/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Profile: {user['username']} ({user['email']})")
            return user
        else:
            print(f"❌ Không thể lấy profile: {response.text}")
            return None
    
    def create_task(self, title, note="", due_at=None):
        """Tạo task mới"""
        url = f"{self.base_url}/tasks/"
        data = {
            "title": title,
            "note": note,
            "is_done": False
        }
        
        if due_at:
            data["due_at"] = due_at
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 201:
            task = response.json()
            print(f"✅ Tạo task thành công: {task['title']} (ID: {task['id']})")
            return task
        else:
            print(f"❌ Không thể tạo task: {response.text}")
            return None
    
    def get_tasks(self, search=None, status=None):
        """Lấy danh sách tasks"""
        url = f"{self.base_url}/tasks/"
        params = {}
        
        if search:
            params['search'] = search
        if status:
            params['status'] = status
        
        response = self.session.get(url, params=params)
        
        if response.status_code == 200:
            result = response.json()
            tasks = result.get('results', [])
            print(f"✅ Lấy được {len(tasks)} tasks")
            for task in tasks:
                status_icon = "✅" if task['is_done'] else "⏳"
                print(f"  {status_icon} {task['title']} (ID: {task['id']})")
            return tasks
        else:
            print(f"❌ Không thể lấy tasks: {response.text}")
            return []
    
    def toggle_task(self, task_id):
        """Toggle trạng thái task"""
        url = f"{self.base_url}/tasks/{task_id}/toggle/"
        response = self.session.patch(url)
        
        if response.status_code == 200:
            result = response.json()
            task = result['task']
            status = "hoàn thành" if task['is_done'] else "chưa hoàn thành"
            print(f"✅ Task '{task['title']}' đã được đánh dấu {status}")
            return task
        else:
            print(f"❌ Không thể toggle task: {response.text}")
            return None
    
    def get_task_stats(self):
        """Lấy thống kê tasks"""
        url = f"{self.base_url}/tasks/stats/"
        response = self.session.get(url)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Thống kê tasks:")
            print(f"  - Tổng số: {stats['total']}")
            print(f"  - Hoàn thành: {stats['completed']}")
            print(f"  - Đang thực hiện: {stats['pending']}")
            return stats
        else:
            print(f"❌ Không thể lấy thống kê: {response.text}")
            return None
    
    def logout(self):
        """Đăng xuất"""
        url = f"{self.base_url}/auth/logout/"
        data = {"refresh": self.refresh_token}
        
        response = self.session.post(url, json=data)
        
        if response.status_code == 200:
            print("✅ Đăng xuất thành công!")
            self.access_token = None
            self.refresh_token = None
            self.session.headers.pop('Authorization', None)
            return True
        else:
            print(f"❌ Đăng xuất thất bại: {response.text}")
            return False

def main():
    """Demo chính"""
    print("🚀 Demo API Todo App với JWT Authentication")
    print("=" * 50)
    
    demo = TodoAPIDemo()
    
    # Test đăng ký user mới
    print("\n1. Đăng ký user mới...")
    username = f"testuser_{datetime.now().strftime('%H%M%S')}"
    email = f"{username}@example.com"
    password = "testpassword123"
    
    if demo.register_user(username, email, password):
        # Test lấy profile
        print("\n2. Lấy thông tin profile...")
        demo.get_user_profile()
        
        # Test tạo tasks
        print("\n3. Tạo một số tasks...")
        demo.create_task("Học Django", "Tìm hiểu về Django REST Framework")
        demo.create_task("Làm bài tập", "Hoàn thành bài tập về API")
        demo.create_task("Đọc sách", "Đọc sách về Python")
        
        # Test lấy danh sách tasks
        print("\n4. Lấy danh sách tasks...")
        tasks = demo.get_tasks()
        
        # Test toggle task
        if tasks:
            print("\n5. Toggle trạng thái task đầu tiên...")
            demo.toggle_task(tasks[0]['id'])
        
        # Test tìm kiếm
        print("\n6. Tìm kiếm tasks...")
        demo.get_tasks(search="Django")
        
        # Test thống kê
        print("\n7. Lấy thống kê...")
        demo.get_task_stats()
        
        # Test đăng xuất
        print("\n8. Đăng xuất...")
        demo.logout()
    
    print("\n🎉 Demo hoàn thành!")

if __name__ == "__main__":
    main()
