from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, CampaignForm, HouseVisitForm, UserProfileForm
from .models import Campaign, HouseVisit, UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def index(request):
    return render(request, 'index.html')

def user_page(request):
    return render(request, 'user_page.html')

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

def campaign_statistics(request):
    campaigns = Campaign.objects.all()
    campaign_statistics = []

    for campaign in campaigns:
        visits_count = HouseVisit.objects.filter(campaign=campaign).count()
        campaign_statistics.append({
            'campaign': campaign,
            'visits_count': visits_count
        })

    return render(request, 'campaign_statistics.html', {'campaign_statistics': campaign_statistics})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_dashboard(request):
    user_campaigns = Campaign.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    user_visits = HouseVisit.objects.filter(user=request.user)

    if request.method == 'POST':
        campaign_form = CampaignForm(request.POST)
        house_visit_form = HouseVisitForm(request.POST)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if campaign_form.is_valid():
            campaign = campaign_form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return redirect('user_dashboard')
        elif house_visit_form.is_valid():
            house_visit = house_visit_form.save(commit=False)
            house_visit.user = request.user
            house_visit.save()
            return redirect('user_dashboard')
        elif profile_form.is_valid():
            profile_form.save()
            return redirect('user_dashboard')
    else:
        campaign_form = CampaignForm()
        house_visit_form = HouseVisitForm()
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_campaigns': user_campaigns,
        'user_profile': user_profile,
        'campaign_form': campaign_form,
        'house_visit_form': house_visit_form,
        'profile_form': profile_form,
        'user_visits': user_visits,
    }

    return render(request, 'user_dashboard.html', context)


def user_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    user = request.user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        password_form = PasswordChangeForm(user, request.POST)

        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, user)
            return redirect('user_dashboard')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        password_form = PasswordChangeForm(user)

    return render(request, 'registration/user_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })