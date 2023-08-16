import openai
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

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


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        # check to see if user is valid and in db
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_msg = 'Invalid username or password'
            return render(request, 'login.html', {'error_msg': error_msg})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # make sure password1 and password2 are identical
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                print("User registered successfuly! Muy bien!")
                return redirect('chatbot')
            except Exception:
                error_msg = 'Error creating account'
                return render(request, 'register.html', {'error_msg': error_msg})
        else:
            error_msg = 'Passwords do not match'
            return render(request, 'register.html', {'error_msg': error_msg})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
