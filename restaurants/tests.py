from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from restaurants.models import Restaurant

User = get_user_model()


class RestaurantAPITestCase(APITestCase):
    def setUp(self):
        # 사용자와 레스토랑 인스턴스 생성
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Make sure to provide all the required field names and values for the Restaurant model
        self.restaurant = Restaurant.objects.create(
            restaurant_name="Test Restaurant",
            road_address="123 Test St",
            license_date="2023-01-01",
            closed_date="2023-01-01",
            latitude=37.5665,
            longitude=126.9780,
            zip_code="04524",
            restaurant_code="REST123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_restaurant(self):
        # RestaurantAPIView 테스트
        url = reverse("restaurant-detail", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.restaurant.pk)  # Response 데이터 검증

    def test_get_restaurant_detail(self):
        # RestaurantDetailAPIView 테스트
        url = reverse("restaurant-detail", kwargs={"restaurant_id": self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 외부 API로 부터 예상되는 return 필드 목록
        expected_keys = {
            "id",
            "location_name",
            "location_code",
            "restaurant_name",
            "license_date",
            "business_status_name",
            "closed_date",
            "location_area",
            "water_supply_facility_name",
            "male_worker_count",
            "year",
            "multi_use_yn",
            "grade_division_name",
            "total_facility_scale",
            "female_worker_count",
            "business_site_around_name",
            "clean_industry_name",
            "clean_business_type",
            "total_worker_count",
            "road_address",
            "lot_num_address",
            "zip_code",
            "latitude",
            "longitude",
            "rating",
            "restaurant_code",
            "reviews",
        }
        self.assertEqual(set(response.data.keys()), expected_keys)  # 필드 검증

    def test_get_restaurant_not_found(self):
        # 존재하지 않는 맛집 조회 시 NotFound 테스트
        url = reverse(
            "restaurant-detail", kwargs={"restaurant_id": 99999}
        )  # 이슈 번호 #27 기준 존재하지 않는 restaurant_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        # 테스트 후 클린업 작업
        self.user.delete()
        self.restaurant.delete()
