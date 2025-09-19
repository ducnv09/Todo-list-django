from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import requests
from .models import ChatMessage

@csrf_exempt
@login_required
def chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'error': 'Tin nhắn không được để trống'}, status=400)

            # Lấy lịch sử chat gần đây để tạo ngữ cảnh (3 tin nhắn gần nhất)
            recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:3]

            # Gọi Gemini API với ngữ cảnh
            gemini_response = call_gemini_api(user_message, recent_messages)

            # Lưu vào database
            chat_message = ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=gemini_response
            )

            return JsonResponse({
                'response': gemini_response,
                'success': True
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)

def call_gemini_api(message, recent_messages=None):
    """Gọi Gemini API để lấy phản hồi với ngữ cảnh"""
    try:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return "Xin lỗi, API key chưa được cấu hình."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        headers = {
            'Content-Type': 'application/json',
        }

        # Tạo ngữ cảnh từ lịch sử chat
        context = "Bạn là một trợ lý AI thông minh và hữu ích. Hãy trả lời bằng tiếng Việt một cách ngắn gọn và dễ hiểu."

        if recent_messages and recent_messages.exists():
            context += "\n\nLịch sử cuộc trò chuyện gần đây (từ mới nhất đến cũ nhất):"
            for msg in recent_messages:
                context += f"\nNguời dùng: {msg.message}"
                context += f"\nTrợ lý: {msg.response}"

        context += f"\n\nCâu hỏi hiện tại: {message}"

        data = {
            "contents": [{
                "parts": [{
                    "text": context
                }]
            }]
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Xin lỗi, tôi không thể tạo phản hồi cho câu hỏi này."
        else:
            return f"Lỗi API: {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        return "Xin lỗi, yêu cầu đã hết thời gian chờ. Vui lòng thử lại."
    except requests.exceptions.RequestException as e:
        return f"Lỗi kết nối: {str(e)}"
    except Exception as e:
        return f"Lỗi không xác định: {str(e)}"

@login_required
def chat_history(request):
    """Lấy lịch sử chat của user"""
    messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]  # 5 tin nhắn gần nhất

    history = []
    for msg in messages:
        history.append({
            'message': msg.message,
            'response': msg.response,
            'created_at': msg.created_at.strftime('%H:%M %d/%m/%Y')
        })

    return JsonResponse({'history': history})
