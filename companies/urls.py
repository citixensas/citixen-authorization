"""Companies Url's"""

from rest_framework import routers

from companies.views import CompanyViewSet, HeadquartersViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'headquarters', HeadquartersViewSet)

urlpatterns = router.urls
