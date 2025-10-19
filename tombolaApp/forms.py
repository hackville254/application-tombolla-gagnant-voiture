from django import forms
from main.models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nom', 'prenom', 'operateur', 'numero_telephone']