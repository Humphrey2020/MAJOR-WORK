from django.contrib import admin
from django.contrib import admin
from .models import CustomUser, Candidate,Staff

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type')

class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'selected_university', 'selected_course')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Candidate, CandidateAdmin)

# Register your models here.
from django.contrib import admin
from .models import OTP, CustomUser

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'otp_code')
    readonly_fields = ('created_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing record
            return self.readonly_fields + ('user', 'otp_code')
        return self.readonly_fields

admin.site.register(OTP, OTPAdmin)
