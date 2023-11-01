from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError


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
            login(request, user)
            serializer = LoginSerializer(user)

            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            res = Response(
                {
                    "user_pk": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "message": "로그인 성공",
                    "token": {
                        "access": str(access_token),
                        "refresh": str(refresh_token),
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        try:
            # 현재 요청의 사용자의 refresh token을 가져옵니다.
            refresh_token = request.auth
            token = RefreshToken(refresh_token)

            # 토큰을 블랙리스트에 추가합니다.
            token.blacklist()

            request.session.flush()

            res = Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
            res.delete_cookie("access")

            return res
        except TokenError:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )


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
