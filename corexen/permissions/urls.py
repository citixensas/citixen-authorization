"""Group urls"""

from rest_framework import routers
from corexen.permissions.views import GroupTemplateViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupTemplateViewSet)

urlpatterns = router.urls
