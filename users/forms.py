from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import EmailMultiAlternatives

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, 
        help_text='Required, a valid email address.')

    class Meta:
        models = User
        fields = ('username', 'email', 'password1', 'password2')

class MyPasswordResetForm(forms.Form):

    username = forms.CharField(label=_('username'), max_length=150)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.EmailMultiAlternatives to 'to_email'.
        """
        subject = loader.render_to_string(subject_template_name, context)
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/hmtl')

        email_message.send()

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=none, html_email_template_name=None, 
             extra_mail_content=None):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        username = self.cleaned_data["username"]

        for user in self.get_users(username):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain_override

            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http'
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)