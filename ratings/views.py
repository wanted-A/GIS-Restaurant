from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from ratings.models import Rating

from ratings.serializers import RatingSerializer
from restaurants.models import Restaurant


# api/v1/ratings/<int:restaurant_id>/review/
class ReviewAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, restaurant_id):
        return Restaurant.objects.get(id=restaurant_id)
    
    def get(self, request, restaurant_id):
        return Response(
            {"message" : "content(선택), score(필수) 를 입력해주세요."},
            status=status.HTTP_200_OK,
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

            restaurant.rating = ((restaurant.rating * review_count) + new_review.score) / (review_count + 1)
            restaurant.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)