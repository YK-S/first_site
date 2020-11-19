
import pytz
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *
import json
import datetime 
# Create your views here.
def vote(request):
    name = request.session.get("user_name")
    utc_tz = pytz.timezone('UTC')
    now_time = datetime.datetime.now(tz=utc_tz)
    vote_set = Vote.objects.filter(end_time__gte=now_time, vote_type__in=[0, 2]).order_by('start_time')[::-1] # 时间未过期
    vote_set = vote_set[0:8]
    data = list()
    for vote in vote_set:
        data.append([vote.id, vote.vote_name, vote.start_time+datetime.timedelta(hours=8), vote.builder.user_name])
    response = render(request, "HomePage.html", {"name": name, "data": data})
    return response



def login(request):
    json_request = json.loads(request.body)     # 获取JSON Request
    name = json_request['name']
    pwd = json_request['pwd']
    user_set = User.objects.filter(user_name=name)  # 找注册名
    code = 1    # 登录成功
    ret_name = ''
    if user_set.exists() is False:  # 没有找到则注册
        user = User(user_name=name, user_pwd=pwd)
        user.save()
        code = 2    # 注册成功
    elif user_set[0].user_pwd == pwd:  # 找到且密码一致 返回登录名
        request.session['user_name'] = name
        ret_name = name
    else:  # 密码不一致
        code = 3    # 用户名或密码错误
    response = JsonResponse({'code': code, 'name': ret_name})
    print(code)
    print(name)
    return response


def check_login(request):      # 检查登录状态 返回true false
    name = request.session.get("user_name")
    if name is None:
        response = HttpResponse("false")
    else:
        response = HttpResponse("true")
    return response


def logout(request):    # 登出
    name = request.session.get('user_name')
    if name is not None:
        del request.session['user_name']
        response = HttpResponse('true')    # 成功登出
    else:
        response = HttpResponse('false')
    return response


def make_vote(request):
    json_request = json.loads(request.body)     # 获取JSON Request
    vote = json_request["vote"]
    vote_name = vote.get("vote_name")
    items_content = vote.get("vote_items")
    builder = User.objects.get(user_name=vote.get("builder"))
    details = vote.get("vote_details")
    print(details)
    utc_tz = pytz.timezone('UTC')
    end_time = datetime.datetime.now(tz=utc_tz) + datetime.timedelta(days=vote.get("limit_days"))
    new_vote = Vote(vote_name=vote_name, vote_type=vote.get("vote_type"), end_time=end_time, builder=builder, vote_details=details)
    new_vote.save()
    for item_content in items_content:
        new_vote = Vote.objects.get(vote_name=vote_name, vote_type=vote.get("vote_type"), end_time=end_time, builder=builder, vote_details=details)
        item = Item(content=item_content, vote=new_vote)
        item.save()
    response = JsonResponse({"ret": True})
    return response


def max_page(request):
    votes_per_page = 8
    utc_tz = pytz.timezone('UTC')
    now_time = datetime.datetime.now(tz=utc_tz)
    num_of_vote = Vote.objects.filter(end_time__gte=now_time, vote_type__in=[0, 2]).count()
    page = int(num_of_vote/votes_per_page)+1
    response = JsonResponse({"ret": page})
    return response


def get_table(request):
    votes_per_page = 8
    page = request.GET.get("page")
    search = request.GET.get("search")
    name = request.GET.get("name")
    type13 = request.GET.get("type13")
    vote_type = [0,2]
    if type13 == '1':
        vote_type = [0,1,2,3]
    print(vote_type,type13)
    if search is None:
        search = ""
    page = int(page)
    vote_begin = (page-1)*votes_per_page
    vote_end = page*votes_per_page
    utc_tz = pytz.timezone('UTC')
    now_time = datetime.datetime.now(tz=utc_tz)
    if name == "":
        vote_set = Vote.objects.filter(end_time__gte=now_time, vote_type__in=vote_type, vote_name__contains=search).order_by('start_time')[::-1]  # 时间未过期
    else:
        builder = User.objects.get(user_name=name)
        vote_set = Vote.objects.filter(end_time__gte=now_time, vote_type__in=vote_type,
                                       vote_name__contains=search, builder=builder).order_by('start_time')[::-1]  # 时间未过期
    num_of_vote = len(vote_set)
    max_page = int(num_of_vote / votes_per_page) + 1
    vote_set = vote_set[vote_begin:vote_end]
    data = list()
    for vote in vote_set:
        data.append([vote.id, vote.vote_name, (vote.start_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), vote.builder.user_name])
    response = JsonResponse({"data": data, "max_page": max_page})
    return response


def vote_exist(request):
    vote_id = request.GET.get("id")
    ret = False
    items = list()
    vote_name = ""
    details = ""
    vote_type = 0
    if vote_id != 'NaN':
        vote_set = Vote.objects.filter(id=vote_id)
        ret = vote_set.exists()
        items = list()
        if ret is True:
            item_set = Item.objects.filter(vote=vote_set[0])
            vote_type = vote_set[0].vote_type
            vote_name = vote_set[0].vote_name
            details = vote_set[0].vote_details
            for item in item_set:
                items.append(item.content)
    response = JsonResponse({"ret": ret, "items": items, "type": vote_type,"vote_name":vote_name,"details":details})
    return response


def test(request):
    votes = Vote.objects.all()
    for item in votes:
        item.delete()
    return redirect("/vote/")


def select(request):
    json_request = json.loads(request.body)     # 获取JSON Request
    print(json_request)
    select = json_request.get('s')
    id = int(json_request.get('id'))
    print(select)
    response = JsonResponse({"select":select,"id":id})
    items = Item.objects.filter(vote=Vote.objects.get(id=id))
    ids = list()
    for item in items:
        ids.append(item.id)
    for i in select:
        item = Item.objects.get(id=ids[i])
        poll = item.poll + 1
        item.poll = poll
        item.save()
    return response
    

def get_my_vote(request):
    vote_id = request.GET.get("id")
    items = list()
    polls = list()
    vote = Vote.objects.get(id=vote_id)
    details = vote.vote_details
    item_set = Item.objects.filter(vote=vote)
    for item in item_set:
        items.append(item.content)
        polls.append(item.poll)
    response = JsonResponse({"items": items, "polls":polls,"details":details})
    return response