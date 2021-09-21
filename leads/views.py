from django.core.mail import send_mail
from django.db.models import query
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead,Agent,Category
from django.http import HttpResponse
from django.views import generic
from .forms import LeadForm,LeadModelForm,CustomUserCreationForm
from agents.mixin import OrganizorLoginRequiredMixin
from .forms import AssignAgentForm,LeadCategoryUpdateForm
#CRUD Create Retrieve Update Delete  + List

def home_page(request):

   context ={
      "name":"小王",
      "age":99
   }
   return render(request,"second_page.html",context)

class UserCreationView(generic.CreateView):
   template_name="registration/signup.html"
   form_class = CustomUserCreationForm

   def get_success_url(self):
      return reverse("login")

class LandingPageView(generic.TemplateView):
   template_name="landing.html"

def landing_page(request):
   return render(request,"landing.html")

class LeadListView(LoginRequiredMixin,generic.ListView):
   template_name = "leads/lead_list.html"
   #queryset = Lead.objects.all()
   context_object_name="leads"

   def get_queryset(self):
      user = self.request.user
      #得到初始化的销售线索
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile,agent__isnull=False)
      else:
         queryset = Lead.objects.filter(organization=user.agent.organization,agent__isnull=False)
         queryset = queryset.filter(agent__user=user)
      return queryset
   
   def get_context_data(self,**kwargs):
      user = self.request.user      
      context = super(LeadListView,self).get_context_data()
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile,agent__isnull=True)
         context.update({
            "unassigned_leads":queryset
         })
      return context




def lead_list(request):
    leads = Lead.objects.all()
    context = {
       "leads":leads
    }
    return render(request,"leads/lead_list.html",context)

class LeadDetailView(LoginRequiredMixin,generic.DetailView):
   template_name = "leads/lead_detail.html"
   #queryset = Lead.objects.all()
   context_object_name = "lead"

   def get_queryset(self):
      user = self.request.user
      #得到初始化的销售线索
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile)
      else:
         queryset = Lead.objects.filter(organization=user.agent.organization)
         queryset = queryset.filter(agent__user=user)
      return queryset

def lead_detail(request,pk):
   lead = Lead.objects.get(id=pk)
   context={
      'lead':lead
   }
   return render(request,"leads/lead_detail.html",context)

class LeadCreateView(OrganizorLoginRequiredMixin,generic.CreateView):
   template_name="leads/lead_create.html"
   form_class = LeadModelForm

   def get_success_url(self):
      return reverse("leads:lead-list")

   def form_valid(self,form):
      lead = form.save(commit=False)
      lead.organization = self.request.user.userprofile
      lead.save()
      #todo 发邮件给管理员
      send_mail(
         subject="创建了一个新的线索",
         message="请尽快去查看",
         from_email="test@test.com",
         recipient_list=['test1@test.com']
      )
      return super(LeadCreateView,self).form_valid(form)

def lead_create(request):
   form = LeadModelForm()
   if request.POST:
      form = LeadModelForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect("/leads/")

   context = {
      'form':form
   }
   return render(request,"leads/lead_create.html",context)

# def lead_create(request):
#    form = LeadModelForm()
#    if request.POST:
#       form = LeadModelForm(request.POST)
#       if form.is_valid():
#          first_name = form.cleaned_data['first_name']
#          last_name = form.cleaned_data['last_name']
#          age = form.cleaned_data['age']
#          agent = Agent.objects.first()
#          Lead.objects.create(
#             first_name = first_name,
#             last_name = last_name,
#             age=age,
#             agent=agent
#          )
#          return redirect("/leads/")

#    context = {
#       'form':form
#    }
#    return render(request,"leads/lead_create.html",context)

class LeadUpdateView(OrganizorLoginRequiredMixin,generic.UpdateView):
   template_name="leads/lead_update.html"
   #queryset=Lead.objects.all()
   form_class = LeadModelForm

   def get_queryset(self):
      user = self.request.user
      #得到初始化的销售线索
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile)
      return queryset

   def get_success_url(self):
      return reverse("leads:lead-list")


def lead_update(request,pk):
   lead = Lead.objects.get(id=pk)
   form = LeadModelForm(instance=lead)
   if request.method == "POST":
      form = LeadModelForm(request.POST,instance=lead)
      if form.is_valid():
         form.save()
         return redirect('/leads/')
   context={
      'lead':lead,
      'form':form
   }
   return render(request,"leads/lead_update.html",context)

class LeadDeleteView(OrganizorLoginRequiredMixin,generic.DeleteView):
   template_name="leads/lead_delete.html"
   #queryset=Lead.objects.all()
   form_class = LeadModelForm

   def get_queryset(self):
      user = self.request.user
      #得到初始化的销售线索
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile)
      return queryset

   def get_success_url(self):
      return reverse("leads:lead-list")

def lead_delete(request,pk):
   lead = Lead.objects.get(id=pk)
   lead.delete()
   return redirect('/leads/')


class AssignAgentView(OrganizorLoginRequiredMixin,generic.FormView):
   template_name = 'leads/assign_agent.html'
   form_class = AssignAgentForm

   def get_form_kwargs(self,**kwargs):
      kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
      kwargs.update({
         "request":self.request
      })
      return kwargs

   def form_valid(self,form):
      agent = form.cleaned_data['agent']
      lead = Lead.objects.get(id=self.kwargs["pk"])
      lead.agent = agent
      lead.save()
      return super(AssignAgentView,self).form_valid(form)

   def get_success_url(self):
      return reverse("leads:lead-list")

class CatetoryListView(LoginRequiredMixin, generic.ListView):
   template_name = "leads/category_list.html"
   context_object_name = 'category_list'
   
   def get_queryset(self):
      user = self.request.user
      if user.is_organizor:
         queryset = Category.objects.filter(organization=user.userprofile)
      else:
         queryset = Category.objects.filter(organization=user.agent.organization)
      return queryset

   def get_context_data(self,**kwargs):
      context = super(CatetoryListView,self).get_context_data(**kwargs)
      user = self.request.user
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile)
      else:
         queryset = Category.objects.filter(organization=user.agent.organization)
      context.update({
         "unassigned_categories":queryset.filter(category__isnull=True).count()
      })
      return context

class CatetoryDetailView(generic.DetailView):
   template_name = "leads/category_detail.html"
   context_object_name = 'category'
   
   def get_queryset(self):
      user = self.request.user
      if user.is_organizor:
         queryset = Category.objects.filter(organization=user.userprofile)
      else:
         queryset = Category.objects.filter(organization=user.agent.organization)
      return queryset

   
   # def get_context_data(self,**kwargs):
   #    context = super(CatetoryDetailView,self).get_context_data(**kwargs)
   #    leads = self.get_object().leads.all()
   #    context.update({
   #       "leads":leads
   #    })
   #    return context

class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
   template_name = "leads/category_update.html"
   form_class = LeadCategoryUpdateForm

   def get_queryset(self):
      user = self.request.user
      #得到初始化的销售线索
      if user.is_organizor:
         queryset = Lead.objects.filter(organization=user.userprofile)
      else:
         queryset = Lead.objects.filter(organization=user.agent.organization)
         queryset = queryset.filter(agent__user=user)
      return queryset
   
   def get_success_url(self):
      return reverse("leads:lead-detail",kwargs={"pk":self.get_object().id})




