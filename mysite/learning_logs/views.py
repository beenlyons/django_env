from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    '''学习笔记主页'''
    return render(request, r"learning_logs/index.html")

@login_required
def topics(request):
    '''显示所有主题'''
    # 查询数据库获取topics信息, 并按date_added进行排序
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 定义一个将要发送给模板的上下文。上下文是一个字典，其中键是我们在模板中要访问的数据的名称
    context = {'topics': topics}
    # 返回
    return render(request, r'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''显示单个主题及其所有的条目'''
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {"topic": topic, "entries": entries}
    return render(request, r'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''添加新主题'''

    if request.method != "POST":
        # 未提交数据， 创建一个表单
        form = TopicForm()
    else:
        # 提交了数据，队数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 保存到数据库
            form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            # reverse获取topics的url
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    '''
    添加新主题
    :param request:
    :param topic_id:
    :return:
    '''
    topic_of_entry = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        # 未提交数据， 创建一个表单
        form = EntryForm()
    else:
        # 提交了数据，队数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 保存到数据库
            new_entry = form.save(commit=False)
            # reverse获取topics的url
            new_entry.topic = topic_of_entry
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {"topic": topic_of_entry, "form": form}
    return render(request, "learning_logs/new_entry.html", context)

@login_required
def edit_entry(request, entry_id):
    '''
    编辑既有条目
    :param request:
    :param entry_id:
    :return:
    '''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # 初次请求 使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        #  POST提交了数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)