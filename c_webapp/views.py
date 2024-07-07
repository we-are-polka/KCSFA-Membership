from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, ChangePasswordForm, UserInfoForm


# Create your views here.
@login_required
def home(request):
    return render(request, 'c_webapp/home.html')

@login_required
def profile_page(request):
    return render(request, 'c_webapp/profile.html')

@login_required
def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		if form.is_valid():
			# Save original form
			form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

@login_required
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')


@login_required
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        update_profile_form = UpdateUserForm(request.POST or None, instance=current_user)
        if update_profile_form.is_valid():
            update_profile_form.save()

            login(request, current_user)
            messages.success(request, "User has been Updated!!")
            
            return redirect('home')
        return render(request, "update_user.html", {'update_profile_form':update_profile_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page")
        return redirect('home')