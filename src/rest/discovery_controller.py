from typing import List
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from src.rest.dto.discovery_history_dto import DiscoveryHistoryDto
from src.rest.dto.discovery_stats_dto import DiscoveryStatsDto
from src.rest.dto.popular_discovery_dto import PopularDiscoveryDto
from src.rest.dto.scan_discovery_dto import ScanDiscoveryDto
from src.rest.dto.scan_discovery_request_dto import ScanDiscoveryRequestDto
from src.rest.dto.undiscovered_item_dto import UndiscoveredItemDto
from src.service.discovery_service import DiscoveryService


class DiscoveryController(viewsets.ViewSet):
    base_route = "api/v1/discoveries"

    def __init__(self, discovery_service: DiscoveryService, **kwargs):
        super().__init__(**kwargs)
        self.discovery_service = discovery_service

    @action(detail=False, methods=['POST'])
    def scan(self, request) -> Response:
        """
        POST /api/v1/discoveries/scan/
        Process a new discovery from image scan
        """
        try:
            scan_request: ScanDiscoveryRequestDto = request.data
            discovery_result: ScanDiscoveryDto = self.discovery_service.process_discovery(
                user_id=request.user.id,
                item_name=scan_request['image']
            )
            return Response(discovery_result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def history(self, request) -> Response:
        """
        GET /api/v1/discoveries/history/
        Get user's discovery history
        """
        try:
            history: List[DiscoveryHistoryDto] = self.discovery_service.get_user_discoveries(
                user_id=request.user.id
            )
            return Response(history, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def stats(self, request) -> Response:
        """
        GET /api/v1/discoveries/stats/
        Get user's discovery statistics
        """
        try:
            stats: DiscoveryStatsDto = self.discovery_service.get_discovery_statistics(
                user_id=request.user.id
            )
            return Response(stats, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def undiscovered(self, request) -> Response:
        """
        GET /api/v1/discoveries/undiscovered/
        Get items not yet discovered by user
        """
        try:
            items: List[UndiscoveredItemDto] = self.discovery_service.get_undiscovered_items(
                user_id=request.user.id
            )
            return Response(items, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def popular(self, request) -> Response:
        """
        GET /api/v1/discoveries/popular/
        Get most commonly discovered items
        """
        try:
            popular_items: List[PopularDiscoveryDto] = self.discovery_service.get_popular_discoveries()
            return Response(popular_items, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
