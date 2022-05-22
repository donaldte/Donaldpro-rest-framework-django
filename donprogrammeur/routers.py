from rest_framework.routers import DefaultRouter
from apps.viewsets import ProductViewsets

router = DefaultRouter()
router.register('products-abc', ProductViewsets, basename="products")

urlpatterns = router.urls

