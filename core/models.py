from datetime import datetime

from django.db import models

CAR = (
    ('O', 'ÔNIBUS'),
    ('C', 'CARRO'),
    ('V', 'VAN'),
    ('A', 'AMBULÂNCIA')
)
SEX = (
    ('M', 'MASCULINO'),
    ('F', 'FEMININO')
)
HOUR_CHOICES = (
    (datetime.strptime('07:00:00', '%H:%M:%S').time(), '07:00'),
    (datetime.strptime('08:00:00', '%H:%M:%S').time(), '08:00'),
    (datetime.strptime('09:00:00', '%H:%M:%S').time(), '09:00'),
    (datetime.strptime('10:00:00', '%H:%M:%S').time(), '10:00'),
    (datetime.strptime('11:00:00', '%H:%M:%S').time(), '11:00'),
    (datetime.strptime('12:00:00', '%H:%M:%S').time(), '12:00'),
    (datetime.strptime('13:00:00', '%H:%M:%S').time(), '13:00'),
    (datetime.strptime('14:00:00', '%H:%M:%S').time(), '14:00'),
    (datetime.strptime('15:00:00', '%H:%M:%S').time(), '15:00'),
    (datetime.strptime('16:00:00', '%H:%M:%S').time(), '16:00')
)


class UserRegister(models.Model):
    cns = models.CharField('Cartão SUS', max_length=18, blank=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    reference = models.CharField('Referência', max_length=30, blank=True)
    birth = models.CharField('Data de Nascimento', max_length=10, blank=True)
    sex = models.CharField('Sexo', max_length=1, choices=SEX, blank=True)
    address = models.CharField('Endereço', max_length=100, blank=True)
    telephone = models.CharField('Telefone', max_length=15, blank=True)

    class Meta:
        verbose_name = 'Cadastro de Usuário'
        verbose_name_plural = 'Cadastro de Usuários'

    def __str__(self):
        return self.name
