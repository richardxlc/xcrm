import random
from django.core.mail import send_mail
from django.views import generic
from leads.models import Agent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from .forms import AgentForm
from .mixin import OrganizorLoginRequiredMixin

class AgentListView(OrganizorLoginRequiredMixin,generic.ListView):
    template_name="agents/agent-list.html"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

class AgentCreateView(OrganizorLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent-create.html"
    form_class = AgentForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(f"{random.randint(0,100000)}")
        user.is_organizor = False
        user.is_agent = True
        user.save()
        Agent.objects.create(user=user,organization=self.request.user.userprofile)
        send_mail(
            subject="CRM 邀请邮件",
            from_email='admin@test.com',
            recipient_list=[user.email],
            message="您已被邀请进入CRM系统，请及时登录并开始工作 "
        )
        return super(AgentCreateView,self).form_valid(form)


class AgentDetailView(OrganizorLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent-detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentUpdateView(OrganizorLoginRequiredMixin,generic.UpdateView):
    template_name = "agents/agent-update.html"
    form_class = AgentForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

class AgentDeleteView(OrganizorLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent-delete.html"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    
