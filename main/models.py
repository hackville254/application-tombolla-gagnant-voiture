from django.db import models
import uuid

OPERATEUR_CHOICES = [
    ('orange_money', 'Orange Money'),
    ('mtn_mobile_money', 'MTN Mobile Money'),
]

class Ticket(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    operateur = models.CharField(max_length=40, choices=OPERATEUR_CHOICES)
    numero_telephone = models.CharField(max_length=15)
    numero_ticket = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    paye = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    date_achat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.numero_ticket}"