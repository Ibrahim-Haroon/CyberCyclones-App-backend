from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.rest.dto.login_dto import LoginDto
from src.rest.dto.login_request_dto import LoginRequestDto
from src.rest.dto.password_change_dto import PasswordChangeDto
from src.rest.dto.password_change_request_dto import PasswordChangeRequestDto
from src.rest.dto.password_reset_dto import PasswordResetDto
from src.rest.dto.password_reset_request_dto import PasswordResetRequestDto
from src.rest.dto.register_user_dto import RegisterUserDto
from src.rest.dto.register_user_request_dto import RegisterUserRequestDto
from src.service.auth_service import AuthService


class AuthController(viewsets.ViewSet):
    base_route = "api/v1/auth"

    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = auth_service

    @action(detail=False, methods=['POST'])
    def register(self, request) -> Response:
        """
        POST /api/v1/auth/register/
        Register a new user
        """
        try:
            register_request: RegisterUserRequestDto = request.data
            user_data: RegisterUserDto = self.auth_service.register(
                username=register_request['username'],
                email=register_request['email'],
                password=register_request['password'],
                display_name=register_request.get('display_name')  # Optional
            )
            return Response(user_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request) -> Response:
        """
        POST /api/v1/auth/login/
        Authenticate user and return token
        """
        try:
            login_request: LoginRequestDto = request.data
            login_data: LoginDto = self.auth_service.login(
                username=login_request['username'],
                password=login_request['password']
            )
            return Response(login_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def reset_password_request(self, request) -> Response:
        """
        POST /api/v1/auth/reset_password_request/
        Request a password reset token
        """
        try:
            reset_request: PasswordResetRequestDto = request.data
            reset_data: PasswordResetDto = self.auth_service.generate_password_reset_token(
                email=reset_request['email']
            )
            return Response(reset_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def reset_password(self, request, pk=None) -> Response:
        """
        POST /api/v1/auth/reset_password/{reset_token}/
        Reset password using reset token
        """
        try:
            new_password = request.data.get('new_password')
            if not new_password:
                raise ValidationError("New password is required")

            success = self.auth_service.reset_password(
                token=pk,  # reset_token from URL
                new_password=new_password
            )
            return Response({"success": success}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def change_password(self, request) -> Response:
        """
        POST /api/v1/auth/change_password/
        Change password for authenticated user
        """
        try:
            change_request: PasswordChangeRequestDto = request.data
            change_data: PasswordChangeDto = self.auth_service.change_password(
                user_id=request.user.id,
                old_password=change_request['old_password'],
                new_password=change_request['new_password']
            )
            return Response(change_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
