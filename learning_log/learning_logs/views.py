from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """Learning log home page"""
    return render(request, "learning_logs/index.html")


def topics(request):
    """Show all topics"""
    if request.user.is_authenticated:
        topics = Topic.objects.filter(Q(owner=request.user) | Q(public=True)).order_by(
            "date_added"
        )
    else:
        topics = Topic.objects.filter(public=True).order_by("date_added")

    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.public and (
        not request.user.is_authenticated or request.user != topic.owner
    ):
        raise Http404

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user and not topic.public:
        raise Http404

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if entry.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
