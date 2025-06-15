import django_filters
from Delivery.models import Delivery

class CustomerFilter(django_filters.FilterSet):
    delivery_status = django_filters.ChoiceFilter(
        field_name="delivery_status",
        choices=[
            ("pending", "Pending"),
            ("in_transit", "In Transit"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        lookup_expr="iexact"
    )
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Delivery
        fields = ["delivery_status", "created_at"]