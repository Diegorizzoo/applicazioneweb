from django.http import HttpResponseRedirect
from .forms import QAForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import QA
import random

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


def quiz(request):
    unanswered_questions = QA.objects.filter(answered_correctly=0)
    if not unanswered_questions:
        # Se non ci sono domande senza answer corretta, mostra il messaggio di completamento
        QA.objects.all().update(answered_correctly=0)
        return render(request, 'quiz_complete.html')

    # Seleziona una domanda casuale tra quelle senza answer corretta
    question = random.choice(unanswered_questions)


    if request.method == 'POST':
        # Check the answer given by the user
        selected_answer = request.POST.get('answer')
        if(selected_answer==question.answer):
            question.answered_correctly = 1
            question.save()
            return redirect('quiz')
        else:
            # Show an error message if the answer is incorrect
            error = True
    else:
        error = False

    context = {'question': question, 'error': error}
    return render(request, 'quiz.html', context)


def quiz_complete(request):
    return render(request, 'quiz_complete.html')


