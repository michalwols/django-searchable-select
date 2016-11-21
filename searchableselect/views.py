try:
    # Django <=1.9
    from django.db.models.loading import get_model
except ImportError:
    # Django 1.10+
    from django.apps import apps
    get_model = apps.get_model

from django.db.models.functions import Length

# Python 3.x
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s):
        return str(s)

from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def filter_models(request):
    model_name = request.GET.get('model')
    search_field = request.GET.get('search_field')
    value = request.GET.get('q')

    model = get_model(model_name)

    values = (
        model.objects
            .annotate(**{search_field + '_length': Length(search_field)})
            .filter(**{'{}__icontains'.format(search_field): value})
            .order_by(search_field + '_length')[:20]
    values = [
        dict(pk=v.pk, name=unicode(v))
        for v
        in values
    ]

    return JsonResponse(dict(result=values))
