from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.service.user_service import UserService
from src.rest.dto.user_profile_dto import UserProfileDto
from src.rest.dto.update_display_name_dto import UpdateDisplayNameDto
from src.rest.dto.update_dsiplay_name_request_dto import UpdateDisplayNameRequestDto


class UserController(viewsets.ViewSet):
    base_route = "api/v1/users"

    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self.user_service = user_service

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def profile(self, request) -> Response:
        """
        GET /api/v1/users/profile/
        Get current user's profile information
        """
        try:
            profile: UserProfileDto = self.user_service.get_profile(
                user_id=request.user.id
            )
            return Response(profile, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_display_name(self, request) -> Response:
        """
        PATCH /api/v1/users/update_display_name/
        Update user's display name
        """
        try:
            update_request: UpdateDisplayNameRequestDto = request.data
            updated_profile: UpdateDisplayNameDto = self.user_service.update_display_name(
                user_id=request.user.id,
                new_display_name=update_request['display_name']
            )
            return Response(updated_profile, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def deactivate(self, request) -> Response:
        """
        POST /api/v1/users/deactivate/
        Deactivate current user's account
        """
        try:
            self.user_service.deactivate_user(request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def reactivate(self, request) -> Response:
        """
        POST /api/v1/users/reactivate/
        Reactivate current user's account
        """
        try:
            self.user_service.reactivate_user(request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def by_username(self, request, pk=None) -> Response:
        """
        GET /api/v1/users/by_username/{username}/
        Get public profile information for any user by username
        Only returns non-sensitive info for other users
        """
        try:
            user = self.user_service.get_user_by_username(username=pk)
            if not user:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Return limited info if viewing other user's profile
            if user.id != request.user.id:
                return Response({
                    "username": user.username,
                    "display_name": user.display_name,
                    "rank_title": user.rank_title,
                    "total_points_earned": user.total_points_earned,
                    "active_skin_id": user.active_skin.id
                }, status=status.HTTP_200_OK)

            # Return full profile if viewing own profile
            profile: UserProfileDto = self.user_service.get_profile(user.id)
            return Response(profile, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def exists(self, request, pk=None) -> Response:
        """
        GET /api/v1/users/exists/{username}/
        Check if username exists (for registration)
        """
        try:
            user = self.user_service.get_user_by_username(username=pk)
            return Response({
                "exists": user is not None
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
