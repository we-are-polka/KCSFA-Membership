from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.http import JsonResponse



# Create your views here.
def register_user(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, "You have registered successfully!")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
                    return JsonResponse({'success': True})
                else:
                    return redirect('home')
            else:
                messages.error(request, "Failed to log in after registration.")
        else:
            errors = form.errors.as_json()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
                return JsonResponse({'success': False, 'errors': errors})
            else:
                messages.error(request, "Registration failed. Please correct the errors.")

    return render(request, 'b_auth/register.html', {'form': form})

# def register_user(request):
#     form  = SignUpForm()
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             #login user
#             user = authenticate(username = username, password = password)
#             login(request, user)
#             messages.success(request, ("You have registered successfully...."))
#             return redirect('home')
#         else:
#             messages.success(request, ("Whoops! There was a problem, Please try again...."))
#             return redirect('home')
#     else:
#         return render(request, 'b_auth/register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(f'login details: user:{username} pass:{password}')

        if user is not None:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
                print('logged in successfully')
                login(request, user)
                return JsonResponse({'success': True})
            else:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if the request is AJAX
                print('login failed')

                return JsonResponse({'success': False})
            else:
                messages.error(request, "Invalid credentials, please try again.")
                return redirect('login')
    else:
        return render(request, 'b_auth/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out. Thanks for stopping by...."))
    return redirect('home')
