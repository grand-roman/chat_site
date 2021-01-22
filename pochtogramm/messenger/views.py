from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from functools import wraps
from time import sleep
# Create your views here.
from messenger.models import Message
from users.models import CustomUser

from django.db import connection, reset_queries
import logging
import time

from django.views.decorators.gzip import gzip_page
from django.contrib.auth.decorators import login_required


def artificial_delay(execute, sql, params, many, context):
    sleep(0.03)
    return execute(sql, params, many, context)


def sql_request_delay(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with connection.execute_wrapper(artificial_delay):
            return func(*args, **kwargs)
    return wrapper


def log_time(func):
    log = logging.getLogger(func.__name__)
    @wraps(func)
    def wrapped(*args, **kwargs):
        log.error(f'calling {func.__name__}')
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        log.error(f'finished {func.__name__} for {end - start}')
        return res
    return wrapped


def log_sql(func):
    log = logging.getLogger(func.__name__)
    @wraps(func)
    def wrapped(*args, **kwargs):
        reset_queries()
        res = func(*args, **kwargs)
        log.error(f'Total {len(connection.queries)}')
        for q in connection.queries:
            log.error(f'{q["sql"]}')
        return res
    return wrapped

def cached(func):
    last_executed = 0.0
    last_value = None
    @wraps(func)
    def wrapped(*args, **kwargs):
        nonlocal last_value
        nonlocal last_executed
        if time.time() - last_executed > 0.7:
            last_value = func(*args, **kwargs)
            last_executed = time.time()
        return last_value
    return wrapped


def hello(request):
    if request.user.is_authenticated:
        return chat(request)
    else:
        return ask_login(request)


def chat(request):
    return render(request, 'chat.html')


def ask_login(request):
    return render(request, 'index.html')


def send(request):
    if 'message_input' not in request.POST:
        return HttpResponse("message is required", status=400)

    message_text = request.POST['message_input']
    message = Message(text=message_text, author=CustomUser(pk=request.user.id))
    message.save()

    return HttpResponse(f'Id: {message.id}', status=201)


@log_sql
@log_time
@gzip_page
@sql_request_delay
def chat_box(request):
    messages = reversed([
        {
            'user': m.author.username,
            'own': m.author_id == request.user.id,
            'message': m.text,
            'time': m.date.strftime("%H.%M")
        }
        for m in get_messages()
    ])

    return render(request, 'chat_box.html', context={
        'messages': messages
    })

@cached
def get_messages():
    return [m for m in Message.objects.select_related('author').order_by('-date').all()[:20]]


def flooders(request):
    fl = [
        {
            'name': u.username,
            'count': u.cnt
        }
        for u in CustomUser.objects.annotate(cnt=Count('messages')).order_by('-cnt').all()[:10]
    ]
    return render(request, 'flooders.html', context={
        'flooders': fl
    })


def search(request):
    if 'text' not in request.GET:
        return HttpResponse("text is required", status=400)

    messages = [] if len(request.GET['text']) == 0 else reversed([
        {
            'user': m.author.username,
            'own': m.author_id == request.user.id,
            'message': m.text,
            'time': m.date.strftime("%H.%M")
        }
        for m in Message.objects.select_related('author').filter(text__contains=request.GET['text']).order_by('-date')[:4]
    ])

    return render(request, 'chat_box.html', context={
        'messages': messages
    })

