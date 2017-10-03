from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .forms import Todo_Form
from .models import Todo
from lab_1.views import mhs_name


# Create your views here.
response = {}
def index(request):    
    response['author'] = "Fajrin Maulana K" #TODO Implement yourname
    todo = Todo.objects.all()
    response['todo'] = todo
    html = 'lab_5/lab_5.html'
    response['todo_form'] = Todo_Form
    return render(request, html, response)

def add_todo(request):
    form = Todo_Form(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        response['title'] = request.POST['title']
        response['description'] = request.POST['description']
        todo = Todo(title=response['title'],description=response['description'])
        todo.save()
        return HttpResponseRedirect('/lab-5/')
    else:
        return HttpResponseRedirect('/lab-5/')

def delete_todo(request, object_id=None):
    obj = get_object_or_404(Todo, pk=object_id)
    obj.delete()
    return HttpResponseRedirect('/lab-5/')

