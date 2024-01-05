from django.shortcuts import render
from django.views import View


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
        return render(request, self.template_name)