import locale
from calendar import month_name, monthrange
from datetime import date, datetime
from io import BytesIO
from math import ceil
from re import match
from subprocess import PIPE, Popen
from wsgiref.util import FileWrapper

from PyPDF2 import PdfFileReader, PdfFileWriter
from django.contrib.staticfiles import finders
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from core import models


class Valid:

    def __init__(self, cns=None, birth=None, telephone=None, area=None):
        self.cns = cns
        self.birth = birth
        self.telephone = telephone
        self.area = area

    def valid_cns(self):
        return match(r'^[1-2]\d{2}\s\d{4}\s\d{4}\s00[0-1]\d$', self.cns) or \
               match(r'^[7-9]\d{2}\s\d{4}\s\d{4}\s\d{4}$', self.cns) and \
               self.ponders() % 11 == 0

    def ponders(self):
        amount = 0
        counter = 15
        for value in self.cns.replace(' ', ''):
            if value is not None:
                amount += int(value) * counter
                counter -= 1
        return amount

    def valid_telephone(self):
        return match(r'\(\d{2}\)\s\d?\d{4}\-\d{4}', self.telephone)

    def valid_birth(self):
        return match(r'\d{2}\/\d{2}\/\d{4}', self.birth)


class GetCNS(View):

    def get(self, request):
        cns = request.GET.get('cns')
        user = request.GET.get('user')
        marking = request.GET.get('marking')
        if user:
            data = serialize('json', models.UserRegister.objects.all())
        elif marking:
            data = serialize('json', models.List.objects.filter(cns=cns))
        else:
            data = serialize('json', models.UserRegister.objects.filter(cns=cns))
        return HttpResponse(data)


