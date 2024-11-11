from typing import List
from src.rest.dto.skin_dto import SkinDto
from src.service.skin_service import SkinService
from src.rest.dto.owned_skin_dto import OwnedSkinDto
from src.rest.dto.skin_equip_dto import SkinEquipDto
from src.rest.dto.skin_stats_dto import SkinStatsDto
from src.rest.dto.skin_purchase_dto import SkinPurchaseDto
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class SkinController(viewsets.ViewSet):
    base_route = "api/v1/skins"

    def __init__(self, skin_service: SkinService, **kwargs):
        super().__init__(**kwargs)
        self.skin_service = skin_service

    @action(detail=False, methods=['GET'])
    def available(self, request) -> Response:
        """
        GET /api/v1/skins/available/
        Get all skins available for purchase (not owned by user)
        """
        try:
            available_skins: List[SkinDto] = self.skin_service.get_available_skins(
                user_id=request.user.id
            )
            return Response(available_skins, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def owned(self, request) -> Response:
        """
        GET /api/v1/skins/owned/
        Get all skins owned by the user
        """
        try:
            owned_skins: List[OwnedSkinDto] = self.skin_service.get_user_skins(
                user_id=request.user.id
            )
            return Response(owned_skins, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def purchase(self, request, pk=None) -> Response:
        """
        POST /api/v1/skins/{skin_id}/purchase/
        Purchase a specific skin
        """
        try:
            purchase_result: SkinPurchaseDto = self.skin_service.purchase_skin(
                user_id=request.user.id,
                skin_id=pk
            )
            return Response(purchase_result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def equip(self, request, pk=None) -> Response:
        """
        POST /api/v1/skins/{skin_id}/equip/
        Equip a specific skin
        """
        try:
            equip_result: SkinEquipDto = self.skin_service.equip_skin(
                user_id=request.user.id,
                skin_id=pk
            )
            return Response(equip_result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def stats(self, request) -> Response:
        """
        GET /api/v1/skins/stats/
        Get statistics about user's skin collection
        """
        try:
            stats: SkinStatsDto = self.skin_service.get_skin_statistics(
                user_id=request.user.id
            )
            return Response(stats, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
