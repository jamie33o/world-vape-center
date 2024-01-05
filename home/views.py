from django.shortcuts import render
from django.views import View
from .models import HomePage


class IndexView(View):
    """
    View class for displaying a list of channels.
    """

    template_name = 'home/index.html'

    def get(self, request):
        """
        Handle GET requests to display the list of channels.

        Returns:
            HttpResponse: Rendered template with channel information.
        """
        
        homepage_instance = HomePage.objects.first()

        context = {
            'homepage_instance': homepage_instance,
        }
        return render(request, self.template_name, context)