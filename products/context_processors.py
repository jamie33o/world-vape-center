# context_processors.py
from .forms import FiltersForm

def filters(request):
    filters_form = FiltersForm(request.GET or None)
    return {'filters_form': filters_form}