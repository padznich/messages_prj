from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from models import Message, Comment
from forms import MessageForm, CommentForm


def show_messages(request):

    request.session['real_url'] = request.build_absolute_uri()
    messages = Message.objects.order_by("-id")          # some JOIN with comments for ordering by comments.added_at
    limit = 3
    page = request.GET.get("page", 1)
    paginator = Paginator(messages, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)

    context = {'page': page,
               'paginator': paginator,
               'messages': page.object_list,
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
    comment_form = CommentForm()

    context = {'message': message,
               'comments': comments,
               'comment_form': comment_form,
               }

    return render(request, 'message.html', context)
