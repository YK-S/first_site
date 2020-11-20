from django.http import JsonResponse
from django.shortcuts import render

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
    responce = render(request, 'default.html')
    return responce