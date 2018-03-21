from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UserForm
from .forms import SearchForm
from .forms import PinForm

from Google.GoogleApi import GoogleApi
from Norton.PQS import PQS
from django.http import JsonResponse

from Google.GoogleApi import LOGIN_FAILURE
from Google.GoogleApi import LOGIN_SUCCESS
from Google.GoogleApi import LOGIN_NEED_PIN_VERIFICATION

google_api = GoogleApi()
pqs = PQS()


def index(request):
    return login_user(request)


def login_user(request):
    if request.method == 'POST':
        # A POST request: Handle Form Upload
        form = UserForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            account = form.cleaned_data['account']
            pwd = form.cleaned_data['pwd']
            success = google_api.login(account, pwd)
            if LOGIN_SUCCESS == success:
                return HttpResponseRedirect('main.html')
            elif LOGIN_NEED_PIN_VERIFICATION == success:
                return HttpResponseRedirect('pin.html')

    return render(request, 'aotas/login.html', {'form': UserForm()})


def verify_pin(request):
    if request.method == 'GET':
        return render(request, 'aotas/pin.html', {'form': PinForm()})
    else:
        # A POST request: Handle Form Upload
        form = PinForm(request.POST) # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            pin = form.cleaned_data['pin']
            success = google_api.verify_pin(pin)
            if LOGIN_SUCCESS == success:
                return HttpResponseRedirect('main.html')
            elif LOGIN_NEED_PIN_VERIFICATION == success:
                return render(request, 'aotas/pin.html', {'form': PinForm()})

        return HttpResponseRedirect('login.html')


def get_devices(request):
    return render(request, 'aotas/main.html', {'devices': google_api.get_device_list()})


def get_apps_results(request):
    if request.method == 'GET' and 'deviceId' in request.GET:
        deviceId = request.GET['deviceId']
        deviceName = request.GET['deviceName']
        if deviceId is None or deviceId == '':
            return render(request, 'aotas/main.html', {'devices': google_api.get_device_list()})
        return render(request, 'aotas/device_result.html', {'raw_results': pqs.batch_scan_app_info(google_api.get_apps_by_device_web_id(deviceId)), 'deviceName': deviceName})
    return render(request, 'aotas/main.html', {'devices': google_api.get_device_list()})


def searchgp(request):
    if request.method == 'GET':
        return HttpResponseRedirect('main.html')
    else:
        # A POST request: Handle Form Upload
        form = SearchForm(request.POST) # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            return render(request, 'aotas/search_result.html', {'search_results': pqs.batch_scan_app_info(google_api.search_apps(keyword)), 'devices': google_api.get_device_list(), 'keyword': keyword})

    return HttpResponseRedirect('main.html')


def install_app(request):
    is_installed = False

    if request.method == 'GET' and 'deviceId' in request.GET and 'package' in request.GET:
        deviceId = request.GET['deviceId']
        package = request.GET['package']

        if deviceId is None or deviceId == '' or package is None or package == '':
            is_installed = False
        if google_api.install_app(package, deviceId):
            is_installed = True

    data = {
        'is_installed': is_installed,
    }

    return JsonResponse(data)
