# VIEWS.PY DETERMINES WHAT YOU'LL SEE WHEN YOU ENTER TO ANY URL


from django.shortcuts import render

def home_page(request):
    #return HttpResponse('Hello world')
    return render(request, 'index.html')