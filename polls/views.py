from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone


# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get_questions_no_choice(self):
        question_choices = Choice.objects.get(question_id=0)
        return question_choices 






class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
     model = Question
     template_name = "polls/results.html"

     def get_queryset(self):
         return Question.objects.filter(pub_date__lte=timezone.now())
         
    

def votes(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
            "question" : question,
            "error_message" : "you didnt select one"
        }
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # request.POST permite acessar dados pelo nome chave, ele retornar o ID da escolha selecionada como uma string
    except (KeyError, Choice.DoesNotExist):
        return render(request,"polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1 # fala para o bando de dados par aumentar o vote em 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        # reverse usa para evitar ter hardcode url na função, pode ser usar a URLconf

# sempre retornar um HttpResponseRedirect depois de lidar com dados 
# em método POST. Isso previne os dados de serem usados duas vezes se 
# se o usuario clicar em um back button