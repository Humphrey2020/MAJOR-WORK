from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required 
from . models import Staff,Candidate
from django.shortcuts import render
#from django.contrib.auth.decorators import login_required, user_passes_test

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.user_type == 'staff':
                return redirect('staff_dashboard')
            elif user.user_type == 'candidate':
                return redirect('candidate_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')




def is_superadmin(user):
    return user.is_authenticated and user.user_type == 'superadmin'

#@login_required
#@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    return render(request, 'superadmin.html')


#@login_required
def staff(request):
    try:
        staff = request.user.Staff # Accessing the Staff profile using the related_name
    except Staff.DoesNotExist:
        return HttpResponse("Staff profile not found.")
    return render(request, 'staff.html', {'staff': staff})

#@login_required
def candidate_dashboard(request):
    try:
        candidate = request.user.Candidate  # Accessing the Candidate profile using the related_name
    except Candidate.DoesNotExist:
        return HttpResponse("Candidate profile not found.")
    return render(request, 'candidate.html', {'candidate': candidate})    






from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Staff, Candidate, CustomUser, OTP
from .serializers import StaffSerializer, CandidateSerializer, CustomUserSerializer
from django.core.mail import send_mail
import random
import openai

# Admin View to Send OTP
class SendOTPView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(user=user, otp_code=otp_code)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'admin@yourdomain.com',
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

# Candidate View to Generate SOP using OpenAI
class GenerateSOPView(APIView):
    def post(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, id=candidate_id)
        openai.api_key = 'your-openai-api-key'
        
        prompt = f"Write a statement of purpose for a candidate named {candidate.full_name} who is applying to {candidate.selected_university} for the course {candidate.selected_course}."
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        
        sop_text = response['choices'][0]['text'].strip()
        candidate.sop = sop_text
        candidate.save()
        
        return Response({'sop': sop_text}, status=status.HTTP_200_OK)

# Login Endpoint to Handle OTP Verification
class OTPLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')
        
        user = get_object_or_404(CustomUser, username=username)
        otp = get_object_or_404(OTP, user=user, otp_code=otp_code, is_used=False)
        
        if otp and not otp.is_used:
            otp.is_used = True
            otp.save()
            return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP or OTP already used.'}, status=status.HTTP_400_BAD_REQUEST)

# View to Get User Dashboard Data
class DashboardView(APIView):
    def get(self, request):
        user = request.user
        if user == 'staff':
            staff_profile = get_object_or_404(Staff, user=user)
            serializer = StaffSerializer(staff_profile)
        elif user == 'candidate':
            candidate_profile = get_object_or_404(Candidate, user=user)
            serializer = CandidateSerializer(candidate_profile)
        else:
            return Response({'message': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
