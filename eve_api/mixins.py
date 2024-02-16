from django.utils import timezone
from datetime import timedelta
from django.db.models import Subquery, OuterRef, Sum, QuerySet

from .models import System, DangerRating
from .base_constants import MAX_HOURS_LIMIT, QUERY_RESULT_CUT_SIZE
from .utils import get_filter_kwargs


class SystemHandlerMixin:
    def _get_systems(self, security_status: str) -> QuerySet[System]:
        filter_kwargs = get_filter_kwargs(security_status)
        days_range = MAX_HOURS_LIMIT // 24
        time_now = timezone.localtime(timezone.now())
        time_starting_point = time_now - timedelta(days=days_range)

        systems = System.objects.filter(**filter_kwargs).annotate(
            danger_rating=Subquery(
                DangerRating.objects.filter(
                    system=OuterRef('pk'),
                    timestamp__range=(time_starting_point, timezone.now())
                )
                .values('system')
                .annotate(rate_sum=Sum('value'))
                .values('rate_sum')[:1]
            )
        ).order_by('danger_rating')[:QUERY_RESULT_CUT_SIZE]

        return systems