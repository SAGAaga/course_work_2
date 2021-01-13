from django.forms import ValidationError
from django.forms import ModelForm
from .models import *
from user.models import *
from django.contrib.auth.models import User
from datetime import datetime


class Pay_form(ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Pay_form, self).__init__(*args, **kwargs)
        contracts = user.contract_set.all().order_by('-contract_number')
        self.fields['contract_number'].queryset = contracts

    def save(self, commit=True, *args, **kwargs):
        user = kwargs.pop('user', None)
        boundform = super(Pay_form, self).save(
            commit=False, *args, **kwargs)
        status = boundform.contract_number.accomodation.status_set.all().order_by(
            "date_in").last()
        if status:
            debt = status.debt
            prepayment = status.prepayment
            consumed = status.consumed
        else:
            debt = 0
            prepayment = 0
            consumed = 0

        if debt <= boundform.summ:
            prepayment += boundform.summ-debt
            debt = 0
        else:
            debt -= boundform.summ

        new_status = Status(consumed=consumed, debt=debt, prepayment=prepayment, date_in=datetime.now(),
                            accomodation_id=boundform.contract_number.accomodation)
        new_status.save()
        boundform.save()
        return boundform

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
        # fields = ['name', 'pecent_of_discount']


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

    def clean_consumed(self):
        consumed = self.cleaned_data['consumed']
        accomodation_id = self.data['accomodation_id']
        status = Accomodation.objects.get(
            accomodation_id=accomodation_id).status_set.all().order_by('date_in').last()
        if status:
            if consumed <= status.consumed:
                raise ValidationError(
                    'Current consumed must be greater then last status.')
        return consumed

    def save(self, commit=True, *args, **kwargs):
        user = kwargs.pop('user', None)
        boundform = super(Status_form, self).save(
            commit=False, *args, **kwargs)

        boundform.date_in = datetime.now()
        accomodation_id = self.data['accomodation_id']
        status = Accomodation.objects.get(
            accomodation_id=accomodation_id).status_set.all().order_by('date_in').last()

        if status:
            difference = boundform.consumed-status.consumed
        else:
            difference = boundform.consumed

        tarif = Tarif.objects.get(
            bottom_line__lte=difference, top_line__gt=difference)
        discount = user.discount_set.all().order_by('pecent_of_discount').last()
        coeff = 1
        if boundform.date_in.month < 4 and boundform.date_in.month > 9:
            coeff = 1.5

        boundform.tarif = tarif
        if status:
            boundform.debt = status.debt+tarif.price*difference * \
                coeff*(1-discount.pecent_of_discount/100)
            boundform.prepayment = status.prepayment
        else:
            boundform.debt = tarif.price*difference * \
                coeff*(1-discount.pecent_of_discount/100)
            boundform.prepayment = 0

        if boundform.prepayment >= boundform.debt:
            boundform.prepayment -= boundform.debt
            boundform.debt = 0
        else:
            boundform.debt -= boundform.prepayment
            boundform.prepayment = 0

        #  unhandled error !!!!  of difference greater the maximum in tarif.top_line
        if commit:
            boundform.save()
        return boundform

    class Meta:
        model = Status
        fields = ['consumed', 'accomodation_id']
