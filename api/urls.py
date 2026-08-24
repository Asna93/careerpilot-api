from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'resumes', views.ResumeViewSet, basename='resume')
router.register(r'applications', views.JobApplicationViewSet, basename='application')
router.register(r'ai-analysis', views.AIAnalysisViewSet, basename='ai-analysis')
router.register(r'interviews', views.InterviewPrepViewSet, basename='interview')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = router.urls
