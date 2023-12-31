from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully Login ...")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in. Please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully registered! Welcome ....")
            return redirect('home')
    
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, id):
    customer = Record.objects.get(id=id)

    if request.user.is_authenticated:
        return render(request, 'record.html', {'customer': customer})
    
    else:
        messages.error(request, "You must be logged in to view this page ...")
        return redirect('home')
    

def delete(request, id):
    records = Record.objects.all()
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=id)
        delete_it.delete()

        record = Record.objects.all()
        messages.success(request, "Customer deleted successfully ... ")
        return redirect('home')
        
    else:
        messages.error(request, "You must be logged in to complete this action ...")
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Successfully added a record ...")
                return redirect('home')
        else:
            return render(request, 'add_record.html', {'form': form})
        
    else:
        messages.error(request, "You must be logged in to complete this action ... ")
        return redirect('home')
    

def edit_record(request, id):
    if request.user.is_authenticated:
        this_record = Record.objects.get(id=id)
        form = AddRecordForm(request.POST or None, instance=this_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated ... ")
            return redirect('home')
        return render(request, 'edit_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to complete this action ... ")
        return redirect('home')