import requests
import base64
from datetime import datetime, timedelta
import logging
import json
from django.conf import settings
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logger = logging.getLogger(__name__)

class MpesaService:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.base_url = getattr(settings, 'MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')
        self.access_token = None
        self.token_expiry = None
        
        logger.debug(f"MpesaService initialized with: URL={self.base_url}, Shortcode={self.shortcode}")
        
        if not all([self.consumer_key, self.consumer_secret, self.shortcode, self.passkey]):
            logger.error("M-Pesa credentials missing! Check your settings.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException),
        before_sleep=lambda retry_state: logger.warning(f"Retrying M-Pesa access token request: attempt {retry_state.attempt_number}")
    )
    def get_access_token(self):
        if self.access_token and self.token_expiry and self.token_expiry > datetime.now():
            logger.debug("Using cached M-Pesa access token")
            return self.access_token
            
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {credentials}"}
        
        logger.info(f"Requesting M-Pesa access token from: {url}")
        
        try:
            logger.debug(f"Making request with headers: Authorization: Basic {'*' * len(credentials)}")
            response = requests.get(url, headers=headers, timeout=10)
            
            logger.debug(f"Access token response - Status: {response.status_code}, Response: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get('access_token')
            self.token_expiry = datetime.now() + timedelta(seconds=int(data.get('expires_in', 3600)) - 300)
            logger.info("M-Pesa access token obtained successfully")
            return self.access_token
        except requests.HTTPError as e:
            logger.error(f"Failed to get access token: {e}, Status: {e.response.status_code}, Response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_access_token: {str(e)}")
            raise

    def generate_password(self, timestamp):
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        encoded_pwd = base64.b64encode(data_to_encode.encode()).decode()
        logger.debug(f"Generated password for timestamp {timestamp} (encoded)")
        return encoded_pwd

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException),
        before_sleep=lambda retry_state: logger.warning(f"Retrying STK Push: attempt {retry_state.attempt_number}")
    )
    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        normalized_phone = self._normalize_phone_number(phone_number)
        
        token = self.get_access_token()
        logger.debug(f"Using access token: {token[:5]}...{token[-5:] if token else ''}")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(int(float(amount))),  # Ensure integer amount
            "PartyA": normalized_phone,
            "PartyB": self.shortcode,
            "PhoneNumber": normalized_phone,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        log_payload = dict(payload)
        logger.info(f"Initiating STK Push to URL: {url}")
        logger.debug(f"STK Push payload: {json.dumps(log_payload, indent=2)}")
        logger.debug(f"STK Push headers: {json.dumps({'Authorization': f'Bearer {token[:5]}...{token[-5:]}', 'Content-Type': 'application/json'}, indent=2)}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            logger.debug(f"STK Push response - Status: {response.status_code}, Response: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            logger.info(f"STK Push successful - CheckoutRequestID: {data.get('CheckoutRequestID', 'N/A')}")
            return data
        except requests.HTTPError as e:
            logger.error(f"Failed to initiate STK Push: {e}")
            logger.error(f"Status: {e.response.status_code}, Response: {e.response.text}")
            raise
        except requests.ConnectionError as e:
            logger.error(f"Connection error during STK Push: {str(e)}")
            raise
        except requests.Timeout as e:
            logger.error(f"Timeout during STK Push: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in stk_push: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException),
        before_sleep=lambda retry_state: logger.warning(f"Retrying STK Query: attempt {retry_state.attempt_number}")
    )
    def query_transaction_status(self, checkout_request_id):
        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        logger.info(f"Querying STK Push status: {checkout_request_id}")
        logger.debug(f"Query payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            logger.debug(f"STK Query response - Status: {response.status_code}, Response: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logger.error(f"Failed to query STK Push: {e}, Status: {e.response.status_code}, Response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in query_transaction_status: {str(e)}")
            raise

    def _normalize_phone_number(self, phone_number):
        """Normalize phone number to the correct format for M-Pesa (e.g., 254XXXXXXXXX)."""
        phone = phone_number.strip()
        
        # Remove + if present
        if phone.startswith('+'):
            phone = phone[1:]
            
        # Ensure it starts with 254 for Kenyan numbers
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
            
        logger.debug(f"Normalized phone number from '{phone_number}' to '{phone}'")
        return phone