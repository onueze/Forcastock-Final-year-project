from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
import secrets
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
#from rest_framework import viewsets, permission
#from rest_framework.views import APIViewfrom 
#from rest_framework.response import Response

# Create your views here.

@require_POST
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('username')

        # Check if the email exists in the User model
        if User.objects.filter(username=email).exists():
            # Get the user object
            user = User.objects.get(email=email)

            formulateEmail(request, email)
            request.session['login_process'] = True

            return redirect('verify_code_register')
        else:
            print('false')
            # Flash error message
            messages.error(request, 'Invalid email. Please register first.')

    return render(request, 'base/login_register.html')

def registerPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        formulateEmail(request, email)
        request.session['login_process'] = False

        return redirect('verify_code_register')

    return render(request, 'base/register.html')



def verify_code_register(request):
    if 'verification_code' in request.session:
        if request.method == "POST":
            entered_code = int(request.POST.get('verification_code'))
            stored_code = request.session['verification_code']

            # Verify the entered code against the stored code 
            if entered_code == stored_code:
                email = request.session['email']
                print('email ', email)

                if 'login_process' in request.session and request.session['login_process']:
                    # User is trying to log in
                    user = authenticate(request, username=email, password="")
                    print(user, " USER")
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Login successful!')
                        return redirect('register')  # Redirect to home page after successful login
                    else:
                        messages.error(request, 'Invalid username or password.')
                        return redirect('login')  # Redirect back to login page for invalid credentials
                else:
                    # User is trying to register
                    new_user = User.objects.create_user(username=email, email=email, password="")
                    new_user.save()
                    messages.success(request, 'Registration successful!')
                    return redirect('login')  # Redirect to login page after successful registration

            else:
                messages.error(request, 'Incorrect verification code. Please try again.')

        return render(request, 'base/email_verification.html')
    


def generate_verification_code():
    # Generate a cryptographically secure random 6-digit number
    return secrets.randbelow(10**6)

# the verification email that is sent to the user
def formulateEmail(request, recipient):
    # Generate a verification code (you can use your own logic)
        verification_code = generate_verification_code()

        # Save the verification code in a session variable
        request.session['verification_code'] = verification_code
        request.session['email'] = recipient

        # Send email with verification code
        subject = 'Verification Code'
        message = f'Your verification code is: {verification_code}'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [recipient]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#def home(request):
    #return render(request, 'backend/templates/home.html')
