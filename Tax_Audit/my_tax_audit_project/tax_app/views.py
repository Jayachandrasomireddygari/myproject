from django.shortcuts import render, redirect
from .models import TaxEntry, Document
from .utils import calculate_tax
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    tax_entries = TaxEntry.objects.filter(user=request.user)
    documents = Document.objects.filter(user=request.user)

    if request.method == 'POST' and 'calculate_tax' in request.POST:
        income = float(request.POST['income'])
        expenses = float(request.POST['expenses'])
        deductions = float(request.POST['deductions'])
        tax_due = calculate_tax(income, expenses, deductions)

        TaxEntry.objects.create(
            user=request.user,
            income=income,
            expenses=expenses,
            deductions=deductions,
            calculated_tax=tax_due
        )
        return redirect('dashboard')

    if request.method == 'POST' and 'upload_file' in request.POST:
        file = request.FILES['document']
        description = request.POST.get('description', '')
        Document.objects.create(user=request.user, file=file, description=description)
        return redirect('dashboard')

    return render(request, 'dashboard.html', {'tax_entries': tax_entries, 'documents': documents})