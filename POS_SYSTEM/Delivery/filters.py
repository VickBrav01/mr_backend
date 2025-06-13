import django_filters
from .models import Delivery


class FilterClasses(django_filters.FilterSet):
    status = django_filters.CharFilter(
        field_name="delivery_status", lookup_expr="iexact"
    )
    created_at = django_filters.DateFromToRangeFilter()
    username = django_filters.CharFilter(
        field_name="customer_name", lookup_expr="icontains"
    )

    class Meta:
        model = Delivery
        fields = ["delivery_status", "created_at", "customer_name"]
