from django.forms import ModelForm
from .models import *
from user.models import *
from django.contrib.auth.models import User


class Pay_form(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Pay_form, self).__init__(*args, **kwargs)
        contracts = user.contract_set.all().order_by('-contract_number')
        self.fields['contract_number'].queryset = contracts

    class Meta:
        model = Payments
        fields = ['summ', 'contract_number']


class Contract_form(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Contract_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        fields = ['contract_number', 'accomodation']


class Discount_form(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Discount_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Discount
        exclude = ('discount_id', 'user')
        #fields = ['name', 'pecent_of_discount']
