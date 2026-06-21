from django import forms

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    inquiry_type = forms.ChoiceField(
        choices=[("", "Select option"), *ContactInquiry.INQUIRY_TYPES],
        label="Inquiry type",
        widget=forms.Select(attrs={"required": True}),
    )

    class Meta:
        model = ContactInquiry
        fields = (
            "full_name",
            "email",
            "phone_number",
            "company_name",
            "country",
            "job_title",
            "inquiry_type",
            "job_details",
        )
        labels = {
            "full_name": "Full name",
            "email": "Email address",
            "phone_number": "Phone number",
            "company_name": "Company name",
            "country": "Country",
            "job_title": "Job title",
            "job_details": "Job details",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "company_name": forms.TextInput(attrs={"placeholder": "Enter your company name"}),
            "country": forms.TextInput(attrs={"placeholder": "Enter your country"}),
            "job_title": forms.TextInput(attrs={"placeholder": "Enter your job title"}),
            "job_details": forms.Textarea(
                attrs={"placeholder": "Describe the job requirements", "rows": 5}
            ),
        }


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "admin@ai-solution.example"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
