from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^\Z', views.login_user, name='login_user'),
	url(r'^login.html$', views.login_user, name='login_user'),
	url(r'^pin.html$', views.verify_pin, name='verify_pin'),
	url(r'^main.html$', views.get_devices, name='get_devices'),
	url(r'^device_result.html$', views.get_apps_results, name='get_apps_results'),
	url(r'^search_result.html$', views.searchgp, name='searchgp'),
	url(r'^install_app.html$', views.install_app, name='install_app'),
]