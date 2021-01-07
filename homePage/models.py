from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from user.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Accomodation(models.Model):
    accomodation_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    squeare = models.IntegerField(validators=[
        MinValueValidator(1)
    ])

    def __str__(self):
        return self.address


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    # in current month
    consumed = models.IntegerField(validators=[MinValueValidator(0)])
    debt = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    prepayment = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    date_in = models.DateTimeField(auto_now_add=True)
    accomodation_id = models.ForeignKey(
        Accomodation, on_delete=models.CASCADE)


def getDateTime():
    return datetime.now()


def getTerm(term=6):
    return datetime.now().date()+relativedelta(months=term)


class Contract (models.Model):
    contract_number = models.CharField(primary_key=True, max_length=8, validators=[RegexValidator(
        regex='^\d{8}$', message='Length has to be 8', code='Incorrect length')])
    last_date_of_prolongation = models.DateField(auto_now=True)
    term = models.DateField(default=getTerm())
    is_activ = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accomodation = models.ForeignKey(Accomodation, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.term = getTerm()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.contract_number


class Tarif(models.Model):
    tarif_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    bottom_line = models.IntegerField(validators=[MinValueValidator(0)])
    top_line = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.IntegerField(validators=[MinValueValidator(1)])
    accomodation = models.ManyToManyField(
        Status, through='Tarif_Status', through_fields=('tarif_id', 'status_id'))

    def __str__(self):
        return self.name


class Tarif_Status(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE)


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True)
    summ = models.IntegerField(validators=[MinValueValidator(0)])
    pay_datetime = models.DateTimeField(auto_now_add=True)
    contract_number = models.ForeignKey(
        Contract, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payment_id)
