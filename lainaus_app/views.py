from django.shortcuts import render

# Näkymä kotisivulle
def home(request):
    # Renderöi kotisivu, jossa on kolme painiketta: Lainaus, Palautus ja Hallinto
    # Tässä ei ole vielä mitään logiikkaa painikkeiden toiminnalle, vain näkymä
    return render(request, 'home.html')
