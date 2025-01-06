from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Home page
@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')  
    else:
        return redirect('login')  

# Login page
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect('landing')
        else:
            return render(request, 'registration/login.html', {"error": "Invalid credentials"})
    return render(request, 'registration/login.html')



# Logout page
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

# Sign-up page
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if password1 != password2:
            return render(request, 'registration/signup.html', {"error": "Passwords do not match"})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/signup.html', {"error": "Username already taken"})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'registration/signup.html', {"error": "Email already registered"})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')  # Redirect to login page after successful sign-up
    
    return render(request, 'registration/signup.html')

# Password reset pages
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                user = None
            
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                domain = get_current_site(request).domain
                reset_url = f'http://{domain}/password_reset/{uid}/{token}/'
                
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                print(f"Sending email to {email} with reset URL: {reset_url}")  # Debug statement
                send_mail(
                    "Password Reset Request",
                    message,
                    'maythada.dku@gmail.com',  # Replace with your actual email
                    [email],
                    fail_silently=False,
                )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, "registration/password_reset.html", {"form": form})

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse('The link is invalid or has expired', status=400)

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

def home(request):
    # Example data (replace with actual database queries)
    total_income = 5000
    total_expenses = 2000
    return render(request, 'home.html', {
        'total_income': total_income,
        'total_expenses': total_expenses
    })
    
'''def add_transaction(request):
    return HttpResponse("Add Transaction Page Coming Soon!")

def view_transactions(request):
    return render(request, 'transactions.html')'''
    
#landing page    
def landing_view(request):
    # Define the context data here (if needed)
    context = {
        'key': 'value',  # Add your key-value pairs here for the template
    }
    
    return render(request, 'registration/landing.html', context)

