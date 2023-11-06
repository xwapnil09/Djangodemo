from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from homeapp.models import User_data

# Create your views here.

def login_signup(request):      # Function to render Signin/Signup page
    stored_messages = messages.get_messages(request)
    success_message = ''
    error_message = ''
    for msg in stored_messages:
        if 'successfully' in str(msg).lower():
            success_message = msg
        else:
            error_message = msg  
    return render(request, 'login-signup.html', {"success_messages":success_message, "error_messages": error_message})


def handleSignup(request):      # This function will handle the Signup to ToDo app
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if len(username)>30:
            messages.error(request, "Username must be under 30 characters !")
            return redirect('/')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist. Please choose a different Username !")
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exist. Please choose a different Email-id !")
            return redirect('/')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain alphabets and numbers !")
            return redirect('/')
        
        if pass1!=pass2:
            messages.error(request, "Passwords do not match !")
            return redirect('/')

        # Create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your account has been successfully created !")
        return  redirect('/')
    else:
        return HttpResponse('404 - Not Found')
    
def handleLogin(request):      # This function will handle the Login to ToDo app
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user:
            login(request ,user)
            messages.success(request, "Successfully Logged In !")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again !")
            return redirect('/')
    return HttpResponse('404 - Not Found')

def handleLogout(request):      # This function will handle the Logout
    logout(request)
    messages.success(request, "Successfully Logged Out !")
    return redirect('/')


def handleDelete(request):      # This function will handle the Delete account will all its data
    if request.method =='POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1!=pass2:
            messages.error(request, "Passwords do not match !")
            return redirect('/')
        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            # User with the provided username and email doesn't exist
            messages.error(request, "User with the provided username and email doesn't exist !")
            return redirect('/')

        # Check if the provided password matches the user's password
        if user.check_password(pass2):
            # Delete the User account
            user.delete()
            obj = User_data.objects.filter(username__exact=username)
            if obj.exists():
                obj.delete()
            messages.success(request, "Successfully Deleted account !")
            return redirect('/')
        else:
            # Incorrect password
            messages.error(request, "Incorrect password, Please try again !")
            return redirect('/')
    else:
        return HttpResponse('404 - Not Found')
    

def home(request):      # This will render the main home page of ToDo App.
    stored_messages = messages.get_messages(request)
    success_message = ''
    for msg in stored_messages:
        success_message = msg
    if request.user.is_authenticated:
        username = request.user
        username1 = str(username).capitalize()
        context = {'success':False, 'failed':False, 'updated_success':False, 'deleted_success':False, 'success_messages': success_message}
        print("goku12", request.POST)
        if request.method == "POST":
            if 'deleteId' in list(request.POST.keys()) or 'updateId' in list(request.POST.keys()):
                deleteId = request.POST.get('deleteId')
                updateId = request.POST.get('updateId')
                if deleteId:
                    User_data.objects.filter(pk=deleteId).delete()
                    context={'deleted_success':True}
                if updateId:
                    newcourse = request.POST.get('newcourse')
                    newamount = request.POST.get('newamount')
                    newphone = request.POST.get('newphone')
                    context={'updated_success':True}
                    User_data.objects.filter(pk=updateId).update(course=newcourse, amount=newamount, phone=newphone)
            else:
            # Handling the form
                course = request.POST.get('course')
                amount = request.POST.get('amount')
                phone = request.POST.get('phone')
                email = username.email
                user = str(username)
                if not course and not amount and not phone:
                    context = {'failed':True}
                else:
                    ins = User_data(course=course, amount=amount, username=user, phone=phone, email=email)
                    ins.save()
                    context = {'success':True}
        alldata = User_data.objects.filter(username__exact=str(request.user))
        context['info']=alldata
        context['username']=username1
        return render(request, 'home.html', context)
    else:
        return HttpResponse('404 - Not Found')