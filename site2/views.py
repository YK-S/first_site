from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def test(request):
    if request.method == "GET":
        response = render(request,"test.html")
    else:
        name = request.POST.get("uname")
        print(name)
        response = JsonResponse({'ret':name})
    return response


def default(request):
    error = ""
    if request.method == "POST":
        pwd = request.POST.get("pwd")
        if pwd == "0603":
            request.session['permission'] = 'True'
            return redirect("/vote/")
        else:
            error = "密码错误"
    responce = render(request, 'default.html', context={"error": error})
    return responce
