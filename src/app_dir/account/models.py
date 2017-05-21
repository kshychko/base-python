from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from app_dir.utils.models import BaseUUIDModel
from app_dir.address.models import Suburb, State, Country


User = get_user_model()


class UserRole(models.Model):
    """ Representation of User Roles. """

    name = models.CharField(max_length=20, help_text=_('Role Name'))

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')

    def __str__(self):
        return self.name

class Account(models.Model):
    """ Representation of User account. """

    user = models.OneToOneField(User, help_text=_('User'), related_name='account')
    role = models.ForeignKey(UserRole, help_text=_('Role'))

    class Meta:
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')

    def __str__(self):
        return f"{self.user} at {self.role}"

    @property
    def draft_application(self):
        from app_dir.permit.models import Application
        draft, created =  Application.objects.get_or_create(
            applicant_account=self,
            is_draft=True
        )

        return draft