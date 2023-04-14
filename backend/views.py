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
    unanswered_questions = QA.question.filter(answered_correctly=False)
    if not unanswered_questions:
        # Se non ci sono domande senza answer corretta, mostra il messaggio di completamento
        return render(request, 'quiz_completed.html')

    # Seleziona una domanda casuale tra quelle senza answer corretta
    question = random.choice(unanswered_questions)

    if request.method == 'POST':
        # Controlla la answer data dall'utente
        answer = request.POST.get('answer')
        if answer == QA.answer:
            # Se la answer è corretta, aggiorna il campo answered_correctly a True

            QA.answered_correctly = True
            QA.save()
            return redirect('quiz')
        else:
            # Se la answer è errata, mostra un messaggio di errore e ricarica la pagina
            error = True
    else:
        error = False

    context = {'question': question, 'error': error}
    return render(request, 'quiz.html', context)


def quiz_complete(request):
    return render(request, 'quiz_complete.html')


