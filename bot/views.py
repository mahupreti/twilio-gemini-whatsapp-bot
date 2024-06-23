import os
from django.shortcuts import render, HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)

twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(twilio_account_sid, twilio_auth_token)

@csrf_exempt
def query(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        print(response)
        generated_text = response.text

        formatted_text = generated_text.replace('**', '*')
        return formatted_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

@csrf_exempt
def bot(request):
    instruction = request.POST["Body"]
    name = request.POST["ProfileName"]
    to = request.POST["From"]
    response_from_bot = query(instruction)

    if len(response_from_bot) > 1600:
        response_from_bot = response_from_bot[:1597] + '...'  

    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=response_from_bot,
            to=to
        )
        print(message)
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

    return HttpResponse("ok")
