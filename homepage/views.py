from django.views.generic import TemplateView

# Create your views here.
class HomepageView(TemplateView):
    template_name = "homepage/home.html"