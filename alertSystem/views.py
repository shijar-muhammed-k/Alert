from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ship_details
from datetime import date, datetime, timedelta


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
    users = User.objects.all().delete
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
        return render(request, 'Operations/home.html')
    else:
        return render(request, 'Operations/home.html')


def viewData(request):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    today = date.today()
    month = datetime.now().month
    data = ship_details.objects.all()
    return render(request, 'Operations/records.html', {'data': data, 'today': today, 'month': [months[month-1], months[month], months[month+1]]})


def editRecord(request, id):
    data = ship_details.objects.get(id=id)
    return render(request, 'Operations/editRecord.html', {'data': data})