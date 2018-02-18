import warnings
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,Http404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.context_processors import csrf
from .models import contact,Profile
from .form import RegisterForm,ContactForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import os
from django.views.static import serve
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url
from django.utils.deprecation import RemovedInDjango110Warning
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters


# Create your views here.
def index(request):
    return render_to_response('work/index.html',{})

@csrf_exempt
def message(request):
    if request.method == "POST":
        print('got a requesst')
        post = request.POST
        email = post.get('email')
        number = post.get('number')
        name = post.get('name')
        message = post.get('msg')
        contact.objects.create(name=name,email=email,number=number,message=message)
        messages.success(request,"Message recorded!, we'll contact you soon",fail_silently=True)
        response_data = {}

    else:
        raise Http404('not allowed')

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('work/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = RegisterForm()
    return render(request, 'work/registration.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'work/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return render(request, 'work/account_activation_invalid.html')

def contactpage(request):
    if request.method == 'POST':
        form1 = ContactForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('/agency/')
    else:
        form1=ContactForm()
        return render(request,'work/message.html',{'form1':form1})
def loginpage(request):
    c={}
    c.update(csrf(request))
    return render(request,'work/login.html',c)

def auth_view(request):
    username= request.POST.get('username','')
    password= request.POST.get('password','')
    remember=request.POST.get('remember')
    if not remember:
        request.session.set_expiry(0)
    user=auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        messages.success(request, 'Your password was updated successfully!')
        return HttpResponseRedirect('/agency/logged/')
    else:
        return  HttpResponseRedirect('/agency/invalid_log/')

def logged(request):
    return render(request,'work/index.html',{'full_name':request.user.username})

def invalid(request):
    return render(request,'work/invalid_log.html',{})

def logout(request):
    auth.logout(request)
    return render(request,'work/index.html',{})

def infobro(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, 'PDFs/infobrochure.pdf')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 1.10.",
                    RemovedInDjango110Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form2': form
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return render(request, template_name, context)

def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return render(request, template_name, context)

@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
    context = {
        'form3': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return render(request, template_name, context)

def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return render(request, template_name, context)

def mail_sending(request):
    send_mail('just checking', 'I am the best', 'as57807@gmail.com', ['abhishek.lock.97@gmail.com'],fail_silently=False,)
    return True


