from django.conf import settings
from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "wishlist", "Wishlist"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    job_url = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(
        max_length=50, blank=True
    )  # LinkedIn, Naukri, referral...
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.APPLIED
    )
    applied_on = models.DateField(null=True, blank=True)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "status"])]

    def __str__(self):
        return f"{self.role} at {self.company}"


class StatusChange(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="status_changes"
    )
    from_status = models.CharField(max_length=20, choices=Application.Status.choices)
    to_status = models.CharField(max_length=20, choices=Application.Status.choices)
    changed_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)  # recruiter, referrer...
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)


class Note(models.Model):
    class Kind(models.TextChoices):
        INTERVIEW = "interview", "Interview"
        GENERAL = "general", "General"

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="notes"
    )
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.GENERAL)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
