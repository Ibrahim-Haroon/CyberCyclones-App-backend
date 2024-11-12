from typing import List
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.service.points_service import PointsService
from src.rest.dto.points_summary_dto import PointsSummaryDto
from src.rest.dto.points_history_dto import PointsHistoryDto
from src.rest.dto.points_breakdown_dto import PointsBreakdownDto
from src.rest.dto.points_deduction_dto import PointsDeductionDto
from src.rest.dto.points_deduction_request_dto import PointsDeductionRequestDto


class PointsController(viewsets.ViewSet):
    base_route = "api/v1/points"

    def __init__(self, points_service: PointsService, **kwargs):
        super().__init__(**kwargs)
        self.points_service = points_service

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def summary(self, request) -> Response:
        """
        GET /api/v1/points/summary/
        Get user's points summary including current balance, total earned, and rank info
        """
        try:
            summary: PointsSummaryDto = self.points_service.get_points_summary(
                user_id=request.user.id
            )
            return Response(summary, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def history(self, request) -> Response:
        """
        GET /api/v1/points/history/
        Get points history with optional timeframe parameter
        """
        try:
            timeframe = request.query_params.get('timeframe', 'week')
            if timeframe not in ['week', 'month', 'year']:
                raise ValidationError("Invalid timeframe. Must be 'week', 'month', or 'year'")

            history: List[PointsHistoryDto] = self.points_service.get_points_history(
                user_id=request.user.id,
                timeframe=timeframe
            )
            return Response(history, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def breakdown(self, request) -> Response:
        """
        GET /api/v1/points/breakdown/
        Get detailed breakdown of how points were earned
        """
        try:
            breakdown: PointsBreakdownDto = self.points_service.get_points_breakdown(
                user_id=request.user.id
            )
            return Response(breakdown, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def deduct(self, request) -> Response:
        """
        POST /api/v1/points/deduct/
        Deduct points from user's balance
        """
        try:
            deduction_request: PointsDeductionRequestDto = request.data

            if not isinstance(deduction_request.get('points'), int) or deduction_request.get('points') <= 0:
                raise ValidationError("Points must be a positive integer")

            result: PointsDeductionDto = self.points_service.deduct_points(
                user_id=request.user.id,
                points=deduction_request['points']
            )
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
