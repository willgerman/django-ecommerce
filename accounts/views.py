from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, PasswordResetForm, CustomUserCreationForm, EmailResetForm, UpdateNameForm

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')

        # Authenticate user
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            # Log the user in and redirect to the dashboard
            login(self.request, user)
            return super().form_valid(form)
        else:
            # If login fails, add error and render form again
            messages.error(self.request, "Invalid email or password")
            return self.form_invalid(form)  # Render form with errors if authentication fails

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('pages:index') 

class SignupView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:dashboard')  # Redirect to dashboard after signup

    def form_valid(self, form):
        # Save the user but don't commit to the database yet
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Hash the password
        user.is_signed_agreement = timezone.now()  # Set agreement time
        user.save()  # Save user to the database

        # Log the user in after signup
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the error below.")
        return super().form_invalid(form)

class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'

@method_decorator(login_required, name='dispatch')
class ResetPasswordView(FormView):
    template_name = 'accounts/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('accounts:dashboard')  # Redirect after successful password reset

    def dispatch(self, request, *args, **kwargs):
        # Check if 'reset_email' is in session, otherwise redirect to login
        if 'reset_email' not in request.session:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.session.get('reset_email')
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            # Set the new password
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            
            # Log the user in and clear the session
            login(self.request, user)
            self.request.session.pop('reset_email', None)

            return super().form_valid(form)  # Redirects to success_url
        else:
            # Redirect to login if user not found
            return redirect('accounts:login')
        
@method_decorator(login_required, name='dispatch')  # Ensure the user is logged in
class ChangeEmailView(FormView):
    template_name = 'accounts/update_email.html'  
    form_class = EmailResetForm  
    success_url = reverse_lazy('accounts:dashboard') 

    def form_valid(self, form):
        current_email = form.cleaned_data['current_email']
        new_email = form.cleaned_data['new_email']
        confirm_new_email = form.cleaned_data['confirm_new_email']
        
        user = get_user_model().objects.filter(email=current_email).first()

        if user:
            # Check if the new email matches the confirmation email
            if new_email == confirm_new_email:
                # Change the user's email
                user.email = new_email
                user.save()
                messages.success(self.request, "Your email address has been successfully updated.")
                return super().form_valid(form)
            else:
                form.add_error('confirm_new_email', "New email and confirmation email do not match.")
                return self.form_invalid(form)
        else:
            form.add_error('current_email', "Current email address not found.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your email address.")
        return super().form_invalid(form)
    

@method_decorator(login_required, name='dispatch')  # Ensure the user is logged in
class ChangeNameView(FormView):
    template_name = 'accounts/update_name.html'  
    form_class = UpdateNameForm  
    success_url = reverse_lazy('accounts:change_name') 

    def form_valid(self, form):
        user = self.request.user  # Get the currently logged-in user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()  # Save the updated user information

        messages.success(self.request, "Your name has been successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your name.")
        return super().form_invalid(form)
