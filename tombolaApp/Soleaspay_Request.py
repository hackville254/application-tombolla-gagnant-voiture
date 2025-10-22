import uuid
import requests

# ---------------------
# Constants
# ---------------------
API_URL = "https://soleaspay.com/api/agent/bills/v3"
API_KEY = "Hmw-dz3boodH1W9rpAeC07CPaFL3ixTv6cGCyxmrQz4-AP"
OPERATION = 2  # Must be integer as per API docs

# ---------------------
# Payment Function
# ---------------------
def create_payment(
    wallet: str,
    amount: float,
    order_id: str,
    description: str,
    payer: str,
    payer_email: str,
    success_url: str,
    failure_url: str,
    service: int
) -> dict:
    """
    Create a payment request to SoleasPay API.

    Returns a dict containing either JSON response or error info.
    """
    print("Creating payment with the following details:")
    print(f"Wallet: {wallet}")
    print(f"Amount: {amount}")
    print(f"Order ID: {order_id}")
    print(f"Description: {description}")
    print(f"payer: {payer}")
    print(f"payer_email: {payer_email}")
    print(f"success_url: {success_url}")
    print(f"failure_url: {failure_url}")
    print(f"service: {service}")

    payload = {
        "wallet": wallet,
        "amount": amount,
        "currency": "XAF",
        "order_id": order_id,
        "description": description,
        "payer": payer,
        "payerEmail": payer_email
    }

    headers = {
        "x-api-key": API_KEY,
        "operation": str(OPERATION),
        "service": str(service),
        "Content-Type": "application/json"
    }
    print('payload:', payload)
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    # Debug output
    print("\n--- HTTP RESPONSE DEBUG ---")
    print("Status:", response.status_code)
    print("Raw Response:", response.text)

    # Parse JSON safely
    try:
        data = response.json()
        print('data:', data)
        reference = data.get('data', {}).get('reference', None)
        return reference
    except ValueError:
        return {
            "error": "Invalid JSON response",
            "status_code": response.status_code,
            "raw_response": response.text
        }

# ---------------------
# Main execution "987654322", "987654320", "987654321"
# ---------------------
# if __name__ == "__main__":
#     wallets = ["987654322", "987654320", "987654321"]
#     for wallet in wallets:
#         response = create_payment(
#             wallet=wallet,
#             amount=1000,
#             order_id=str(uuid.uuid4()),
#             description="Test payment",
#             payer="John Doe",
#             payer_email="john.doe@example.com",
#             success_url="https://example.com/success",
#             failure_url="https://example.com/failure",
#             service=36
#         )
#         print(f"\nResponse for wallet {wallet}:\n{response}")
