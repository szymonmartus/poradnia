from atom.filters import CrispyFilterMixin
import django_filters
from .models import Letter


class StaffLetterFilter(CrispyFilterMixin, django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(StaffLetterFilter, self).__init__(*args, **kwargs)
        self.filters['status'].field.choices.insert(0, ('', u'---------'))

    class Meta:
        model = Letter
        fields = ['status', ]


class UserLetterFilter(CrispyFilterMixin, django_filters.FilterSet):
    class Meta:
        model = Letter
        fields = []
