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
        fields = ['job_no','partner','color','style','status']
        # exclude = ['date','party_dc_no','unique_id', 'slug','created_on','modified_on']    


class DeliveryFilter(django_filters.FilterSet):

    job_no = ModelMultipleChoiceFilter(queryset=Job.objects.all())
    # number = django_filters.CharFilter(lookup_expr='icontains')
    # date = DateFilter(field_name="date")
    job_no__color = ModelMultipleChoiceFilter(queryset=Color.objects.all())
    job_no__style = ModelMultipleChoiceFilter(queryset=Style.objects.all())
    job_no__status = ModelMultipleChoiceFilter(queryset=Status.objects.all())
    # end_date = DateFilter(field_name="date", lookup_expr='lte')
    size = ModelMultipleChoiceFilter(queryset=Size.objects.all())
    # piece_type = ModelMultipleChoiceFilter(queryset=PieceType.objects.all())



    class Meta:
        model = Delivery
        fields = ['job_no','job_no__color','job_no__style','job_no__status','size']
        # exclude = ['date','party_dc_no','unique_id', 'slug','created_on','modified_on'] 