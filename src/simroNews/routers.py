from rest_framework.routers import DefaultRouter


from app.viewset import *

router = DefaultRouter()

router.register('typeActeur', TypeACteurViewSet, basename='type-acteur')

urlpatterns = router.urls