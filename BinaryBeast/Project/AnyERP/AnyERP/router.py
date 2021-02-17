from rest_framework import routers

from saraswati_enterprises.views import ProductViewset

router = routers.DefaultRouter()
router.register('products', ProductViewset)