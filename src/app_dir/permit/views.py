import os

from django.contrib.auth.views import login
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from formtools.wizard.views import SessionWizardView

from app_dir.permit import forms


class HomeView(TemplateView):
    template_name = 'home.html'


class LoginView(TemplateView):
    template_name = 'login.html'
    form = forms.LoginForm()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        self.form = forms.LoginForm(request.POST or None)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request):
        if self.form.is_valid():
            login(request, request.user)
            return redirect('home')
        return self.get(request)


class ApplicationWizardView(SessionWizardView):
    form_list = [
        ('application', forms.ApplicantForm),
        ('agent', forms.AgentForm),
        ('recipient', forms.RecipientForm),
        ('transport', forms.TransportForm),
        ('goods_a', forms.TransportForm),
        ('goods_b', forms.TransportForm)
    ]

    templates_list = {
        'application': 'permit.html',
        'agent': 'permit.html',
        'recipient': 'permit.html',
        'transport': 'permit.html',
        'goods_a': 'permit.html',
        'goods_b': 'permit.html',
    }

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'applications'))

    def get_template_names(self):
        return [self.templates_list[self.steps.current]]

    def get_form_instance(self, step):
        # Let's use the draft only for authenticated user
        if self.request.user.is_authenticated():
            draft = self.request.user.account.draft_application
            if draft:
                return draft

        return self.instance_dict.get(step, None)  # the default implementation

    def done(self, form_list, form_dict, **kwargs):
        # We are going to create a new application for every goods a/b

        return redirect('/')


class ApplicantView(TemplateView):
    template_name = 'permit.html'
    form = forms.ApplicantForm()

    def dispatch(self, request, *args, **kwargs):
        self.form = forms.ApplicantForm(request.POST or None)
        return super(ApplicantView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApplicantView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        # TODO: save form
        if request.POST.get('next'):
            return redirect(reverse('agent'))
        return self.get(request, *args, **kwargs)


class AgentView(TemplateView):
    template_name = 'permit.html'
    form = forms.AgentForm()

    def dispatch(self, request, *args, **kwargs):
        self.form = forms.AgentForm(request.POST or None)
        return super(AgentView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AgentView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        # TODO: save form
        if request.POST.get('next'):
            return redirect(reverse('recipient'))
        if request.POST.get('previous'):
            return redirect(reverse('applicant'))
        return self.get(request, *args, **kwargs)


class RecipientView(TemplateView):
    template_name = 'permit.html'
    form = forms.RecipientForm()

    def dispatch(self, request, *args, **kwargs):
        self.form = forms.RecipientForm(request.POST or None)
        return super(RecipientView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecipientView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        # TODO: save form
        if request.POST.get('next'):
            return redirect(reverse('transport'))
        if request.POST.get('previous'):
            return redirect(reverse('agent'))
        return self.get(request, *args, **kwargs)


class TransportView(TemplateView):
    template_name = 'permit.html'
    form = forms.TransportForm()

    def dispatch(self, request, *args, **kwargs):
        self.form = forms.TransportForm(request.POST or None)
        return super(TransportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransportView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        # TODO: save form
        if request.POST.get('next'):
            return redirect(reverse('goods'))
        if request.POST.get('previous'):
            return redirect(reverse('agent'))
        return self.get(request, *args, **kwargs)


class GoogdsView(TemplateView):
    template_name = 'googds.html'
    form_option_a = forms.GoodsAForm()
    form_option_b = forms.GoodsBForm()

    def dispatch(self, request, *args, **kwargs):
        self.form_option_a = forms.OptionAForm(request.POST or None)
        self.form_option_b = forms.OptionBForm(request.POST or None)
        return super(GoogdsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoogdsView, self).get_context_data(**kwargs)
        context['form_option_a'] = self.form_option_a
        context['form_option_b'] = self.form_option_b
        return context
