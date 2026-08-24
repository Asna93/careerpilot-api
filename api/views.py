import random

from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AIAnalysis, InterviewPrep, JobApplication, Resume
from .serializers import (
    AIAnalysisSerializer,
    InterviewPrepSerializer,
    JobApplicationSerializer,
    RegisterSerializer,
    ResumeSerializer,
    UserSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=201,
        )


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user', 'is_default']
    ordering_fields = ['uploaded_at', 'name']

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this resume.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this resume.")
        instance.delete()


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'job_type', 'user']
    search_fields = ['company_name', 'job_title']
    ordering_fields = ['created_at', 'date_applied']

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this application."
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this application."
            )
        instance.delete()


class AIAnalysisViewSet(viewsets.ModelViewSet):
    queryset = AIAnalysis.objects.all()
    serializer_class = AIAnalysisSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['application', 'match_level']

    def get_queryset(self):
        return AIAnalysis.objects.filter(application__user=self.request.user)

    def perform_create(self, serializer):
        application = serializer.validated_data.get('application')

        # Check permissions
        if application and application.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to create analysis for this application."
            )

        # Generate MOCK/DUMMY data (no real AI)
        mock_data = {
            'match_score': random.randint(70, 88),
            'match_level': random.choice(['low', 'moderate', 'strong']),
            'matching_skills': ['React', 'Django', 'Python', 'TypeScript', 'PostgreSQL', 'REST API'],
            'missing_skills': ['Docker', 'AWS', 'Kubernetes', 'CI/CD'],
            'strengths': [
                'Strong backend experience with Django and Python',
                'Frontend skills with React and modern JavaScript',
                'Database design and optimization expertise',
            ],
            'areas_for_improvement': [
                'Cloud deployment experience (AWS, Docker)',
                'DevOps and CI/CD pipeline knowledge',
                'Mobile development skills',
            ],
            'keyword_suggestions': ['Docker', 'AWS', 'Kubernetes', 'CI/CD', 'GraphQL', 'Microservices', 'TDD', 'Agile'],
            'overall_recommendation': 'Good fit for this role. Consider adding cloud and DevOps skills to strengthen your profile.',
        }

        # Save with mock data
        serializer.save(
            match_score=mock_data['match_score'],
            match_level=mock_data['match_level'],
            matching_skills=mock_data['matching_skills'],
            missing_skills=mock_data['missing_skills'],
            strengths=mock_data['strengths'],
            areas_for_improvement=mock_data['areas_for_improvement'],
            keyword_suggestions=mock_data['keyword_suggestions'],
            overall_recommendation=mock_data['overall_recommendation'],
        )

    def perform_update(self, serializer):
        if serializer.instance.application.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this analysis.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.application.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this analysis."
            )
        instance.delete()


class InterviewPrepViewSet(viewsets.ModelViewSet):
    queryset = InterviewPrep.objects.all()
    serializer_class = InterviewPrepSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['application']

    def get_queryset(self):
        return InterviewPrep.objects.filter(application__user=self.request.user)

    def perform_create(self, serializer):
        application = serializer.validated_data.get('application')
        if application and application.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to create prep for this application."
            )
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.application.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this prep.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.application.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this prep.")
        instance.delete()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        if serializer.instance != self.request.user:
            raise PermissionDenied("You do not have permission to edit this user.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance != self.request.user:
            raise PermissionDenied("You do not have permission to delete this user.")
        instance.delete()
