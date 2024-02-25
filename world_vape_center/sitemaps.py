from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    """
    Sitemap for static views.

    This sitemap includes static views such as home, about_us, contact_us, etc.
    """
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        """
        Get a list of static view names.

        Returns:
            list: List of static view names.
        """
        return ["home",
                "about_us",
                "contact_us",
                "payments_options",
                "delivery_info",
                "returns_policy",
                "terms",
                "faq"]

    def location(self, item):
        """
        Get the URL for a specific static view.

        Args:
            item (str): Name of the static view.

        Returns:
            str: URL for the specified static view.
        """
        return reverse(item)

    