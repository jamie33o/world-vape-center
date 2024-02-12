# sitemaps.py
from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["home",
                "about_us",
                "contact_us",
                "payments_options",
                "delivery_info",
                "returns_policy",
                "terms",
                "faq"]

    def location(self, item):
        return reverse(item)
    