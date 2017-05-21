from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from app_dir.permit.models import Application


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput, label=_(u'Email'))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                _("Authentication failed. Please try again.")
            )
        return self.cleaned_data


class ApplicantForm(forms.ModelForm):
    agree = forms.CharField(
        widget=forms.CheckboxInput,
        required=False,
        label=_('I am an agent acting on behalf of this applicant')
    )

    class Meta:
        model = Application
        fields = [
            'applicant',
        ]


class AgentForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'agent',
        ]


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'recipient',
        ]


class TransportForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'transport',
        ]


class GoodsAForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'goods_a',
        ]


class GoodsBForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'goods_b',
        ]
