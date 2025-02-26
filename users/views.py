from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.dateparse import parse_date
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.conf import settings
from .forms import MemberLoginForm, MemberRegistrationForm
from .utils import generate_token
from .models import Member
from posts.models import Post
import threading

# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()


def reset_user_password(member, request):
    current_site = get_current_site(request)
    email_subject = "Reset Password"
    email_body = render_to_string('registration/reset_pw.html', {'member': member,
                                                                 'domain': current_site.domain,
                                                                 'uid': urlsafe_base64_encode(force_bytes(member.pk)),
                                                                 'token': generate_token.make_token(member)})
    email = EmailMessage(subject=email_subject, 
                         body=email_body, 
                         from_email=settings.EMAIL_FROM_USER, 
                         to=[member.email])
    EmailThread(email).start()


def send_activation_email(member, request):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string('registration/activate.html', {'member': member,
                                                                 'domain': current_site.domain,
                                                                 'uid': urlsafe_base64_encode(force_bytes(member.pk)),
                                                                 'token': generate_token.make_token(member)})
    email = EmailMessage(subject=email_subject, 
                         body=email_body, 
                         from_email=settings.EMAIL_FROM_USER, 
                         to=[member.email])
    EmailThread(email).start()


def index(request):
    posts = Post.objects.all()
    members = Member.objects.all()
    return render(request, 'home.html', {'posts': posts,
                                         'members': members,})


def login_user(request):
    if request.method == 'POST':
        form = MemberLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            member = authenticate(request, username=username, password=password)
            if member is not None:
                login(request, member)
                if not member.is_email_verified:
                    messages.add_message(request, messages.ERROR, "Your email isn't verified. Please check your email to verify your account.")
                    logout(request)
                    return redirect('login')
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password. Try again.")
    else:
        form = MemberLoginForm()
    return render(request, "registration/login.html", {"form": form})


def register_user(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.set_password(form.cleaned_data['password'])
            member.save()
            send_activation_email(member, request)
            messages.add_message(request, messages.SUCCESS, "We've sent you an email to verify your account.")
            return redirect('login')
    else:
        form = MemberRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        member = Member.objects.get(pk=uid)
    except Exception as e:    
        member = None
    if member and generate_token.check_token(member, token):
        member.is_email_verified = True
        member.save()
        messages.add_message(request, messages.SUCCESS, "Email has been verified, you can now log in!")
        return redirect('login')
    return render(request, "registration/activation_failed.html")


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def profile_user(request, username):
    if request.method == "POST":
        upload = request.FILES.get('upload', None)
        bio = request.POST.get('bio', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        profile = request.user.profile
        profile.bio = bio

        if upload:
            profile.profile_picture = upload
        try:
            if date_of_birth:
                parsed_date = parse_date(date_of_birth)
                if not parsed_date:
                    raise ValidationError('Invalid date format. Please use YYYY-MM-DD.')
                profile.date_of_birth = parsed_date

            profile.save()
            messages.success(request, 'Profile updated!')

        except ValidationError:
            messages.error(request, 'Error updating profile. Please try again.')
            return render(request, 'profile/visit_profile.html', {'bio':bio, 'date_of_birth':date_of_birth, 'upload':upload})

        return redirect('profile', username=request.user.username)
    return render(request, "profile/visit_profile.html")


def new_activation_email(request):
    # TODO: Implement functionality for user to request a new activation email
    # registration/activation_failed.html
    # messages.add_message(request, messages.SUCCESS, "We've sent you a new activation link. Please check your email.")
    return redirect('index')