import os
import pyotp
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import OTP
from .forms import OTPForm, EmailForm

def send_otp_via_sendgrid(email, otp_code):
    subject = 'Your OTP for Changing Your Password'
    message_content = f'Your OTP for changing your password is: {otp_code}'
    from_email = 'support@fntn-mugs.com'  
    message = Mail(
        from_email=from_email,
        to_emails=email,
        subject=subject,
        plain_text_content=message_content
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)  
    except Exception as e:
        print(f"Error sending OTP via SendGrid: {e}")

# Send OTP View
class SendOTPView(FormView):
    template_name = 'otp/send_otp.html'
    success_url = reverse_lazy('otp_auth:verify_otp')
    form_class = EmailForm

    def form_valid(self, form):
        email = form.cleaned_data['email']  # Retrieves validated data
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            otp_secret = pyotp.random_base32()  # Generates secret key
            otp = pyotp.TOTP(otp_secret)
            otp_code = otp.now()  # Calculates OTP based on timestamp and key

            otp_obj, created = OTP.objects.get_or_create(user=user, email=email)
            otp_obj.otp_secret = otp_secret
            otp_obj.save()

            send_otp_via_sendgrid(email, otp_code)

            # Store the email in session for verification
            self.request.session['reset_email'] = email

            return super().form_valid(form)
        else:
            form.add_error('email', 'Email not found')
            return self.form_invalid(form)

class VerifyOTPView(FormView):
    template_name = 'otp/verify_otp.html'
    success_url = reverse_lazy('accounts:reset_password')
    form_class = OTPForm

    def form_valid(self, form):
        otp_code = form.cleaned_data['otp']
        email = self.request.session.get('reset_email')

        if not email:
            return redirect('otp_auth:send_otp')

        otp_obj = OTP.objects.filter(email=email).first()

        if otp_obj:
            otp = pyotp.TOTP(otp_obj.otp_secret)
            print(f"OTP Secret: {otp_obj.otp_secret}")
            print(f"Expected OTP: {otp.now()}, Entered OTP: {otp_code}")

            if otp.verify(otp_code, valid_window=1):  
                otp_obj.is_verified = True
                otp_obj.save()
                messages.success(self.request, "OTP verified successfully.")
                return super().form_valid(form)
            else:
                messages.error(self.request, "Invalid OTP. Please try again.")
                return self.form_invalid(form)
        else:
            messages.error(self.request, "OTP not found.")
            return self.form_invalid(form)

