from django.contrib import admin
from .models import Ticket
# Register your models here.
# Personnalisation de l’administration des tickets de tombola
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('numero_ticket','reference_paiement', 'paye', 'nom', 'prenom', 'operateur', 'numero_telephone', 'date_achat')
    list_filter = ('paye', 'operateur', 'date_achat')
    search_fields = ('numero_ticket', 'nom', 'prenom', 'numero_telephone', 'reference_paiement')
    ordering = ('-date_achat',)
