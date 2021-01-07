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
        super(Contract_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        fields = ['contract_number', 'accomodation']


class Discount_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Discount_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Discount
        exclude = ('discount_id', 'user')
        #fields = ['name', 'pecent_of_discount']


class Accomodation_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Accomodation_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Accomodation
        fields = ['address', 'squeare']


class Status_form(ModelForm):
    def __init__(self, *args, **kwargs):
        accomodation_set = kwargs.pop('accomodation', None)
        super(Status_form, self).__init__(*args, **kwargs)
        self.fields['accomodation_id'].queryset = accomodation_set

    class Meta:
        model = Status
        fields = ['consumed', 'accomodation_id']
