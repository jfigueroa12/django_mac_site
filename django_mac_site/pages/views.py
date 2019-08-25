from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import InfoForm
from .jss_api_call import query_api
# Create your views here.

class GetInfoView(TemplateView):
    template_name = 'get_info.html'


def get_info(request):
    serial = ''
    results = {}

    if request.method == 'POST':
        form = InfoForm(request.POST)

        if form.is_valid():
            serial = form.cleaned_data['serial']
            results = query_api(serial)

        return render(request, 'results.html', { 'serial': serial, 'results': results })

    else:

        form = InfoForm()
        return render(request, 'get_info.html', { 'form': form })
