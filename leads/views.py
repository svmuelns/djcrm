# VIEWS.PY DETERMINES WHAT YOU'LL SEE WHEN YOU ENTER TO ANY URL

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm

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
    form = LeadModelForm()
    print(request.POST) # data we submitted in html
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadModelForm(request.POST) # LeadForm() convalidates the fields, if it's have less chars than needed etc
        if form.is_valid():
            form.save()
            return redirect('/leads') # we go back to /leads once we create a form
    context = {
        "form": form 
    }
    return render(request, "leads/lead_create.html", context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead) # specifies the single instance of the Module we want to update instead of saving a new instance of the lead
                                        # we will see a prepopulated form from the lead we're on
    # TO SUBMIT EDITS, WE HAVE TO VALIDATE THE DATA
    if request.method == "POST":
        print('Receiving a post request')
        form = LeadModelForm(request.POST, instance=lead) # LeadForm() convalidates the fields, if it's have less chars than needed etc
        if form.is_valid():
            form.save()
            return redirect('/leads') # we go back to /leads once we create a form

    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# LONG WAY TO DO IT
# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     print(request.POST) # data we submitted in html
    
#     # TO SUBMIT EDITS, WE HAVE TO VALIDATE THE DATA
#     if request.method == "POST":
#         print('Receiving a post request')
#         form = LeadForm(request.POST) # LeadForm() convalidates the fields, if it's have less chars than needed etc
#         if form.is_valid():
#             print("The form is valid")
#             print(form.cleaned_data)

#             # ===== RETRIEVING DATA ====
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             # ===== LEAD UPDATE =====
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age

#             lead.save()
#             return redirect('/leads') # we go back to /leads once we create a form
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)

# LARGE WAY TO DO

# def lead_create(request):
    # form = LeadForm()
    # print(request.POST) # data we submitted in html
    # if request.method == "POST":
    #     print('Receiving a post request')
    #     form = LeadForm(request.POST) # LeadForm() convalidates the fields, if it's have less chars than needed etc
    #     if form.is_valid():
    #         print("The form is valid")
    #         print(form.cleaned_data)

    #         # ===== RETRIEVING DATA ====
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = form.cleaned_data['agent']
    #         # ===== LEAD CREATION =====
    #         Lead.objects.create(
    #             first_name = first_name,
    #             last_name = last_name,
    #             age = age,
    #             agent = agent
    #         )
    #         print('The lead has been created')
    #         return redirect('/leads') # we go back to /leads once we create a form
    # context = {
    #     "form": form 
    # }
#     return render(request, "leads/lead_create.html", context)