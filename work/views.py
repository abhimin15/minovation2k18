import warnings
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,Http404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.context_processors import csrf
from .models import contact,Profile
from .form import *
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

def thanku(request):
    return render_to_response('work/thanku.html',{})

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
def checkout(request):
	if request.method == 'POST':
		try:
			userDetails=AluminiDetails.objects.get(email=request.user)
			if userDetails.register==1:
				return render(request, 'work/errorMessage.html', {'error':"You are already registered for the meet"})
		except:
			return render(request, 'work/errorMessage.html', {'error':"Unrecognized Request"})
		order_form = OrderForm(request.POST)
		person_details = paymentForm(request.POST)
	   # try:
		number_of_person=request.POST['persons_count']
		delegate=request.POST['delegate']

		if delegate=="Indian Delegate":
			amount=((int(number_of_person)-1)*500)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			amount=((int(number_of_person)-1)*25)+100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']
		#except:
			#return render(request, 'failure.html', {'error':"Invalid Inputs"})

		try:
			person={"person1":request.POST['person1'],"person2":request.POST['person2'],"person3":request.POST['person3'],"person4":request.POST['person4'],"person5":request.POST['person5'],"person6":request.POST['person6']}
			count=0
			for key, value in person.iteritems():
				if not value.strip()=="":
					count+=1
			if not str(count)==number_of_person:
				return render(request, 'work/errorMessage.html', {'error':"Person count does not match",'personCount':number_of_person,'count':count,'person':person})

		except:
			return render(request, 'work/errorMessage.html', {'error':"Error occured while matching the person count",'personCount':number_of_person,'count':count,'person':person})

		count=ReferenceNumber.objects.get(id=1)

		value=str(count.number)
		count.number+=1
		count.save()
		txnid="AM"+"0"*(5-len(value))+value

		#order_form.txnid=txnid
		if order_form.is_valid():
			initial = order_form.cleaned_data

			if not initial['amount']==(amount):
				return render(request, 'work/errorMessage.html', {'error':"Amount does not match"})
			initial.update({'key': merchant_key,
							'surl': request.build_absolute_uri(reverse('order.success')),
							'furl': request.build_absolute_uri(reverse('order.failure')),
							'udf1':person['person1']+"|"+person['person2']+"|"+person['person3'],'udf2':person['person4']+"|"+person['person5']+"|"+person['person6'],'udf3':number_of_person,'udf4':delegate,
							})
			# Once you have all the information that you need to submit to payu
			# create a payu_form, validate it and render response using
			# template provided by PayU.
			initial['txnid']=txnid
			payu_form = PayUForm(initial)
			if payu_form.is_valid():
				payuForm=payu_form.cleaned_data
				payu_form_final=PayUForm(payuForm)
				#return render(request, 'payment/errorMessage.html', {'error':payuForm["hash"]+" "+payuForm["udf4"]+" "+payuForm["txnid"]})
				context = {'form': payu_form_final,
						   'action': "%s" % settings.PAYU_INFO['payment_url']}
				ts=time.time()

				loggerCheckout.info(txnid+"  "+initial['email']+"  "+datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
				return render(request, 'work/paymentForm.html', context)
			else:
				loggerPay.error('Something went wrong! Looks like initial data\
						used for payu_form is failing validation')
				return render(request, 'work/errorMessage.html', {'error':"Code:410 ."})
		else:
			return render(request, 'work/errorMessage.html', {'error':"Code: 409"})
	else:

		return render(request, 'work/errorMessage.html', {'error':"Request is not POST"})
#@csrf_protect
@csrf_exempt
def success(request):
	if request.method == 'POST':
		ts=time.time()
		timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		try:
			txnid=request.POST.get('txnid')
			mihpayid=request.POST.get('mihpayid')
			email=request.POST.get('email')
			amount=request.POST.get('amount')
			error_Message=request.POST.get('error_Message')
			status=request.POST.get('status')
			mode=request.POST.get('mode')
			group1=request.POST.get('udf1').split("|")
			group2=request.POST.get('udf2').split("|")
			personCount=request.POST.get('udf3')
			delegate=request.POST.get('udf4')

			#timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		except:
			loggerPay.error("Parameters are not in response")

		if delegate=="Indian Delegate":
			#amount=((int(number_of_person)-1)*3000)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			#amount=int(number_of_person)*100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']

		if not verify_hash(request.POST,salt):
			return redirect('order.failure')
		else:
			loggerPay.info(mihpayid+"\t"+txnid+'\t'+email+"\t"+amount+"\t"+cc+"\t"+timestamp+"\t"+error_Message+"\t"+status)
			#try:
			payment=PaymentDetails(email=email,txnid=txnid,mihpayid=mihpayid,timestamp=datetime.datetime.now(),amount=amount,mode=mode)
			members=AlumniMeetMembers(email=email,delegate=delegate,person_count=personCount,person1=group1[0],person2=group1[1],person3=group1[2],person4=group2[0],person5=group2[1],person6=group2[2])
			payment.save()
			members.save()
			user=AluminiDetails.objects.get(email=request.POST.get('email'))
			user.register=1
			user.save()
			return render(request, 'payment/success.html',{'request':request.POST})
			#except:
				#return render(request, 'errorMessage.html', {'error':"Database Error"})

	else:
                return render_to_response('portal/error.html')
@csrf_exempt
def failure(request):
	context_dict={}
	if request.method == 'POST':

		ts=time.time()
		try:
			txnid=request.POST.get('txnid')
			mihpayid=request.POST.get('mihpayid')
			email=request.POST.get('email')
			amount=request.POST.get('amount')
			error_Message=request.POST.get('error_Message')
			status=request.POST.get('status')
			timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			delegate=request.POST.get('udf4')
		except:
			loggerPay.error("Parameters are not in response")

		if delegate=="Indian Delegate":
			#amount=((int(number_of_person)-1)*3000)+5000
			cc="rupee"
			merchant_key=settings.PAYU_INFO['merchant_key_rupee']
			salt=settings.PAYU_INFO['salt_rupee']
		elif delegate=="Foreign Delegate":
			#amount=int(number_of_person)*100
			cc="dollar"
			merchant_key=settings.PAYU_INFO['merchant_key_usd']
			salt=settings.PAYU_INFO['salt_usd']

		context_dict["email"]=email
		context_dict['timestamp']=timestamp
		context_dict['txnid']=txnid
		if not verify_hash(request.POST,salt):
			loggerPay.warning("Response data for order (txnid: %s) has been "
						   "tampered. Confirm payment with PayU." %
						   request.POST.get('txnid'))

			context_dict['reason']="Response data for payment has been tampered"

			return render(request, 'payment/failure.html', context_dict)
		else:
			loggerPay.info(mihpayid+"\t"+txnid+'\t'+email+"\t"+amount+"\t"+cc+"\t"+timestamp+"\t"+error_Message+"\t"+status)
			context_dict['reason']=request.POST.get('error_Message')
			return render(request, 'payment/failure.html', context_dict)

	else:
		raise Http404("Unauthorized request")
