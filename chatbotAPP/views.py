import openai
from django.http import JsonResponse
from django.shortcuts import render

openai_api_key = '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'
openai.api_key = openai_api_key


def ask_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')
