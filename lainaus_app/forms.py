from django import forms
from django.core.exceptions import ValidationError
from .models import Lainaus, Opiskelija, Auto
from django.forms.widgets import DateTimeInput
import re

# Validoidaan Opiskelija ID
def validate_opiskelija_id(value):
    """
    Validoidaan, että Opiskelija ID on muodossa:
    6 numeroa, viiva, 3 numeroa ja kirjain. Esim. 123456-123A.
    """
    pattern = r'^\d{6}-\d{3}[A-Za-z]$'
    if not re.match(pattern, value):
        raise ValidationError('Opiskelija ID:n tulee olla muodossa 123456-123A.')

# Validoidaan Puhelinnumero
def validate_phone_number(value):
    """
    Validoidaan, että puhelinnumero on muodossa:
    +358 ja 9 numeroa.
    """
    pattern = r'^\+358\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Puhelinnumeron tulee alkaa +358 ja sisältää 9 numeroa.')

# Lomake lainaukselle
class LainausForm(forms.ModelForm):
    """
    Lomake auton lainaamiselle.
    Sisältää opiskelijan tiedot, auton valinnan, lainauspäivämäärän ja palautuspäivämäärän.
    """

    # Opiskelijan tiedot
    etunimi = forms.CharField(
        max_length=100,
        label='Etunimi',
        required=True,  # Tämä kenttä täytetään käyttäjän toimesta
        help_text='Opiskelijan etunimi.'
    )
    
    sukunimi = forms.CharField(
        max_length=100,
        label='Sukunimi',
        required=True,  # Tämä kenttä täytetään käyttäjän toimesta
        help_text='Opiskelijan sukunimi.'
    )
    
    # Puhelinnumeron validointi ja syöttö
    puhelinnumero = forms.CharField(
        max_length=13,
        validators=[validate_phone_number],
        label='Puhelinnumero',
        help_text='Syötä puhelinnumero muodossa +358123456789.'
    )

    # Auton valinta
    auto = forms.ModelChoiceField(
        queryset=Auto.objects.all(),
        label='Auto',
        help_text='Valitse lainattava auto.'
    )

    # Lainaus- ja palautuspäivämäärä
    lainaus_päivä = forms.DateField(
        widget=DateTimeInput(attrs={'type': 'date'}),
        label='Lainauspäivämäärä',
        help_text='Aseta lainauspäivämäärä.'
    )

    palautus_päivä = forms.DateField(  # Tässä käytämme oikeaa nimeä
        widget=DateTimeInput(attrs={'type': 'date'}),
        label='Palautus_päivä',
        help_text='Aseta palautus_päivä.'
    )

    # Metodi täyttämään etunimi ja sukunimi kentät opiskelijan mukaan
    # Tämä ei ole enää tarpeellinen, koska käyttäjä täyttää tiedot itse.

    class Meta:
        model = Lainaus
        fields = ['etunimi', 'sukunimi', 'puhelinnumero', 'auto', 'lainaus_päivä', 'palautus_päivä']
