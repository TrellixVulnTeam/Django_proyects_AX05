from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm, NewTodoForm, UpdateTodoForm
import datetime

def index(request):
	todo_list = Todo.objects.order_by('id')
	newtodoform = NewTodoForm()
	mydate = datetime.datetime.now()
	context = {'todo_list' : todo_list, 'form' : newtodoform, 'mydate' : mydate}
	return render(request, 'todo/index.html', context)

@require_POST
def addTodo(request):
	newtodoform = NewTodoForm(request.POST)
	if newtodoform.is_valid():
		new_todo = newtodoform.save()
	return redirect('index')

@require_POST
def updateLastTodo(request):
	updatetodo = Todo.objects.order_by('-pk')[0]
	updatetodoform = UpdateTodoForm(request.POST, instance=updatetodo)
	if updatetodoform.is_valid():
		new_todo = updatetodoform.save()
	return redirect('index')

def completeTodo(request, todo_id):
	todo = Todo.objects.get(pk=todo_id)
	if todo.complete:
		todo.complete = False
	else:
		todo.complete = True
	todo.save()
	return redirect ('index')

def deleteCompleted(request):
	Todo.objects.filter(complete__exact=True).delete()
	return redirect('index')

def deleteAll(request):
	Todo.objects.all().delete()
	return redirect('index')
