from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Resume(models.Model):
    FILE_TYPE_CHOICES = [
        ("pdf", "PDF"),
        ("docx", "DOCX"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="resumes/")
    file_type = models.CharField(max_length=4, choices=FILE_TYPE_CHOICES)
    is_default = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.name} ({self.user})"


class JobApplication(models.Model):
    JOB_TYPE_CHOICES = [
        ("full-time", "Full-time"),
        ("part-time", "Part-time"),
        ("contract", "Contract"),
        ("freelance", "Freelance"),
    ]

    STATUS_CHOICES = [
        ("wishlist", "Wishlist"),
        ("applied", "Applied"),
        ("screening", "Screening"),
        ("interview", "Interview"),
        ("technical-test", "Technical Test"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("withdrawn", "Withdrawn"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    application_url = models.URLField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="wishlist"
    )
    date_applied = models.DateField()
    recruiter_name = models.CharField(max_length=200, blank=True)
    recruiter_email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    job_description = models.TextField()
    ai_match_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    selected_resume = models.ForeignKey(
        Resume,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_applications",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"


class AIAnalysis(models.Model):
    MATCH_LEVEL_CHOICES = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("strong", "Strong"),
    ]

    application = models.OneToOneField(
        JobApplication, on_delete=models.CASCADE, related_name="ai_analysis"
    )
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="ai_analyses"
    )
    match_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    match_level = models.CharField(max_length=10, choices=MATCH_LEVEL_CHOICES)
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    areas_for_improvement = models.JSONField(default=list)
    keyword_suggestions = models.JSONField(default=list)
    overall_recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Analysis for {self.application}"


class InterviewPrep(models.Model):
    application = models.OneToOneField(
        JobApplication, on_delete=models.CASCADE, related_name="interview_prep"
    )
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    required_skills = models.JSONField(default=list)
    technical_questions = models.JSONField(default=list)
    behavioral_questions = models.JSONField(default=list)
    project_based_questions = models.JSONField(default=list)
    prep_tips = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview Prep for {self.application}"
