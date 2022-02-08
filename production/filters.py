import django_filters
from django_filters import DateFilter, CharFilter, ModelChoiceFilter, MultipleChoiceFilter, ModelMultipleChoiceFilter

from .models import *
from master.models import *

class JobFilter(django_filters.FilterSet):
	# start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	# note = CharFilter(field_name='note', lookup_expr='icontains')
    # job_no = ModelChoiceFilter(queryset=Job.objects.all())
    job_no = ModelMultipleChoiceFilter(queryset=Job.objects.all())
    partner = ModelMultipleChoiceFilter(queryset=Partner.objects.all())
    style = ModelMultipleChoiceFilter(queryset=Style.objects.all())
    color = ModelMultipleChoiceFilter(queryset=Color.objects.all())
    status = ModelMultipleChoiceFilter(queryset=Status.objects.all())

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['date','party_dc_no','unique_id', 'slug','created_on','modified_on']    