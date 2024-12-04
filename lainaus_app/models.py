from django.db import models
from django.core.exceptions import ValidationError
import datetime  # Haetaan nykyinen päivämäärä

# Opiskelija-malli
class Opiskelija(models.Model):
    etunimi = models.CharField(max_length=100)  # Etunimi
    sukunimi = models.CharField(max_length=100)  # Sukunimi
    opiskelija_id = models.CharField(max_length=50, unique=True)  # Opiskelija ID
    ajokortti_id = models.CharField(max_length=50, unique=True)  # Ajokortin ID
    puhelinnumero = models.CharField(max_length=15)  # Puhelinnumero

    def __str__(self):
        return f'{self.etunimi} {self.sukunimi} (ID: {self.opiskelija_id})'

# Auto-malli
class Auto(models.Model):
    merkki = models.CharField(max_length=100)  # Merkki
    malli = models.CharField(max_length=100)  # Malli
    vuosi = models.IntegerField()  # Vuosi
    väri = models.CharField(max_length=50)  # Väri
    rekisterikilpi = models.CharField(max_length=20, unique=True)  # Rekisterikilpi
    kilometrimäärä = models.IntegerField()  # Kilometrimäärä

    def __str__(self):
        return f'{self.merkki} {self.malli} ({self.vuosi}, {self.väri}, {self.rekisterikilpi})'



class Opiskelija(models.Model):
    etunimi = models.CharField(max_length=100, verbose_name='Etunimi')  # Nombre del estudiante
    sukunimi = models.CharField(max_length=100, verbose_name='Sukunimi')  # Apellido del estudiante

class Lainaus(models.Model):
    opiskelija = models.ForeignKey(Opiskelija, on_delete=models.CASCADE)  # Relación con Opiskelija (estudiante)
    etunimi = models.CharField(max_length=100, verbose_name='Etunimi')  # Nombre
    sukunimi = models.CharField(max_length=100, verbose_name='Sukunimi')  # Apellido
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, null=True, blank=True)  # Relación con Auto
    lainaus_päivä = models.DateField(default=datetime.date.today)  # Fecha de préstamo
    palautus_päivä = models.DateField(null=True, blank=True)  # Fecha de devolución
    viivakoodi = models.CharField(max_length=100, blank=True, null=True)  # Código de barras (opcional)


    def clean(self):
        """
        Varmistetaan, että palautuspäivämäärä ei ole ennen lainauspäivämäärää.
        """
        if self.palautus_päivä and self.lainaus_päivä and self.palautus_päivä <= self.lainaus_päivä:
            raise ValidationError("Palautus_päivä ei voi olla ennen lainaus_päivä.")

    def __str__(self):
        palautus = self.palautus_päivä or "Ei palautettu"
        return f'Lainaus: {self.opiskelija} on lainannut {self.auto} ({self.lainaus_päivä} - {palautus})'
