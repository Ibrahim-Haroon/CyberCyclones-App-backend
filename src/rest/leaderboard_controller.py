from typing import List
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.rest.dto.category_leaderboard_dto import CategoryLeaderboardDto
from src.rest.dto.global_leaderboard_dto import GlobalLeaderboardDto
from src.rest.dto.nearby_ranking_dto import NearbyRankingDto
from src.rest.dto.user_ranking_dto import UserRankingDto
from src.rest.dto.weekly_leaderboard_dto import WeeklyLeaderboardDto
from src.service_module import ServiceModule


class LeaderboardController(viewsets.ViewSet):
    base_route = "api/v1/leaderboard"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        __service_module = ServiceModule()
        self.leaderboard_service = __service_module.leaderboard_service

    @action(detail=False, methods=['GET'])
    def global_rankings(self, request) -> Response:
        """
        GET /api/v1/leaderboard/global/
        Get global leaderboard rankings
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            rankings: List[GlobalLeaderboardDto] = self.leaderboard_service.get_global_leaderboard(
                limit=limit
            )
            return Response(rankings, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def weekly(self, request) -> Response:
        """
        GET /api/v1/leaderboard/weekly/
        Get weekly leaderboard rankings
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            rankings: List[WeeklyLeaderboardDto] = self.leaderboard_service.get_weekly_leaderboard(
                limit=limit
            )
            return Response(rankings, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def category(self, request, pk=None) -> Response:
        """
        GET /api/v1/leaderboard/category/{category}/
        Get category-specific leaderboard (pk is the category name)
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            rankings: List[CategoryLeaderboardDto] = self.leaderboard_service.get_category_leaderboard(
                category=pk,
                limit=limit
            )
            return Response(rankings, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def my_ranking(self, request) -> Response:
        """
        GET /api/v1/leaderboard/my_ranking/
        Get detailed ranking information for current user
        """
        try:
            ranking: UserRankingDto = self.leaderboard_service.get_user_ranking_details(
                user_id=request.user.id
            )
            return Response(ranking, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def nearby(self, request) -> Response:
        """
        GET /api/v1/leaderboard/nearby/
        Get rankings for users nearby in rank
        """
        try:
            range_value = int(request.query_params.get('range', 2))
            rankings: List[NearbyRankingDto] = self.leaderboard_service.get_nearby_rankings(
                user_id=request.user.id,
                range=range_value
            )
            return Response(rankings, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
