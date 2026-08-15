from .models import Catalog


def site_catalog(request):
    return {"site_catalog": Catalog.objects.first()}
