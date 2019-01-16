import locale
from calendar import month_name, monthrange
from datetime import date, datetime
from io import BytesIO
from math import ceil
from re import match
from subprocess import PIPE, Popen
from wsgiref.util import FileWrapper

from django.contrib.staticfiles import finders
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from PyPDF2 import PdfFileReader, PdfFileWriter
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
