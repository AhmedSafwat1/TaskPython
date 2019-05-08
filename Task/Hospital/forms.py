from django.forms import ModelForm

from .models import *


class RequestBloodForm(ModelForm):
    class Meta:
        model = RequestBlood
        fields = ('blood_type', 'patients_status', 'quantity', 'hospital')
