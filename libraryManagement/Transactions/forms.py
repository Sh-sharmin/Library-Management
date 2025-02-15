from django import forms
from .models import DepositTransaction
class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositTransaction
        fields = ['amount',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user') 
        super().__init__(*args, **kwargs)

    def clean_amount(self): 
        min_deposit_amount = 50
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.balance_after = self.user.balance
        return super().save()