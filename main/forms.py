from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, HiringRequest


INPUT_CLASSES = (
    "min-h-11 w-full rounded-sm border border-[#fdb515] bg-white px-4 py-2.5 "
    "text-sm text-slate-950 outline-none transition placeholder:text-slate-500 "
    "focus:border-[#003577] focus:ring-2 focus:ring-[#003577]/20"
)


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "phone", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": _("نام"),
                    "autocomplete": "name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": _("تلفن"),
                    "autocomplete": "tel",
                    "inputmode": "tel",
                    "dir": "ltr",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": f"{INPUT_CLASSES} min-h-36 resize-y",
                    "placeholder": _("متن پیام"),
                    "rows": 5,
                }
            ),
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_message(self):
        return self.cleaned_data["message"].strip()


class HiringRequestForm(forms.ModelForm):
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    class Meta:
        model = HiringRequest
        fields = (
            "full_name",
            "phone",
            "email",
            "desired_position",
            "experience_years",
            "message",
            "resume",
        )
        labels = {
            "full_name": _("نام و نام خانوادگی"),
            "phone": _("شماره تماس"),
            "email": _("ایمیل"),
            "desired_position": _("عنوان شغلی موردنظر"),
            "experience_years": _("سابقه کار (سال)"),
            "message": _("درباره خودتان"),
            "resume": _("فایل رزومه"),
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": INPUT_CLASSES, "autocomplete": "name"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "autocomplete": "tel",
                    "inputmode": "tel",
                    "dir": "ltr",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "autocomplete": "email",
                    "dir": "ltr",
                }
            ),
            "desired_position": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "experience_years": forms.NumberInput(
                attrs={"class": INPUT_CLASSES, "min": "0", "max": "60"}
            ),
            "message": forms.Textarea(
                attrs={"class": f"{INPUT_CLASSES} min-h-36 resize-y", "rows": 5}
            ),
            "resume": forms.ClearableFileInput(
                attrs={
                    "class": (
                        "block min-h-12 w-full cursor-pointer rounded-sm border "
                        "border-[#fdb515] bg-white text-sm text-slate-700 "
                        "file:me-4 file:min-h-12 file:border-0 file:bg-[#003577] "
                        "file:px-5 file:text-sm file:font-bold file:text-white "
                        "hover:file:bg-[#002a60] focus-visible:outline-2 "
                        "focus-visible:outline-offset-2 focus-visible:outline-[#003577]"
                    ),
                    "accept": ".pdf,.doc,.docx",
                }
            ),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot", "")
        if value:
            raise forms.ValidationError(_("درخواست نامعتبر است."))
        return value

    def clean_full_name(self):
        return self.cleaned_data["full_name"].strip()

    def clean_desired_position(self):
        return self.cleaned_data["desired_position"].strip()

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError(
                _("لطفاً حداقل ۲۰ نویسه درباره خودتان بنویسید.")
            )
        return message
