from django.shortcuts import render
from django.shortcuts import render, redirect
from main.models import Ticket
from .forms import TicketForm
from .Soleaspay_Request import create_payment

def jouer(request):
    ticket = None
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            # Simuler le paiement ici (à adapter selon ton système) 
            # ticket.paye = True
            service = 1 if ticket.operateur == "mtn_mobile_money" else 2
            print("Ticket créé avec ID :", ticket.id , ticket.nom , ticket.prenom , ticket.operateur , ticket.numero_telephone , ticket.paye , "service",service)
            ticket.save()
            reference = create_payment(
                wallet=ticket.numero_telephone,
                amount=100,
                order_id=str(ticket.id),
                description="Achat de ticket",
                payer=f"{ticket.nom} {ticket.prenom}",
                payer_email="support@djanguibet.com",
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
                service= service
            ) 
            print(reference , ticket.id)
            ticket.reference_paiement = reference
            ticket.save()
            return render(request, 'pending_payment.html', {'ticket': ticket})
    else:
        form = TicketForm()
    return render(request, 'jouer.html', {'form': form, 'ticket': ticket})


def all_tickets(request):
    form = TicketForm()
    tickets = []
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            operateur = form.cleaned_data['operateur']
            numero_telephone = form.cleaned_data['numero_telephone']
            tickets = Ticket.objects.filter(
                nom=nom,
                prenom=prenom,
                operateur=operateur,
                numero_telephone=numero_telephone
            )
    return render(request, 'all_tickets.html', {'form': form, 'tickets': tickets})

def index(request):
    return render(request, 'index.html')

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import hashlib

# Secret partagé avec Soleaspay
SOLEASPAY_SECRET = "0o0kyO-w0YD6t2Z_BpGv4KZeF9t7l5GDGt5sJELhaG8"

@csrf_exempt
def callback_soleaspay(request):
    try:
        # ✅ Vérification du hash SHA512 dans le header
        received_hash = request.headers.get("X-Private-Key", "")
        valid_hash = hashlib.sha512(SOLEASPAY_SECRET.encode('utf-8')).hexdigest()

        if received_hash != valid_hash:
            print("❌ Tentative non autorisée (hash invalide)")
            return HttpResponse("Unauthorized", status=401)

        # ✅ Lecture du JSON
        body = request.body.decode('utf-8')
        data = json.loads(body)

        reference = data.get('data', {}).get('reference', None)
        status = data.get('status', None)

        if reference and status == "SUCCESS":
            ticket = get_object_or_404(Ticket, reference_paiement=reference)
            ticket.paye = True
            ticket.save()

            print(f"✅ Paiement confirmé pour le ticket {reference}")
            return HttpResponse("OK", status=200)

        print(f"⚠ Référence ou statut invalide ({reference}, status={status})")
        return HttpResponse("Bad Request", status=400)

    except Exception as e:
        print("🚨 Erreur callback Soleaspay:", e)
        return HttpResponse("Server Error", status=500)