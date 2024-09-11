from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Event, EventCategory, CPDLog
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.utils import timezone


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

@login_required
def all_events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')  # Upcoming events
    categories = EventCategory.objects.all()
    context = {
        'events': events,
        'categories': categories,
    }
    return render(request, 'c_webapp/events.html', context)


@login_required
def single_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = request.user.profile
    is_registered = CPDLog.objects.filter(member=profile, event=event).exists()
    attendee_count = event.cpdlog_set.count()

    # Retrieve messages if they exist
    success_message = None
    error_message = None
    for message in messages.get_messages(request):
        if message.level == messages.SUCCESS:
            success_message = message
        elif message.level == messages.ERROR:
            error_message = message

    # Pass the context, including attendee count, registration status, and messages
    return render(request, 'c_webapp/single_event.html', {
        'event': event,
        'is_registered': is_registered,
        'attendee_count': attendee_count,
        'success_message': success_message,
        'error_message': error_message,
    })


# Register for Event (RSVP)
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = get_object_or_404(Profile, user=request.user)

    # Check if the user is already registered for this event
    if CPDLog.objects.filter(member=profile, event=event).exists():
        messages.error(request, 'You are already registered for this event.')
        return redirect('single_event', event_id=event_id)

    # Register the user for the event
    CPDLog.objects.create(member=profile, event=event)

    # Add the success message
    messages.success(request, f'Successfully registered for <br> {event.name}.')

    return redirect('single_event', event_id=event_id)

@login_required
def unregister_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    profile = get_object_or_404(Profile, user=request.user)

    # Check if the user is registered for this event
    cpd_log = CPDLog.objects.filter(member=profile, event=event).first()
    if not cpd_log:
        messages.error(request, 'You are not registered for this event.')
        return redirect('single_event', event_id=event_id)

    # Deduct the points acquired from this event
    profile.total_cpd_points -= event.category.points_per_event
    profile.save()

    # Remove the RSVP
    cpd_log.delete()

    # Add the success message
    messages.success(request, f'You have successfully unregistered from <br> {event.name}.')

    return redirect('single_event', event_id=event_id)