class PrintList(View):

    def get(self, request, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, "pt_BR.utf-8")
        year = kwargs["year"]
        month = kwargs["month"]
        day = kwargs["day"]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Lista de Viagens - {}.{}.{}.pdf".format(day, month, year)'
        list_all = models.List.objects.filter(date__day=day, date__month=month, date__year=year)
        self.position = 25.5 * cm
        self.per_page = 5
        self.page = 1
        pdf1 = BytesIO()
        pdf2 = BytesIO()
        pdf3 = BytesIO()
        self.tmp_pdf1 = canvas.Canvas(pdf1, pagesize=A4)
        for car in models.CarType.objects.all():
            passenger = 0
            companion = 0
            for n in list_all.filter(car=car):
                passenger += 1
                companion += n.companion
            self.counter = passenger
            if passenger > 0:
                for listed in list_all.filter(car=car):
                    self.write_list(car, listed, passenger, companion)
                if not int(passenger / 5):
                    self.tmp_pdf1.showPage()
                    self.position = 25.5 * cm
                    self.per_page = 5
                    self.page = 1
        self.tmp_pdf1.save()
        read_pdf1 = PdfFileReader(pdf1)
        total_pages = read_pdf1.getNumPages()
        file = finders.find('pdf/file.pdf')
        read_pdf_base = PdfFileReader(open(file, "rb"))
        output = PdfFileWriter()
        output2 = PdfFileWriter()
        page = read_pdf_base.getPage(0)
        for total in range(total_pages):
            output.addPage(page)
        output.write(pdf2)
        read_pdf2 = PdfFileReader(pdf2)
        for total in range(total_pages):
            page = read_pdf2.getPage(total)
            page.mergePage(read_pdf1.getPage(total))
            output2.addPage(page)
        output2.write(pdf3)
        response.write(pdf3.getvalue())
        pdf1.close()
        pdf2.close()
        pdf3.close()
        response['Content-Disposition'] = 'inline; filename=agenda-de-viagem_{}-{}-{}.pdf'.format(day, month, year)
        return response

    def write_list(self, car, listed, passenger, companion):
        name = listed.name.split(' ')
        name_size = len(name)
        address = listed.address.split(' ')
        address_size = len(name)
        while len(listed.name) > 28:
            if len(name[name_size - 2]) > 3:
                listed.name = listed.name.replace(name[name_size - 2], name[name_size - 2][0])
            name_size -= 1
        while len(listed.address) > 25:
            if len(address[address_size - 2]) > 3:
                listed.address = listed.address.replace(address[address_size - 2], address[address_size - 2][0])
            address_size -= 1
        if self.per_page == 5:
            self.tmp_pdf1.setFont("Times-Bold", 14)
            self.tmp_pdf1.drawString(A4[0] / 2 + 1.4 * cm, self.position + cm, '{}'.format(car))
            self.tmp_pdf1.drawCentredString(
                A4[0] / 2, self.position + 0.55 * cm,
                '{} de {} de {} - Total {} - Passageiros {} - Acompanhantes {} - Página {} de {}'.format(
                    listed.date.day, month_name[listed.date.month].title(),
                    listed.date.year, passenger + companion, passenger, companion, self.page, ceil(passenger / 5)
                )
            )
        self.tmp_pdf1.setFont("Times-BoldItalic", 14)
        self.tmp_pdf1.drawString(2.25 * cm, self.position, '{} {}'.format(self.counter, listed.name))
        self.tmp_pdf1.drawString(15.8 * cm, self.position - 2.9 * cm, listed.cns)
        if len(listed.reference) > 12:
            self.tmp_pdf1.drawString(15.35 * cm, self.position, listed.reference[:13])
            self.tmp_pdf1.drawString(13 * cm, self.position - 0.57 * cm, listed.reference[13:])
        else:
            self.tmp_pdf1.drawString(15.35 * cm, self.position, listed.reference)
        self.tmp_pdf1.drawString(3.15 * cm, self.position - 0.57 * cm, listed.address)
        self.tmp_pdf1.drawString(2.8 * cm, self.position - 1.14 * cm, listed.local)
        self.tmp_pdf1.drawString(14.75 * cm, self.position - 1.14 * cm, str(listed.get_hour_display()))
        self.tmp_pdf1.drawString(16.5 * cm, self.position - 1.14 * cm, listed.telephone)
        self.tmp_pdf1.drawString(3.4 * cm, self.position - 1.71 * cm, listed.goal)
        self.tmp_pdf1.drawString(13.9 * cm, self.position - 1.71 * cm, listed.note)
        self.tmp_pdf1.drawString(7.7 * cm, self.position - 2.28 * cm, listed.search)
        self.tmp_pdf1.drawCentredString(5.34 * cm, self.position - 3.41 * cm, str(listed.companion))
        self.position -= 4.89 * cm
        self.per_page -= 1
        self.counter -= 1
        if self.per_page == 0:
            self.tmp_pdf1.showPage()
            self.page += 1
            self.per_page = 5
            self.position = 25.5 * cm


def named_month(month_number):
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')
    return date(1900, month_number, 1).strftime('%B').title()


def this_month(request):
    today = datetime.now()
    return calendar(request, today.year, today.month)


def calendar(request, year, month):
    my_year = int(year)
    my_month = int(month)
    my_calendar_from_month = datetime(my_year, my_month, 1)
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1])
    my_events = models.List.objects.filter(date__gte=my_calendar_from_month).filter(date__lte=my_calendar_to_month)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1
    return render(request, 'core.vacancy.html', {
        'event_list': my_events, 'month': my_month,
        'month_name': named_month(my_month), 'year': my_year,
        'previous_month': my_previous_month,
        'previous_month_name': named_month(my_previous_month),
        'previous_year': my_previous_year, 'next_month': my_next_month,
        'next_month_name': named_month(my_next_month),
        'next_year': my_next_year, 'year_before_this': my_year_before_this,
        'year_after_this': my_year_after_this
    })


def folder(request):
    file = finders.find('pdf/file.pdf')
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Folha Extra.pdf'
    return response


def tag(request):
    file = finders.find('pdf/tag.pdf')
    wrapper = FileWrapper(open(file, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Etiquetas.pdf'
    return response
