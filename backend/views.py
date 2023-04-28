from django.http import HttpResponseRedirect
from .forms import QAForm
from django.shortcuts import render, redirect
from .models import QA, UserAnswer
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


@login_required
def backend(request):
    if request.method == 'POST':
        form = QAForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            qa = QA(question=question, answer=answer)
            qa.save()
            return HttpResponseRedirect('backend')
    else:
        form = QAForm()
    return render(request, 'backend.html', {'form': form})

@login_required
def quiz(request):
    error = False

    unanswered_questions = QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True)

    if not unanswered_questions:
        UserAnswer.objects.filter(user=request.user).update(answered_correctly=False)
        return render(request, 'quiz_complete.html')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer:
            question = QA.objects.get(pk=request.POST.get('question_id'))
            if answer.strip().upper() == question.answer.upper():
                user_answer = UserAnswer.objects.get_or_create(user=request.user, question=question)[0]
                user_answer.answered_correctly = True
                user_answer.save()

                if QA.objects.exclude(useranswer__user=request.user, useranswer__answered_correctly=True).count() == 0:
                    UserAnswer.objects.filter(user=request.user).answered_correctly=0

                if UserAnswer.objects.filter(user=request.user, answered_correctly=False).exists():
                    return redirect('quiz')
                else:
                    UserAnswer.objects.filter(user=request.user).update(answered_correctly=False)
                    return render(request, 'quiz_complete.html')
            else:
                error = True

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





