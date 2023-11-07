from django.core.cache import cache
from celery import shared_task
from location.models import Location

# 인기 맛집 조회수 기준
VIEWS_THRESHOLD = 100


# 인기 장소 데이터 로드 테스크
@shared_task
def cache_popular_locations():
    popular_locations = Location.objects.filter(views__gte=VIEWS_THRESHOLD)

    from location.serializers import LocationSerializer

    serializer = LocationSerializer(popular_locations, many=True)

    # serializer 데이터 캐싱
    cache.set("popular_location_data", serializer.data, timeout=600)  # 600초 후 캐시 삭제
