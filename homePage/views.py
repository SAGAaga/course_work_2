from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import *
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
from docxtpl import DocxTemplate
from datetime import datetime
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
import calendar
from datetime import datetime

from django.core.files import File

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
#from django.core.mail import EmailMessage
from email.message import EmailMessage
import mimetypes
import smtplib


class IndexView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        # avarage count contracts for singl accomodation
        contract_num = Contract.objects.all().count()
        acco_list = set()
        for contract in Contract.objects.all():
            acco_list.add(contract.accomodation)
        accomodation_num = len(acco_list)
        contract_for_accomodation = contract_num/accomodation_num
        more_or_actually = 'acctually one'
        if contract_for_accomodation > 1:
            more_or_actually = 'more then one'

        all_user_contracts = self.get_All_Contracts(request)['data']

        context = {
            'single_accomodation': contract_for_accomodation,
            'more_or_actually': more_or_actually, 'all_user_contracts': all_user_contracts}
        return render(request, 'homePage/HomePage.html', context=context)

    def get_All_Contracts(self, request):
        all_user_contracts = User.objects.get(
            username=request.user.username).contract_set.all().filter(is_activ=True)
        num = all_user_contracts.filter(term__year__lt=datetime.now().year).filter(
            term__month__lt=datetime.now().month).count()
        avg_sq = []
        for acc in all_user_contracts:
            temp = acc.accomodation.contract_set.all().count()
            if temp > 1:
                avg_sq.append(acc.accomodation)
        count = 0
        for acc in avg_sq:
            count += acc.squeare
        if len(avg_sq):
            avg_sq = count/len(avg_sq)
        else:
            avg_sq = 0
        context = {'data': all_user_contracts,
                   'term_data': num, 'avg_squer': avg_sq}
        return context


