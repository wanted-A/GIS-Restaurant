from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .location_data import get_location_data
from .serializers import SignupSerializer


class SignupView(APIView):
    """
    POST:회원가입
    """

    def get(self, request):
        return Response({"message": "username, email, password를 입력해주세요."})

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # location_data = get_location_data()
            # if location_data:
                user = serializer.save()
                return Response(
                    {
                        "pk": user.pk,
                        "username": user.username,
                        "email": user.email,
                        "message": "회원가입 성공!",
                        "is_recommend": user.is_recommend,
                        # "user_lat": user.user_lat,
                        # "user_lon": user.user_lon,
                    },
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     else:
        #         return Response(
        #             {"message": "위치 정보를 가져올 수 없습니다."},
        #             status=status.HTTP_503_SERVICE_UNAVAILABLE,
        #         )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
