# VIEWS.PY DETERMINES WHAT YOU'LL SEE WHEN YOU ENTER TO ANY URL

from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganizerAndLoginRequiredMixin
from django.http import HttpResponse
from django.views import generic                    # from django.views.generic import Template, ListView, DetailView, UpdateView, DeleteView
from .models import Lead, Agent, Category
from .forms import (LeadForm, LeadModelForm, CustomUserCreationForm, 
    LeadCategoryUpdateForm, LeadModelOrganizerForm #AssignAgentForm
)
# CRUD+L - Create, Retrieve, Update and Delete + List

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')

def landing_page(request): # deprecated ones, we will use only class, delete later
    return render(request, "landing.html")

class LandingPageView(generic.TemplateView):    # Class Based Views
    template_name = "landing.html"

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    #return HttpResponse('Hello world')
    return render(request, 'leads/lead_list.html', context)

class LeadListView(LoginRequiredMixin, generic.ListView):           # class LeadListView(ListView)
    template_name = 'leads/lead_list.html'
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
            # it's not doing multiple querys on db, just temporal ones to filter
            # FILTER the leads WERE the agents are the logged in agent
        return queryset

def lead_detail(request, pk): #primarykey
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadDetailView(generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

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

class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.agent.organization
        lead.agent = self.request.user.agent
        lead.save()
        # TODO send email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

class LeadCreateOrganizerView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelOrganizerForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(LeadCreateOrganizerView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.agent.organization
        lead.save()
        # TODO send email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateOrganizerView, self).form_valid(form)

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

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')

class LeadUpdateOrganizerView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelOrganizerForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(LeadUpdateOrganizerView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse('leads:lead-list')

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:lead-list')

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
        
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            "contacted_lead_count": queryset.filter(category=1).count(),
            "converted_lead_count": queryset.filter(category=2).count(),
            "unconverted_lead_count": queryset.filter(category=3).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)

        elif user.is_agent:
            queryset = Category.objects.filter(organization=user.agent.organization)
        
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)

        if user.is_agent:
            queryset = Category.objects.filter(organization=user.agent.organization)
        
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):

    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)

        if user.is_agent:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk":self.get_object().id})
        # will redirect like if we typed lead.pk
        #kwargs dictionary of arguments





# class AssignAgentView(LoginRequiredMixin, generic.FormView):
#     template_name = "leads/assign_agent.html"
#     form_class = AssignAgentForm

#     def get_form_kwargs(self):
#         return {
#             "request": self.request
#         }


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
    # context = {
    #     "form": form,
    #     "lead": lead
    # }
    # return render(request, "leads/lead_update.html", context)

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