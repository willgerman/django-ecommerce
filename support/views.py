from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import SupportForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.http import HttpResponseRedirect



class ContactView(FormView):
    template_name = "support/contact.html"  # Template for the contact page
    form_class = SupportForm

    def get_success_url(self):
        return reverse_lazy('support:support')  # Redirect for contact page submissions

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']

        email_message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=settings.DEFAULT_FROM_EMAIL,
            subject=subject,
            plain_text_content=f'From: {name} <{email}>\n\n{message}',
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(email_message)
            success_message = 'Your message has been sent successfully.'

            if response.status_code == 202:
                if self.request.POST.get('source') == 'footer':
                    # Add success message and redirect back to the same page with #footer
                    messages.success(self.request, success_message)
                    referer = self.request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(f"{referer}#footer")
                # Redirect for contact page submissions
                messages.success(self.request, success_message)
            else:
                error_message = f'Failed to send the email. Status code: {response.status_code}'
                if self.request.POST.get('source') == 'footer':
                    messages.error(self.request, error_message)
                    referer = self.request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(f"{referer}#footer")
                messages.error(self.request, error_message)
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            if self.request.POST.get('source') == 'footer':
                messages.error(self.request, error_message)
                referer = self.request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(f"{referer}#footer")
            messages.error(self.request, error_message)

        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'Invalid form submission. Please correct the errors and try again.'
        if self.request.POST.get('source') == 'footer':
            messages.error(self.request, error_message)
            referer = self.request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(f"{referer}#footer")
        messages.error(self.request, error_message)
        return super().form_invalid(form)