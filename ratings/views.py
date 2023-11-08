from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from ratings.models import Rating

from drf_yasg.utils import swagger_auto_schema

from ratings.serializers import RatingSerializer
from restaurants.models import Restaurant

from swagger import *


# api/v1/ratings/<int:restaurant_id>/review/
class ReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, restaurant_id):
        return Restaurant.objects.get(id=restaurant_id)

    @swagger_auto_schema(
        operation_id="평가 등록 기능 안내",
        operation_description="평가 생성 기능을 사용하기에 앞서 어떤 값들이 사용되는지 안내합니다.",
        manual_parameters=[PATH_RESTAURANT_ID_NOT_REQUIRED],
        responses={200: "```{\nmessage: content(선택), score(필수) 를 입력해주세요.```"},
    )
    def get(self, request, restaurant_id):
        return Response(
            {"message": "content(선택), score(필수) 를 입력해주세요."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_id="평가 생성",
        operation_description="맛집에 대한 평가를 등록합니다.",
        manual_parameters=[PATH_RESTAURANT_ID],
        responses={
            201: RatingSerializer,
            400: "```{\n시리얼라이저 에러",
            401: "```{\ndetail: 자격 인증데이터(authentication credentials)가 제공되지 않았습니다.",
        },
    )
    def post(self, request, restaurant_id):
        """
        평가 생성 API
        """
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            restaurant = self.get_object(restaurant_id)
            review_count = Rating.objects.filter(restaurant=restaurant).count()

            new_review = serializer.save(user=request.user, restaurant=restaurant)

            restaurant.rating = (
                (restaurant.rating * review_count) + new_review.score
            ) / (review_count + 1)
            restaurant.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
