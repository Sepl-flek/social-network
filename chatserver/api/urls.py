from rest_framework.routers import SimpleRouter

from api.views import RoomsViewsSet

router = SimpleRouter()
router.register(r"rooms", RoomsViewsSet)

urlpatterns = router.urls