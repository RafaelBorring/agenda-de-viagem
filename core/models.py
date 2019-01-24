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
    enable = models.BooleanField('Ativo', default=True)
    create_on = models.DateField('Criado em:', auto_now_add=True, blank=True)
    update_on = models.DateField('Atualizado em:', auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cadastro de Usuário'
        verbose_name_plural = 'Cadastro de Usuários'


class List(models.Model):
    cns = models.CharField('Cartão SUS', max_length=18, blank=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    reference = models.CharField('Referência', max_length=30, blank=True)
    address = models.CharField('Endereço', max_length=100, blank=True)
    local = models.CharField('Destino', max_length=23, blank=True)
    date = models.DateField('Data', blank=True)
    hour = models.TimeField('Hora', default='07:00:00', choices=HOUR_CHOICES, blank=True)
    car = models.ForeignKey('CarType', on_delete=models.CASCADE, verbose_name='Tipo', blank=True)
    telephone = models.CharField('Telefone', max_length=15, blank=True)
    goal = models.CharField('Finalidade', max_length=23, blank=True)
    search = models.CharField('Local onde pegará o transporte', max_length=30, blank=True)
    note = models.CharField('Observação', max_length=15, blank=True)
    companion = models.DecimalField('Acompanhante', default=0, blank=True, max_digits=2, decimal_places=0)
    create_on = models.DateField('Criado em:', auto_now_add=True, blank=True)
    update_on = models.DateField('Atualizado em:', auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lista de Passageiros'
        verbose_name_plural = 'Listas de Passageiros'


class Holiday(models.Model):
    name = models.CharField('Feriado de', max_length=50)
    date = models.DateField('Dia', unique=True)
    create_on = models.DateField('Criado em:', auto_now_add=True, blank=True)
    update_on = models.DateField('Atualizado em:', auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'


class City(models.Model):
    name = models.CharField('Município', max_length=50, unique=True)
    enable = models.BooleanField('Ativo', default=True)
    create_on = models.DateField('Criado em:', auto_now_add=True, blank=True)
    update_on = models.DateField('Atualizado em:', auto_now=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'


class CarType(models.Model):
    description = models.CharField('Descrição', max_length=50, unique=True)
    type = models.CharField('Tipo', max_length=1, choices=CAR)
    destiny = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Destino')
    vacancy = models.DecimalField('N° de Vagas', max_digits=2, decimal_places=0)
    enable = models.BooleanField('Ativo', default=True)
    create_on = models.DateField('Criado em:', auto_now_add=True, blank=True)
    update_on = models.DateField('Atualizado em:', auto_now=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
