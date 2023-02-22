from django.shortcuts import render

# 메인 화면 페이지
def index(request):

    # sidebar active
    nav_check = "sidebar_main"
    
    return render(request, "main.html", {'nav_check' : nav_check})