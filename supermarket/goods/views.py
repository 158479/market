from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request,'goods/index.html')

def main(request):
    return render(request,'goods/main.html')

def goods_list(request):
    return render(request,'goods/list.html')