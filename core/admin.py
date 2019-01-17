from django import forms
from django.contrib import admin

from core import models, views


class UserRegisterForm(forms.ModelForm):
    message = 'Habilite o javascript!'

    class Meta:
        model = models.UserRegister
        fields = '__all__'

    def clean_cns(self):
        cns = self.cleaned_data['cns']
        if not views.Valid(cns=cns).valid_cns() or models.UserRegister.objects.filter(cns=cns):
            raise forms.ValidationError(self.message)
        return cns

    def clean_nome(self):
        nome = self.cleaned_data['name']
        if not nome.isupper():
            raise forms.ValidationError(self.message)
        return nome

    def clean_birth(self):
        birth = self.cleaned_data['birth']
        if not views.Valid(birth=birth).valid_birth():
            raise forms.ValidationError(self.message)
        return birth

    def clean_address(self):
        address = self.cleaned_data['address']
        if not address.isupper():
            raise forms.ValidationError(self.message)
        return address

    def clean_telefone(self):
        telephone = self.cleaned_data['telephone']
        if telephone:
            if not views.Valid(telephone=telephone).valid_telephone():
                raise forms.ValidationError(self.message)
        return telephone


class ListForm(forms.ModelForm):
    message = 'Habilite o javascript!'

    class Meta:
        model = models.List
        fields = '__all__'

    def clean_cns(self):
        cns = self.cleaned_data['cns']
        return cns

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.isupper():
            raise forms.ValidationError(self.message)
        return name

    def clean_address(self):
        address = self.cleaned_data['address']
        if not address.isupper():
            raise forms.ValidationError(self.message)
        return address

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if telephone:
            if not views.Valid(telephone=telephone).valid_telephone():
                raise forms.ValidationError(self.message)
        return telephone

    def clean_date(self):
        date = self.cleaned_data['date']
        if date is None:
            raise forms.ValidationError(self.message)
        return date


class UserRegisterAdmin(admin.ModelAdmin):
    form = UserRegisterForm
    list_display = ('name', 'cns', 'birth', 'sex', 'address', 'telephone')
    search_fields = ('name', 'cns', 'birth', 'sex', 'address', 'telephone')

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/core.user.register.js',
            'js/core.valid.cns.js'
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cns']
        else:
            return []

    def get_actions(self, request):
        actions = admin.ModelAdmin.get_actions(self, request)
        return actions


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

    def save_model(self, request, obj, form, change):
        obj.save()
        split_name = obj.name.split(' ')
        if len(split_name) > 1:
            cname = '{} {} {}'.format('Acompanhante de', split_name[0], split_name[-1])
        else:
            cname = '{} {}'.format('Acompanhante de', split_name[0])
        if change:
            models.List.objects.filter(id_companion=obj.id).delete()
            while obj.companion > 0:
                models.List(name=cname, date=obj.date, car=obj.car, id_companion=obj.id).save()
                obj.companion -= 1
        if obj.companion > 0 and not change:
            while obj.companion > 0:
                models.List(name=cname, date=obj.date, car=obj.car, id_companion=obj.id).save()
                obj.companion -= 1

    def delete_model(self, request, obj):
        models.List.objects.filter(id_companion=obj.id).delete()
        obj.delete()

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.cns:
            return ['cns', 'name', 'reference', 'address', 'telephone']
        elif obj and not obj.cns:
            return [
                'cns', 'name', 'reference', 'address', 'telephone', 'local', 'goal', 'companion', 'date', 'hour',
                'search', 'note'
            ]
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        if obj is None or obj.cns:
            return True
        else:
            return False

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.maskedinput.min.js',
            'js/jquery.validate.min.js',
            'js/moment.js',
            'js/core.marking.js',
            'js/core.valid.cns.js'
        )

    def get_actions(self, request):
        actions = admin.ModelAdmin.get_actions(self, request)
        return actions


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
    fields = ('type', 'destiny', 'vacancy')
    list_display = ('description', 'destiny', 'vacancy')
    ordering = ('type', 'destiny', 'description')

    def save_model(self, request, obj, form, change):
        counter = 1
        description = '{} {:02d} - {}'.format(obj.get_type_display(), counter, obj.destiny)
        while models.CarType.objects.filter(description=description):
            counter += 1
            description = '{} {:02d} - {}'.format(obj.get_type_display(), counter, obj.destiny)
        obj.description = description
        obj.save()

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
