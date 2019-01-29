from django import forms
from django.contrib import admin

from core import models, views


class UserRegisterForm(forms.ModelForm):
    message = 'Habilite o javascript!'

    def clean_cns(self):
        cns = self.cleaned_data.get('cns')
        if not views.Valid(cns=cns).valid_cns() or models.UserRegister.objects.filter(cns=cns):
            raise forms.ValidationError(self.message)
        return cns

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isupper():
            raise forms.ValidationError(self.message)
        return name

    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        if not views.Valid(birth=birth).valid_birth():
            raise forms.ValidationError(self.message)
        return birth

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address.isupper():
            raise forms.ValidationError(self.message)
        return address

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            if not views.Valid(telephone=telephone).valid_telephone():
                raise forms.ValidationError(self.message)
        return telephone

    class Meta:
        model = models.UserRegister
        fields = '__all__'
        exclude = ('enable',)


class ListForm(forms.ModelForm):
    message = 'Habilite o javascript!'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = models.CarType.objects.exclude(enable=False)

    def clean(self):
        cns = self.cleaned_data.get('cns')
        date = self.cleaned_data.get('date')
        car = self.cleaned_data.get('car')
        companion = self.cleaned_data.get('companion')
        description = models.CarType.objects.get(description=car)
        vacancy = description.vacancy
        get_user = models.List.objects.filter(date=date, cns=cns)
        counter = 0
        if self.instance.pk:
            get_pk = models.List.objects.get(pk=self.instance.pk)
            counter -= get_pk.companion + 1
            get_user = None
        for n in models.List.objects.filter(date=date, car=car):
            counter += n.companion + 1
        total_vacancy = vacancy - counter
        total_user = companion + 1
        if total_vacancy < total_user:
            if total_vacancy > 1:
                raise forms.ValidationError('Veículo com {} vagas!'.format(vacancy - counter))
            else:
                raise forms.ValidationError('Veículo com {} vaga!'.format(vacancy - counter))
        if get_user:
            raise forms.ValidationError('Usuário já agendado no {}'.format(get_user[0].car))

    def clean_cns(self):
        cns = self.cleaned_data.get('cns')
        return cns

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.isupper():
            raise forms.ValidationError(self.message)
        return name

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address.isupper():
            raise forms.ValidationError(self.message)
        return address

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            if not views.Valid(telephone=telephone).valid_telephone():
                raise forms.ValidationError(self.message)
        return telephone

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            raise forms.ValidationError(self.message)
        return date

    class Meta:
        model = models.List
        fields = '__all__'


class CarTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['destiny'].queryset = models.City.objects.exclude(enable=False)


class UserRegisterAdmin(admin.ModelAdmin):
    form = UserRegisterForm
    list_display = ('name', 'cns', 'birth', 'sex', 'address', 'telephone')
    search_fields = ('name', 'cns', 'birth', 'sex', 'address', 'telephone')

    def save_model(self, request, obj, form, change):
        if not change:
            if models.UserRegister.objects.filter(cns=obj.cns):
                models.UserRegister.objects.filter(cns=obj.cns).update(enable=True)
            else:
                obj.save()

    def delete_model(self, request, obj):
        obj.enable = False
        obj.save()

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(enable=False)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cns']
        else:
            return []

    def get_actions(self, request):
        actions = admin.ModelAdmin.get_actions(self, request)
        return actions

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/core.user.register.js',
            'js/core.valid.cns.js'
        )


class ListAdmin(admin.ModelAdmin):
    form = ListForm
    fields = (
        'cns', 'name', 'reference', 'address', 'telephone', 'local', 'goal', 'companion', 'date', 'hour', 'car',
        'search', 'note'
    )
    list_display = ('name', 'reference', 'local', 'companion', 'date', 'hour', 'car', 'telephone', 'search')
    search_fields = ('cns', 'name', 'reference')
    date_hierarchy = 'date'
    change_list_template = 'admin.change_list.html'

    def get_actions(self, request):
        actions = admin.ModelAdmin.get_actions(self, request)
        return actions

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/moment.js',
            'js/core.marking.js',
            'js/core.valid.cns.js'
        )


class HolidayAdmin(admin.ModelAdmin):
    fields = ('name', 'date')
    list_display = ('name', 'date')

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/moment.js',
            'js/core.marking.js',
            'js/core.valid.cns.js'
        )


class CityAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)

    def save_model(self, request, obj, form, change):
        if not change:
            if models.City.objects.filter(name=obj.name):
                models.City.objects.filter(name=obj.name).update(enable=True)
            else:
                obj.save()

    def delete_model(self, request, obj):
        obj.enable = False
        obj.save()

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(enable=False)

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/moment.js',
            'js/core.marking.js',
            'js/core.valid.cns.js'
        )


class CarTypeAdmin(admin.ModelAdmin):
    form = CarTypeForm
    fields = ('type', 'destiny', 'vacancy')
    list_display = ('description', 'destiny', 'vacancy')
    ordering = ('destiny', 'type', 'description')

    def save_model(self, request, obj, form, change):
        counter = 1
        description = '{} {:02d} - {}'.format(obj.get_type_display(), counter, obj.destiny)
        if not change:
            while models.CarType.objects.filter(description=description, enable=True):
                counter += 1
                description = '{} {:02d} - {}'.format(obj.get_type_display(), counter, obj.destiny)
        obj.description = description
        if models.CarType.objects.filter(description=description):
            models.CarType.objects.filter(description=description).update(enable=True)
        else:
            obj.save()

    def delete_model(self, request, obj):
        obj.enable = False
        obj.save()

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(enable=False)

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/moment.js',
            'js/core.marking.js',
            'js/core.valid.cns.js'
        )


admin.site.register(models.UserRegister, UserRegisterAdmin)
admin.site.register(models.List, ListAdmin)
admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.CarType, CarTypeAdmin)
admin.site.disable_action('delete_selected')
admin.site.site_title = 'Administração das Viagens'
admin.site.site_header = 'Agenda de Viagens'
admin.site.index_title = 'Agenda'
