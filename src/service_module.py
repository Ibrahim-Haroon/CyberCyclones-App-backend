from src.service.auth_service import AuthService
from src.service.user_service import UserService
from src.util.singleton import singleton
from src.repository.user_repository import UserRepository
from src.service.points_service import PointsService
from src.service.discovery_service import DiscoveryService
from src.service.leaderboard_service import LeaderboardService
from src.service.skin_service import SkinService


@singleton
class ServiceModule:
    def __init__(self):
        self.user_repository = UserRepository()

        self.auth_service = AuthService(
            user_repository=self.user_repository
        )

        self.user_service = UserService(
            user_repository=self.user_repository
        )

        self.points_service = PointsService(
            user_repository=self.user_repository
        )

        self.discovery_service = DiscoveryService(
            user_repository=self.user_repository,
            points_service=self.points_service
        )

        self.leaderboard_service = LeaderboardService(
            user_repository=self.user_repository
        )

        self.skin_service = SkinService(
            user_repository=self.user_repository,
            points_service=self.points_service
        )
