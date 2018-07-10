from django.shortcuts import render, redirect, get_object_or_404 #TODO: pesquisar sobre isso get_list_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
User = get_user_model()

from .forms import NewTopicForm, NewBoardForm
from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'boards/topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('forum:board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})

def new_board(request):
    if request.method == 'POST':
        form = NewBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
        
            return redirect('edp:edps')
    else:
        form = NewBoardForm()
    return render(request, 'boards/new_topic.html', {'form': form})
   
   