from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _

from exclusivebooleanfield.fields import ExclusiveBooleanField

from app_dir.utils.models import BaseUUIDModel
from app_dir.utils.enum import enum
from app_dir.address.models import Suburb
from app_dir.account.models import Account


GENUS = enum(MALE=1, FEMALE=2)
GENUS.CHOICES = (
   (GENUS.MALE, _('Male')),
   (GENUS.FEMALE, _('Female'))
)

class Application(BaseUUIDModel):
    """ Representation of Permit Application. """

    STATUS_NEW, STATUS_PENDING, STATUS_APPROVED = range(1, 4)
    STATUS_CHOICES = (
        (STATUS_NEW, _('New')),
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved'))
    )

    applicant = JSONField(default={}, help_text=_('Applicant'))
    agent = JSONField(default={}, help_text=_('Agent'))
    recipient = JSONField(default={}, help_text=_('Recipient'))
    transport = JSONField(default={}, help_text=_('Transport'))
    goods_a = JSONField(default={}, help_text=('Goods (A)'))
    goods_b = JSONField(default={}, help_text=_('Goods (B)'))

    applicant_name = models.CharField(max_length=70, blank=True, help_text=_('Applicant Name'))
    permit_number = models.CharField(max_length=10, blank=True, help_text=_('Permit No'))

    valid_from = models.DateField(null=True, blank=True, help_text=_('Valid From'))
    valid_to = models.DateField(null=True, blank=True, help_text=_('Valid To'))

    applicant_account = models.ForeignKey(
        Account,
        related_name='applicant_account',
        help_text=_('Applicant Account'),
        null=True,
        blank=True
    )

    assessor = models.ForeignKey(
        Account,
        related_name='accessor',
        help_text=_('Assessor'),
        null=True,
        blank=True
    )
    assessment_date = models.DateField(null=True, blank=True, help_text=_('Assessment Date'))
    assessment = models.TextField(blank=True, help_text=_('Assessment'))

    delegate = models.ForeignKey(
        Account,
        related_name='delegate',
        help_text=_('Delegate'),
        null=True,
        blank=True
    )
    delegate_date = models.DateField(null=True, blank=True, help_text=_('Delegate Date'))

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW, help_text=_('Status'))

    is_draft = ExclusiveBooleanField(on=('applicant_account'), default=False)

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __str__(self):
        return self.permit_number


class ApplicationStatusChange(BaseUUIDModel):
    """ Representation of Application status changes log. """

    application = models.ForeignKey(Application, help_text=_('Application'))
    staff = models.ForeignKey(Account, help_text=_('Staff Account'))

    action_date = models.DateField(help_text=_('Date of action'))
    new_status = models.SmallIntegerField(choices=Application.STATUS_CHOICES, help_text=_('New status set'))
    notes = models.TextField(help_text=_('Notes'))

    class Meta:
        verbose_name = _('Application Status Change')
        verbose_name_plural = _('Application Status Changes')

    def __str__(self):
        return self.action_date


class Inspections(BaseUUIDModel):
    application = models.ForeignKey(Application, blank=True, null=True, related_name='inspections')
    inspection_officer = models.ForeignKey(Account, blank=True, null=True, related_name='inspections')
    inspection_date = models.DateField(auto_now_add=True, help_text=_("Inspection date"))
    findings = models.CharField(max_length=200, default='', help_text=_("Findings"))

    # maybe we should make it boolean or integer choice field?
    status = models.CharField(max_length=50, default='', help_text=_("Status"))
    biosecurity_concerns = models.TextField(max_length=400, default='', help_text=_("Biosecurity concerns"))
    noncompliance_details = models.TextField(max_length=400, default='', help_text=_("Noncompliance Details"))

    goods_a = JSONField(default={}, help_text=('Goods (A)'))
    goods_b = JSONField(default={}, help_text=_('Goods (B)'))

    class Meta:
        verbose_name = _('Inspection')
        verbose_name_plural = _('Inspections')

    def __str__(self):
        return ' '.join([self.inspection_date, self.status])


class FileStorage(BaseUUIDModel):
    # TBD
    upload = models.FileField(upload_to='uploads/')

    class Meta:
        verbose_name = _('File Storage')
        verbose_name_plural = _('File Storages')


class SupportingFiles(BaseUUIDModel):
    file_type = models.CharField(max_length=50, default='', help_text=_("Supported files type"))
    file_storage = models.ForeignKey('FileStorage', help_text=_("File"))

    class Meta:
        verbose_name = _('Supporting File')
        verbose_name_plural = _('Supporting Files')

    def __str__(self):
        return self.type
