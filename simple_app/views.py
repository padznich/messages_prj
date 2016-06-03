from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Message, Comment
from forms import MessageForm, CommentForm


def show_messages(request):

    request.session['real_url'] = request.build_absolute_uri()

    messages = Message.objects.order_by("-id")          # some JOIN with comments for ordering by comments.added_at
    limit = 3
    page = request.GET.get("page", 1)
    paginator = Paginator(messages, limit)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages = paginator.page(paginator.num_pages)

    context = {'page': page,
               'paginator': paginator,
               'messages': messages,
               }

    return render(request, 'home.html', context)


def add_message(request):

    if request.method == "POST":
        message_form = MessageForm(request.POST or None)
        if message_form.is_valid():
            message_form.save()
            return HttpResponseRedirect(request.session.get('real_url'))
    else:
        message_form = MessageForm()

    context = {
        "message_form": message_form,
    }

    return render(request, 'add_message.html', context)


def choosen_message(request, id):

    request.session['real_url'] = request.build_absolute_uri()
    message = Message.objects.get(id=id)

    comments = Comment.objects.filter(message=id)
    limit = 20
    page = request.GET.get("page", 1)
    paginator = Paginator(comments, limit)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    if request.is_ajax():
        template = 'form.html'
    else:
        template = 'message.html'

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CommentForm()

    context = {'page': page,
               'paginator': paginator,
               'message': message,
               'comments': comments,
               'form': form,
               }

    return render(request, template, context)
