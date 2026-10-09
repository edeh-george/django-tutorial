from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .serializers import LoginSerializer

User = get_user_model()


class LoginView(APIView):
    authentication_classes = (TokenAuthentication,)
    parser_classes = (JSONParser,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            user = User.objects.get(username__iexact=data["username"])
            if user.check_password(data["password"]):
                token = Token.objects.create(user=user)
                request.session["_user_id"] = user.id
                return Response(
                    {
                        "message": "Login successful",
                        "data": {"user": user.username, "user_token": token},
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentails, username or password incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as ve:
            return Response(
                {"error": ve.detail, "message": "Please check the inforamation passed"},
                status=400,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User matching credentials oes not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_userprofile(request):
    user = request.user
    return Response({"username": user.username, "email": user.email})
