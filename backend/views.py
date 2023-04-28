from django.http import HttpResponseRedirect
from .forms import QAForm
from django.shortcuts import render, redirect
from .models import QA, UserAnswer
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QASerializer
import requests
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



@login_required
def backend(request):
    if request.method == 'POST':
        form = QAForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data.get('question')
            answer = form.cleaned_data.get('answer')

            token, created = Token.objects.get_or_create(user=request.user)
            response = requests.post('http://localhost:8000/api/addquestion/', {'question': question, 'answer': answer}, headers={'Authorization': f'Token {token.key}'})

            if response.status_code == 201:
                qa = QA.objects.create(question=question, answer=answer)
                return redirect('backend')
            else:
                form.add_error(None, 'Errore durante la creazione della domanda.')
    else:
        form = QAForm()

    questions = QA.objects.all()

    context = {'form': form, 'questions': questions}
    return render(request, 'backend.html', context)


@login_required
def quiz(request):
    unanswered_questions = QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True)

    if not unanswered_questions:
        return render(request, 'quiz_completed.html')

    error = False

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer:
            question = QA.objects.get(pk=request.POST.get('question_id'))
            if answer.strip().upper() == question.answer.upper():
                token, created = Token.objects.get_or_create(user=request.user)
                response = requests.post('http://localhost:8000/api/answer/', {'question_id': question.pk, 'answer': answer}, headers={'Authorization': f'Token {token.key}'})
                if response.status_code == 200 and response.json()['correct']:
                    user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
                    user_answer.answered_correctly = True
                    user_answer.save()

                    if QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True).count() == 0:
                        UserAnswer.objects.filter(user=request.user).delete()

                    if UserAnswer.objects.filter(user=request.user, answered_correctly=False).exists():
                        return redirect('quiz')
                    else:
                        UserAnswer.objects.filter(user=request.user).update(answered_correctly=False)
                        return render(request, 'quiz_complete.html')
                else:
                    error = True
            else:
                error = True
        else:
            error = False

    question = random.choice(unanswered_questions)

    context = {'question': question, 'error': error}
    return render(request, 'quiz.html', context)





def quiz_complete(request):
    return render(request, 'quiz_complete.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('backend')
            else:
                form.add_error(None, 'Username o password errati')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('backend')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request):
    question = request.data.get('question')
    answer = request.data.get('answer')

    if not question or not answer:
        return Response({'error': 'question and answer fields are required'}, status=400)

    qa = QA.objects.create(question=question, answer=answer)

    return Response({'question_id': qa.pk}, status=201)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_question(request):
    question_id = request.data.get('question_id')
    answer = request.data.get('answer')
    if not question_id or not answer:
        return Response({'error': 'question_id and answer fields are required'}, status=400)

    try:
        question = QA.objects.get(id=question_id)
    except QA.DoesNotExist:
        return Response(status=404)

    if answer.strip().upper() == question.answer.upper():
        user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
        user_answer.answered_correctly = True
        user_answer.save()
        return Response({'correct': True})
    else:
        user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
        user_answer.answered_correctly = False
        user_answer.save()
        return Response({'correct': False})






