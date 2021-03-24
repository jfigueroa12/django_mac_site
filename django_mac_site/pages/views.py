from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import InfoForm
from .forms import DEPForm
from .jss_api_call import query_api
from .jss_api_call import convert_units
from .jss_api_call import truncate
from .jss_api_call import format_results
from .dep_req import dep_request
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class GetInfoView(TemplateView):
    template_name = 'get_info.html'

@csrf_exempt
def get_info(request):
    serial = ''
    results = {}

    if request.method == 'POST':
        form = InfoForm(request.POST)

        if form.is_valid():
            serial = form.cleaned_data['serial']
            (results, storage_results) = query_api(serial)

            if 'Not Found' in results:
                return render(request, 'results.html', { 'serial': serial, 'results': results })
            else:
                convert_units(results, storage_results)
                final_results = format_results(results, storage_results)
                return render(request, 'results.html', { 'serial': serial, 'results': final_results })

    else:
        form = InfoForm()
        return render(request, 'get_info.html', { 'form': form })


@csrf_exempt
def dep_check(request):

    if request.method == 'POST':
        form = DEPForm(request.POST)

        if form.is_valid():
            serial = form.cleaned_data['serial']
            results = dep_request(serial)

            if 'Not Found' in results:
                return render(request, 'dep_results.html', { 'serial': serial, 'results': results })
            else:
                return render(request, 'dep_results.html', { 'serial': serial, 'results': results })

    else:
        form = DEPForm()
        return render(request, 'dep.html', { 'form': form })
