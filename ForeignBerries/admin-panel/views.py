from django.shortcuts import render, redirect
from django.db.models.functions import Concat, Lower
from django.db.models import Sum, Q, Count, F, CharField, Value
from django.forms import inlineformset_factory
from .models import *
from .forms import *

def index(request):
    return render(request, 'app/index.html')

def busses(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           buses = Bus.objects.annotate(pc = Concat(('company'), Value(' '),('model'), Value(' '),F('yearOfIssue'), Value(' '),F('number'), Value(' '),F('VinNumber'), Value(' '),F('fuelConsumption'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            buses = Bus.objects.all()
    else: 
        buses = Bus.objects.all()
    
    context = {'buses' : buses}
    return render(request, 'admin-panel/busses.html', context)

def add_bus(request):
    form  = BusForm()

    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('busses')

    context = {'form' : form}
    return render(request, 'admin-panel/add-bus.html', context)

def update_bus(request, bus_id):
    bus = Bus.objects.get(id = bus_id)
    form = BusForm(instance=bus)

    if request.method == 'POST':
        form = BusForm(request.POST, instance = bus)
        if form.is_valid():
            form.save()
            return redirect('/busses')

    context = {'form' : form}
    return render(request, 'admin-panel/add-bus.html', context)


def delete_bus(request, bus_id):
    bus = Bus.objects.get(id = bus_id)
    if request.method == "POST":
        bus.delete()
        return redirect('/busses')
    context = {'bus' : bus}
    return render(request, 'admin-panel/delete-bus.html', context) 

def add_journey(request):
    form = JourneyForm()

    if request.method == 'POST':
        form = JourneyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'admin-panel/add-journey.html', context)


def update_journey(request, Journey_id):  
    journey = Journey.objects.get(id = Journey_id)
    form = JourneyForm(instance=journey)

    if request.method == 'POST':
        form = JourneyForm(request.POST, instance = journey)
        if form.is_valid():
            form.save()
            return redirect('journey/')

    context = {'form' : form}
    return render(request, 'admin-panel/add-journey.html', context)


def delete_journey(request, Journey_id):
    journey = Journey.objects.get(id = Journey_id)

    if request.method == 'POST':
        journey.delete()
        return redirect('journeys/')
    context = {'journey' : journey}
    return render(request, 'admin-panel/delete-journey.html', context)


def journeys(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           journey = Journey.objects.annotate(pc = Concat(('id'),Value(' '),F('number'),Value(' '),F('bus__number'),Value(' '),('ArrivalTime'),Value(' '),F('DepartureTime'),Value(' '),F('FullDistance'), Value(' '),F('fromWhere'),Value(' '),F('whereTo'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            journey = Journey.objects.all()
    else: 
        journey = Journey.objects.all()

    return render(request, 'admin-panel/journeys.html', {'journey' : journey})


def journey_stations (request, Journey_id):
    StationFormSet = inlineformset_factory(Journey, Station, fields=('stationName', 'distanceFromStart', 'stationArrivalTime', 'stationDepartureTime'), extra=15)
    journey = Journey.objects.get(id = Journey_id)
    formset = StationFormSet(instance = journey)
    #form = StationForm(initial={'journey' : journey})
    if request.method == 'POST':
        #form = StationForm(request.POST)
        formset = StationFormSet(request.POST, instance = journey)
        if formset.is_valid():
            formset.save()
            return redirect('/journey/')
    context = {'formset' : formset}
    return render(request, 'admin-panel/journey-stations.html', context)


def tickets(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           tickets = Ticket.objects.annotate(pc = Concat(('buyerName'), Value(' '),('buyerSurname'), Value(' '),F('price'), Value(' '),F('date'), Value(' '),F('journey__number'), Value(' '),F('type'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            tickets = Ticket.objects.all()
    else: 
        tickets = Ticket.objects.all()
    
    context = {'tickets' : tickets}
    return render(request, 'admin-panel/tickets.html', context)


def statistics(request):
    dat = request.POST.get('valu', '')
    datan = request.POST.get('validol', '')
    jrns = Journey.objects.all()
    js = 'не обрано'
    if request.method == 'POST':
        jrnsbus = request.POST.get('jrns', '')
        js = jrnsbus
        if jrnsbus == 'не обрано':
            total_sold = 0
        elif dat and datan and jrnsbus != 'None':
            total_sold = (Ticket.objects.filter(journey = Journey.objects.get(number=jrnsbus)).filter(Q(date__gte = dat) & Q(date__lte = datan)).aggregate(total_sold=Sum('price')))
        elif dat and datan and jrnsbus == 'None':
            total_sold = (Ticket.objects.filter(Q(date__gte = dat) & Q(date__lte = datan)).aggregate(total_sold=Sum('price')))
        else:
            total_sold = 6
    else :
        total_sold = 3

    context = {'total_sold' : total_sold,  'jrns' : jrns, 'dat' : dat, 'datan' : datan, 'js' : js}
    return render(request, 'admin-panel/statistics.html', context)


def search(request):
    return render(request, 'app/search.html')

def buy(request):
    return render(request, 'app/buy.html')

def success(request):
    return render(request, 'app/success.html')

