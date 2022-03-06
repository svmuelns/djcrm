# VIEWS.PY DETERMINES WHAT YOU'LL SEE WHEN YOU ENTER TO ANY URL

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    #return HttpResponse('Hello world')
    return render(request, 'leads/lead_list.html', context)

def lead_detail(request, pk): #primarykey
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request):
    form = LeadForm()
    print(request.POST) # data we submitted in html
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadForm(request.POST) # LeadForm() convalidates the fields, if it's have less chars than needed etc
        if form.is_valid():
            print("The form is valid")
            print(form.cleaned_data)

            # ===== RETRIEVING DATA ====
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.first() # it will retrieve the first object
            
            # ===== LEAD CREATION =====
            Lead.objects.create(
                first_name = first_name,
                last_name = last_name,
                age = age,
                agent = agent
            )
            print('The lead has been created')
            return redirect('/leads') # we go back to /leads once we create a form
    context = {
        "form": form 
    }
    return render(request, "leads/lead_create.html", context)