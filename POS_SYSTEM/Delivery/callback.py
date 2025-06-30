from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import MpesaTransaction, Delivery
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_callback(request):
    try:
        # Parse callback data
        data = json.loads(request.body)
        result = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = result.get('CheckoutRequestID')
        result_code = str(result.get('ResultCode'))
        result_desc = result.get('ResultDesc')

        # Find the transaction
        transaction = MpesaTransaction.objects.filter(checkout_request_id=checkout_request_id).first()
        if not transaction:
            logger.error(f"No transaction found for CheckoutRequestID: {checkout_request_id}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Transaction not found"}, status=404)

        # Update transaction based on result code
        if result_code == "0":
            # Successful payment
            transaction.status = "completed"
            transaction.mpesa_receipt_number = result.get('CallbackMetadata', {}).get('Item', [{}])[1].get('Value')
            transaction.result_code = result_code
            transaction.result_desc = result_desc
            transaction.delivery.is_paid = True
            transaction.delivery.save()
            logger.info(f"Payment successful for delivery {transaction.delivery.parcel_id}")
        else:
            # Failed payment
            transaction.status = "failed"
            transaction.result_code = result_code
            transaction.result_desc = result_desc
            logger.error(f"Payment failed for delivery {transaction.delivery.parcel_id}: {result_desc}")

        transaction.save()
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback processed successfully"})
    except Exception as e:
        logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return JsonResponse(
            {"ResultCode": 1, "ResultDesc": f"Error processing callback: {str(e)}"},
            status=500
        )