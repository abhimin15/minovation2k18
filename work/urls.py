from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^thanku/$', views.thanku, name='thanku'),
    url(r'^messages/$', views.message, name='messages'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^create/$', views.contactpage, name='contactpage'),
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
    url(r'^success/$', views.success, name='order.success'),
    url(r'^checkout/$',views.checkout, name='order.checkout'),
    url(r'^failure/$', views.failure, name='order.failure'),

]
