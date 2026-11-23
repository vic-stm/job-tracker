from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, JobApplicationViewSet, NoteViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("applications", JobApplicationViewSet, basename="application")
router.register("notes", NoteViewSet, basename="note")

urlpatterns = router.urls
