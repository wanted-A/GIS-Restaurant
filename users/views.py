from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .location_data import get_location_data
from .serializers import SignupSerializer, LoginSerializer, MyPageSerializer


from .serializers import SignupSerializer, LoginSerializer, MyPageSerializer


class SignupView(APIView):
    """
    POST:회원가입
    """

    def get(self, request):
        return Response({"message": "username, email, password를 입력해주세요."})

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.save()

            # simple jwt 발급
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            res = Response(
                {
                    "user_pk": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "message": "회원가입 성공",
                    "token": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST: 로그인
    """

    def get(self, request):
        return Response(
            {"message": "username, password를 입력해주세요."}, status=status.HTTP_200_OK
        )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"message": "username, password를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            location_data = get_location_data()
            if location_data:
                user.user_lat = location_data["location"]["lat"]
                user.user_lon = location_data["location"]["lng"]
                user.save(update_fields=["user_lat", "user_lon"])  # 위도, 경도만 업데이트

            login(request, user)

            serializer = LoginSerializer(user)

            # simplejwt 토큰 발급
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            res = Response(
                {
                    "user_pk": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "message": "로그인 성공",
                    "user_lat": user.user_lat,
                    "user_lon": user.user_lon,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            request.session["refresh"] = refresh_token
            res.set_cookie("access", access_token, httponly=True)

            return res
        return Response(
            {"message": "username, password를 확인해주세요."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """
    로그아웃
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "로그아웃 페이지 입니다."})

    def post(self, request):
        # 쿠키에서 access 토큰 삭제
        response = Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")

        # 세션에서 refresh 토큰 가져오기
        refresh_token = request.session.get("refresh")

        # refresh 토큰이 있으면 블랙리스트에 추가
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                # 세션에서 refresh 토큰 삭제
                del request.session["refresh"]

            # 이미 블랙리스트에 있는 토큰일 경우 예외 발생
            except Exception as e:
                print(e)
        #         return Response(
        #             {"message": "로그아웃 처리 중 오류가 발생했습니다."},
        #             status=status.HTTP_400_BAD_REQUEST,
        #         )
        # else:
        #     return Response({"message": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return response


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = MyPageSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = MyPageSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_info = serializer.save()
            return Response(
                MyPageSerializer(updated_info).data, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
