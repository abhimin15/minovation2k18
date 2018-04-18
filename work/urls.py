from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^donation/$', views.donation, name='donation'),
    url(r'^payment/',include('payment.urls')),

    url(r'^messages/$', views.message, name='messages'),
    url(r'^create/$', views.contactpage, name='contactpage'),

    url(r'^registration/$', views.registration, name='registration'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^login/$', views.loginpage, name='login'),
    url(r'^logged/$', views.logged, name='logged'),
    url(r'^invalid_log/$', views.invalid, name='invalid'),
    url(r'^auth_user/$', views.auth_view, name='auth_view'),
    url(r'^info/$', views.infobro, name='infobro'),

    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),

    url(r'^email/$', views.mail_sending, name='mail_sending'),

    url(r'^payment_process/$', views.payment_process, name='payment_process' ),
    url(r'^payment_done/$', views.payment_done, name='payment_done'),
    url(r'^payment_canceled/$', views.payment_canceled, name='payment_canceled'),
    url(r'^payment_take/$',views.payment_taken, name='payment_taken'),
    url(r'^decision/$',views.decision,name='decision'),
]
