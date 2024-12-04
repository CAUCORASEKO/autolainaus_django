from django.shortcuts import render
from django.http import HttpResponse
from .forms import LainausForm
from .models import Lainaus, Opiskelija, Auto  # Se mantiene 'Auto', 'Opiskelija' y 'Lainaus' correctamente
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

# Pääsivu (Página principal)
def home(request):
    """
    Pääsivu, johon käyttäjä ohjataan.
    """
    return render(request, 'home.html')

# Lainaus-sivu (Vista para el préstamo)
def lainaus_view(request):
    """
    Autojen lainaaminen ja viivakoodin luominen.
    Lomake, auton lista ja opiskelijan ID:n viivakoodi.
    """
    form = LainausForm()
    autot = Auto.objects.all()  # Haetaan kaikki autot

    if request.method == 'POST':
        form = LainausForm(request.POST)
        if form.is_valid():
            context = process_lainaus_form(form)
            context['form'] = form
            context['autot'] = autot
            return render(request, 'lainaus.html', context)

    # Palautetaan tyhjä lomake ja auton lista
    return render(request, 'lainaus.html', {'form': form, 'autot': autot})

# Prosessoi lainauslomake ja luo viivakoodi (Procesar el formulario y generar el código de barras)
def process_lainaus_form(form):
    """
    Prosessoi lainauslomakkeen tiedot, luo viivakoodi ja tallentaa lainauksen tietokantaan.
    """
    lainaus = form.save(commit=False)  # Tallentaa ilman sitouttamista
    opiskelija_id = lainaus.opiskelija.opiskelija_id  # Hakee opiskelijan ID:n
    barcode_image, opiskelija_id = generate_barcode_with_id(opiskelija_id)  # Luodaan viivakoodi
    lainaus.viivakoodi = barcode_image  # Liitetään viivakoodi lainaukseen
    lainaus.save()  # Tallentaa lainauksen tietokantaan
    return {'barcode': barcode_image, 'opiskelija_id': opiskelija_id}

# Luo viivakoodi opiskelijan ID:llä (Generar el código de barras con el ID del estudiante)
def generate_barcode_with_id(opiskelija_id):
    """
    Luo viivakoodin opiskelijan ID:llä ja lisää sen alle tekstin.
    Palauttaa kuvan base64-muodossa ja opiskelijan ID:n.
    """
    # Luo viivakoodi Code128-muodossa
    code128 = barcode.get_barcode_class('code128')
    barcode_image = code128(opiskelija_id, writer=ImageWriter())
    barcode_io = BytesIO()
    barcode_image.write(barcode_io)
    barcode_io.seek(0)

    # Käytetään PIL:ia lisäämään opiskelijan ID teksti viivakoodin alle
    image = Image.open(barcode_io)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = opiskelija_id  # Teksti, joka näytetään viivakoodin alla
    text_width, text_height = draw.textsize(text, font=font)
    position = ((image.width - text_width) // 2, image.height - text_height - 5)
    draw.text(position, text, font=font, fill="black")

    # Muutetaan kuva base64-muotoon
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str, opiskelija_id  # Palautetaan kuva base64-muodossa ja opiskelijan ID

# Autojen palautus-sivu (Vista para la devolución de coches)
def palautus_view(request):
    """
    Palautus-sivu, jossa käyttäjä voi palauttaa auton.
    """
    return HttpResponse("Tämä on palautus-sivu.")

# Hallintapaneeli (Página de administración)
def hallinto_view(request):
    """
    Hallintapaneeli, johon voidaan lisätä lisätoimintoja.
    """
    return HttpResponse("Tämä on hallintapaneeli.")
