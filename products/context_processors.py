# context_processors.py
from .forms import FiltersForm

def filters(request):
    """
    Provide the FiltersForm instance as a context variable.

    This function creates an instance of
    the FiltersForm using the request's GET parameters.
    It is intended to be used as a context
    processor to make the form available in templates.

    Parameters:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        dict: A dictionary containing the FiltersForm instance.
    """
    filters_form = FiltersForm(request.GET or None)
    return {'filters_form': filters_form}
