from django.shortcuts import render,HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_done(request):
    return render(request,'work/done.html',{})

def payment_canceled(request):
    return render(request,'work/canceled.html',{})

def payment_process(request):
    order = request.session.get('order')
    host = request.get_host()
    paypal_dict = {
    'business': settings.PAYPAL_RECEIVER_EMAIL ,
    'amount': '%.2f' %order.get('amount'),
    'item_name': 'Item_Name_xyz',
    'invoice': 'Abhishek',
    'currency_code': 'USD',
    'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
    'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
    'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form4 = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'work/payment_process.html', {'form4': form4 })
# Create your views here.
