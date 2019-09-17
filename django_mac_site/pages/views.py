from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import InfoForm
from .jss_api_call import query_api
from .jss_api_call import convert_units
from .jss_api_call import truncate
from .jss_api_call import format_results
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