class All_Payments(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        payments_list = []
        all_user_contracts = User.objects.get(
            username=request.user.username).contract_set.all()

        for contract in all_user_contracts:
            payments = contract.payments_set.all()
            payments_list.append(payments)
        try:
            all_payments = payments_list[0]
        except IndexError as err:
            all_payments = []

        for payment in payments_list:
            all_payments = all_payments | payment

        #contracts = []
        # for contract in all_user_contracts:
            # contracts.append(contract.contract_number)
        #all_payments = Payments.objects.filter(contract_number__in=contracts)

        return render(request, 'homePage/All_Payments.html', context={'data': all_payments})


class Payment_info(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        payment = Payments.objects.get(payment_id=id)
        return render(request, 'homePage/Payment.html', context={'payment': payment})


class Payment_Delete(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        payment = Payments.objects.get(payment_id=id)
        payment.delete()
        return redirect('all_payments_url')


class Edit_Payment(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        user = User.objects.get(username=request.user.username)
        payment = Payments.objects.get(payment_id=id)
        form = Pay_form(user=user, initial={
                        'summ': payment.summ, 'contract_number': payment.contract_number})
        return render(request, 'homePage/edit.html', context={'form': form})

    def post(self, request, id):
        user = User.objects.get(username=request.user.username)
        boundform = Pay_form(request.POST, user=user)
        if boundform.is_valid():
            payment = Payments.objects.get(payment_id=id)
            payment.summ = request.POST['summ']
            payment.contract_number = Contract.objects.get(
                contract_number=request.POST['contract_number'])
            payment.save()
            return redirect('all_payments_url')
        else:
            return render(request, 'homePage/edit.html', context={'form': boundform})


class All_Contracts(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        all_user_contracts = User.objects.get(
            username=request.user.username).contract_set.all().filter(is_activ=True)
        num = all_user_contracts.filter(term__year__lt=datetime.now().year).filter(
            term__month__lt=datetime.now().month).count()
        avg_sq = []
        for acc in all_user_contracts:
            temp = acc.accomodation.contract_set.all().count()
            if temp > 1:
                avg_sq.append(acc.accomodation)
        count = 0
        for acc in avg_sq:
            count += acc.squeare
        if len(avg_sq):
            avg_sq = count/len(avg_sq)
        else:
            avg_sq = 0
        return render(request, 'homePage/All_Contracts.html',
                      context={'data': all_user_contracts, 'term_data': num, 'avg_squer': avg_sq})


class Contract_info(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        contract = Contract.objects.get(contract_number=id)
        return render(request, 'homePage/Contract.html', context={'contract': contract})


class Contract_Delete(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        contract = Contract.objects.get(contract_number=id)
        contract.is_activ = False
        contract.save()
        return redirect('all_contracts_url')


class Edit_Contract(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        user = User.objects.get(username=request.user.username)
        contract = Contract.objects.get(contract_number=id)
        form = Contract_form(initial={
            'contract_number': contract.contract_number, 'accomodation': contract.accomodation_id})
        return render(request, 'homePage/edit.html', context={'form': form})

    def post(self, request, id):
        user = User.objects.get(username=request.user.username)
        boundform = Contract_form(request.POST)
        contract = Contract.objects.get(contract_number=id)
        if request.POST['contract_number'] == id:
            contract.accomodation = Accomodation.objects.get(
                accomodation_id=request.POST['accomodation'])
            contract.contract_number = request.POST['contract_number']
            contract.save()
            return redirect('all_contracts_url')
        elif boundform.is_valid():
            contract.accomodation = Accomodation.objects.get(
                accomodation_id=request.POST['accomodation'])
            contract.contract_number = request.POST['contract_number']
            contract.save()
            return redirect('all_contracts_url')
        else:
            return render(request, 'homePage/edit.html', context={'form': boundform})


class Create_Contract(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = Contract_form()
        return render(request, 'homePage/edit.html', context={'form': form})

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        boundform = Contract_form(request.POST)
        if boundform.is_valid():
            contract = Contract(
                accomodation=Accomodation.objects.get(
                    accomodation_id=request.POST['accomodation']),
                contract_number=request.POST['contract_number'],
                user=user)
            contract.save()
            return redirect('all_contracts_url')
        else:
            return render(request, 'homePage/edit.html', context={'form': boundform})


class Discounts_View(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        discounts = User.objects.get(
            username=request.user.username).discount_set.all()
        disc_num = set()
        users_disc = Client_Discount.objects.all()
        for user in users_disc:
            disc_num.add(user.user)
        ln = len(disc_num)*100
        disc_num = ln/User.objects.all().count()
        return render(request, 'homePage/discounts.html', context={'data': discounts, 'disc_num': disc_num})


class Discount_View(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        discount = User.objects.get(
            username=request.user.username).discount_set.all().get(discount_id=id)
        return render(request, 'homePage/discount.html', context={'discount': discount})


class Discount_Delete(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        discount = User.objects.get(
            username=request.user.username).discount_set.all().get(discount_id=id)
        discount.delete()
        return redirect('discounts_url')


class Discount_Edit(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        user = User.objects.get(username=request.user.username)
        discount = Discount.objects.get(discount_id=id)
        form = Discount_form(initial={
            'name': discount.name, 'pecent_of_discount': discount.pecent_of_discount})
        return render(request, 'homePage/edit.html', context={'form': form})

    def post(self, request, id):
        user = User.objects.get(username=request.user.username)
        boundform = Discount_form(request.POST)
        discount = Discount.objects.get(discount_id=id)
        if boundform.is_valid():
            discount.pecent_of_discount = request.POST['pecent_of_discount']
            discount.name = request.POST['name']
            discount.save()
            return redirect('discounts_url')
        else:
            return render(request, 'homePage/edit.html', context={'form': boundform})


class Discount_Add(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = Discount_form()
        return render(request, 'homePage/edit.html', context={'form': form})

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        boundform = Discount_form(request.POST)
        if boundform.is_valid():
            discount = Discount(
                pecent_of_discount=request.POST['pecent_of_discount'],
                name=request.POST['name'])
            discount.save()
            discount.user.add(user)
            return redirect('discounts_url')
        else:
            return render(request, 'homePage/edit.html', context={'form': boundform})


class Pay(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = Pay_form(user=user)
        return render(request, 'homePage/pay.html', context={'form': form})

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        boundform = Pay_form(request.POST, user=user)
        if boundform.is_valid():
            new_payment = boundform.save()
            return redirect('payment_report_url', id=new_payment.payment_id)
        else:
            return render(request, 'homePage/pay.html', context={'form': boundform})


class Make_Payment_Report(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        payment = Payments.objects.get(payment_id=id)
        user = User.objects.get(username=request.user.username)
        street = Accomodation.objects.get(accomodation_id=Contract.objects.get(
            contract_number=payment.contract_number).accomodation_id)
        template = get_template('reports/payment_tpl.html')
        context = {'date': datetime.now().date(), 'pay_date': datetime.date(payment.pay_datetime), 'payment': payment,
                   'user': user,
                   'street': street}
        html = template.render(context)
        pdf = render_to_pdf(
            template_src='reports/payment_tpl.html', content_dict=context)
        if pdf:

            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse('Not found')


class Make_Report_Contract(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request, id):
        contract = Contract.objects.get(contract_number=id)
        payments = contract.payments_set.all()
        user = User.objects.get(username=request.user.username)
        template = get_template('reports/contract_tpl.html')
        context = {'date': datetime.now().date(), 'payments': payments,
                   'user': user, 'contract': contract}
        html = template.render(context)
        pdf = render_to_pdf(
            template_src='reports/contract_tpl.html', content_dict=context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse('Not found')


def render_to_pdf(template_src, content_dict={}):
    template = get_template(template_src)
    html = template.render(content_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('ISO-8859-1')), result)
    if not pdf.err:
        #spdf = result.getvalue().decode('windows-1252').encode("utf-8")
        filename = 'mypdf.pdf'
        with open(filename, 'wb') as f:
            f.write(result.getvalue())

        msg = EmailMessage()

        msg['Subject'] = 'REPORT!'
        msg['From'] = 'ringoosringoo123@gmail.com'
        msg['To'] = 'nikita.sahaidachnyi@nure.ua'

        #msg.set_content('This is a plain text email')

        msg.add_attachment(result.getvalue(), maintype='application',
                           subtype='octet-stream', filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('ringoosringoo123@gmail.com', 'Ring123oo')
            smtp.send_message(msg)

        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None


class Automatization(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_url')

    def get(self, request):
        users = User.objects.filter()
        dataa = {}
        for user in users:
            dataa[user] = {}
            payments_list = []
            for contract in user.contract_set.all():
                payments_list.append(contract.payments_set.all())
            try:
                all_payments = payments_list[0]
            except IndexError as err:
                all_payments = []

            for payment in payments_list:
                all_payments = all_payments | payment
            dataa[user]['data'] = all_payments

            month_info = {}
            for i in range(1, 13):
                for da in dataa[user]['data']:
                    if da.pay_datetime.month == i:
                        try:
                            month_info[i] += 1
                        except KeyError:
                            month_info[i] = 1
                        try:
                            dataa[user][i] += da.summ
                        except KeyError:
                            dataa[user][i] = da.summ
            for i in range(1, 13):
                try:
                    temp = dataa[user][i]
                except KeyError:
                    dataa[user][i] = 0

        trow = []
        count = 0
        for user in dataa.keys():
            trow.append([user])
            for i in range(1, 13):
                trow[count].append(dataa[user][i])
            count += 1
        template = get_template('reports/automatization.html')
        monthes = []
        for i in range(1, 13):
            monthes.append(calendar.month_name[i])
        context = {'date': datetime.now().date(), 'data': dataa,
                   'monthes': monthes, 'trow': trow}
        html = template.render(context)
        pdf = render_to_pdf(
            template_src='reports/automatization.html', content_dict=context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse('Not found')
