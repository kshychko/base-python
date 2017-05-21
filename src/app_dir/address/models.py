from django.db import models
from django.utils.translation import ugettext_lazy as _


class Suburb(models.Model):
    """ Suburb/Town. """

    name = models.CharField(max_length=35)

    class Meta:
        verbose_name = _('Suburb/Town')
        verbose_name_plural = _('Suburbs/Towns')

    def __str__(self):
        return self.name

class State(models.Model):
    """ State. """

    name = models.CharField(max_length=35)

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')

    def __str__(self):
        return self.name

class Country(models.Model):
    """ Country. """

    name = models.CharField(max_length=70)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name