from django import forms
from captcha.fields import CaptchaField
from django.core.validators import FileExtensionValidator
from gsras.models import News

class Captcha (forms.Form):
    captcha = CaptchaField (error_messages= {"invalid":u"Неверная каптча"})

class Organization (forms.Form):
    organization = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': u'Название организации',
        'class': 'form-control'
    }))
    boss_surname = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': u'Фамилия',
        'class': 'form-control'
    }))
    boss_firstname = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': u'Имя',
        'class': 'form-control'
    }))
    boss_secname = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': u'Отчество',
        'class': 'form-control'
    }))

class DataNeed (forms.Form):
    CHOICE = [("retro", u"Ретроспективно"), ("realtime", u"Реальное время")]
    choice_data_type = forms.ChoiceField(required=False, initial='retro', choices=CHOICE,  widget=forms.RadioSelect(attrs = {
        "class": "btn-check", "autocomplete": "off"
    }) )
    add_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'csv', 'pdf', 'doc', 'docx', 'xlsx', 'xls', 'odt', 'ods'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': ".txt, .csv, .pdf, .doc, .docx, .xlsx, .xls, .odt, .ods"})
    )
    req_comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': u'Комментарий к вложению',
        'class': 'form-control'
    }))

class ContactPersonal (forms.Form):

    contacts_surname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': u'Фамилия *',
        'class': 'form-control'
    }))
    contacts_firstname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': u'Имя *',
        'class': 'form-control'
    }))
    contacts_secname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': u'Отчество *',
        'class': 'form-control'
    }))
    contacts_phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': u'Телефон *',
        'class': 'form-control'
    }))
    contacts_email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': u'Email *',
        'class': 'form-control'
    }))
