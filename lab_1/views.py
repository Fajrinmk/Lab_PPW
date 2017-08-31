from django.shortcuts import render
from datetime import datetime

# Enter your name here
mhs_name = 'Fajrin Maulana K' # TODO Implement this

# Create your views here.
def index(request):
    response = {'name': mhs_name, "age": calculate_age(1998)}
    return render(request, 'index.html', response)

# TODO Implement this to complete last checklist
def calculate_age(birth_year):
    today = datetime.now().year
    return today - birth_year
