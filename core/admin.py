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


admin.site.register(models.UserRegister, UserRegisterAdmin)
admin.site.disable_action('delete_selected')
admin.site.site_title = 'Administração das Viagens'
admin.site.site_header = 'Agenda de Viagens'
admin.site.index_title = 'Agenda'
