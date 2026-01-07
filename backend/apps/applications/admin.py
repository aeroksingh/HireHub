from django.contrib import admin
from django.core.mail import send_mail
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "status", "applied_at")
    list_filter = ("status", "job")
    search_fields = ("candidate__email", "job__title")

    actions = ["mark_shortlisted", "mark_rejected"]

    def mark_shortlisted(self, request, queryset):
        for application in queryset:
            application.status = "SHORTLISTED"
            application.save()

            # 📧 SEND EMAIL
            send_mail(
                subject="You are shortlisted 🎉",
                message=(
                    f"Congratulations!\n\n"
                    f"You have been shortlisted for the role:\n"
                    f"{application.job.title}\n\n"
                    f"Our team will contact you soon."
                ),
                from_email=None,
                recipient_list=[application.candidate.email],
            )

        self.message_user(request, "Selected applications marked as SHORTLISTED")

    mark_shortlisted.short_description = "Shortlist selected candidates"

    def mark_rejected(self, request, queryset):
        queryset.update(status="REJECTED")
        self.message_user(request, "Selected applications marked as REJECTED")

    mark_rejected.short_description = "Reject selected candidates"
