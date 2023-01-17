from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ship_details
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.db import connection


# Create your views here.
def check_user(request):
    if User.objects.count() == 0:
        return render(request, 'AddUser.html')
    else:
        return redirect('login')


def create_user(request):
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('register')
    else:
        return render(request, 'AddUser.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('register')
    else:
        if request.method == "POST":
            userName = request.POST['userName']
            password = request.POST['password']
            user = authenticate(username=userName, password=password)
            if user is not None:
                login(request, user)
                return redirect('register')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def register(request):
    count = get_alert_items()
    if request.method == 'POST':
        db = ship_details()
        db.name = request.POST['name']
        db.address = request.POST['address']
        db.email = request.POST['email']
        db.phone = request.POST['phone']
        db.docking_date = request.POST['dockingDate']
        db.undocking_date = request.POST['undockingDate']
        db.reminder_type = request.POST['reminderType']
        reminder_date = request.POST['reminderDate']
        reminder_days = request.POST['reminderDays']
        if reminder_date != '':
            db.reminder_date = reminder_date
            db.reminder_days = (datetime.strptime(db.undocking_date, "%Y-%m-%d") - datetime.strptime(reminder_date, "%Y-%m-%d")).days
        if reminder_days != '':
            db.reminder_days = int(reminder_days)
            db.reminder_date = (datetime.strptime(db.undocking_date, "%Y-%m-%d") - timedelta(days=int(reminder_days))).date()
        db.save() 
        return render(request, 'Operations/home.html', {'count': count})
    else:
        return render(request, 'Operations/home.html', {'count': count})


def viewData(request):
    count = get_alert_items()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    today = date.today()
    month = datetime.now().month
    data = ship_details.objects.all()
    return render(request, 'Operations/records.html', {'data': data, 'today': today, 'month': [months[month-1], months[month], months[month+1]], 'count': count})


def editRecord(request, id):
    count = get_alert_items()
    data = ship_details.objects.get(id=id)
    if request.method == 'POST':
        data.name = request.POST['name']
        data.address = request.POST['address']
        data.email = request.POST['email']
        data.phone = request.POST['phone']
        data.docking_date = request.POST['dockingDate']
        data.undocking_date = request.POST['undockingDate']
        data.reminder_type = request.POST['reminderType']
        data.status = ''
        reminder_date = request.POST['reminderDate']
        reminder_days = request.POST['reminderDays']
        if reminder_date != '':
            data.reminder_date = reminder_date
            data.reminder_days = (datetime.strptime(data.undocking_date, "%Y-%m-%d") - datetime.strptime(reminder_date, "%Y-%m-%d")).days
        if reminder_days != '':
            data.reminder_days = int(reminder_days)
            data.reminder_date = (datetime.strptime(data.undocking_date, "%Y-%m-%d") - timedelta(days=int(reminder_days))).date()
        data.save() 
        return redirect('view')
    else:
        return render(request, 'Operations/editRecord.html', {'data': data, 'count': count})


def success(request, id):
    data = ship_details.objects.get(id=id)
    data.status = 'success'
    data.save()
    return HttpResponse('<script type="text/javascript">alert("Record marked as success!", window.location.href = "alert");</script>')

def alert(request):    
    count = get_alert_items()
    data = ship_details.objects.filter(reminder_date__lte=datetime.now().date())
    alert_items = []
    for i in data:
        if i.status != 'success':
            alert_items.append(i)
    return render(request, 'Operations/alertRecord.html', {'data': alert_items, 'count': count})


def get_alert_items():
    data = ship_details.objects.filter(reminder_date__lte=datetime.now().date())
    count = 0
    for i in data:
        if i.status != 'success':
            count += 1
    return count