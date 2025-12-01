# chatbot/views.py
import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")  # ✅ This works for all keys

@csrf_exempt
def chat_with_gemini(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user_message = data.get("message", "")
        if not user_message:
            return JsonResponse({"error": "No message"}, status=400)

        try:
            response = model.generate_content(user_message)
            bot_reply = response.text
            return JsonResponse({"reply": bot_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST required"}, status=400)

def chat_page(request):
    return render(request, "chat.html")
