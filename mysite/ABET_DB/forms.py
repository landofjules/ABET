from django import forms
from django.core.exceptions import ValidationError

from ABET_DB.models import performanceLevels

class performanceLevelsForm(forms.ModelForm):
    
    confirm_achievementLevel = forms.EmailField(
        label="Confirm performanceLevel", 
        required=True,
    )
    
    class Meta:
        model = performanceLevels
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        
        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_achievementLevel'] = email
        
        return super(performanceLevelsForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        
        if(self.cleaned_data.get('email') != self.cleaned_data.get('confirm_email')):
            raise ValidationError(
                "Email addresses must match."
            )
            
        return self.cleaned_data