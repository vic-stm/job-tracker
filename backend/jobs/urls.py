from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    ContactViewSet,
    JobApplicationViewSet,
    NoteViewSet,
    TechnologyViewSet,
)

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("applications", JobApplicationViewSet, basename="application")
router.register("notes", NoteViewSet, basename="note")
router.register("contacts", ContactViewSet, basename="contact")
router.register("technologies", TechnologyViewSet, basename="technology")

urlpatterns = router.urls
