from django.urls import path
from .views import login_view
from . import views
from . views import SendOTPView,GenerateSOPView,OTPLoginView,DashboardView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('sentotp/' ,views.SendOTPView.as_view()),
    path('generate_sop/',views.GenerateSOPView.as_view()),
    path('otp_check',views.OTPLoginView.as_view()),
    path('dashbord_views',views.DashboardView.as_view())
]
