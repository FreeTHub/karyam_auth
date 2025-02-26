import time
import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import KeysDocument
from datetime import datetime
User = get_user_model()
import logging

logger = logging.getLogger("authentication")

class APIGatewayMiddleware:
    logger.info("API Gateway Middleware")
    # auth_logger.info("API Gateway Middleware auth_logger")
    """
    Middleware to validate API Gateway requests.
    Ensures the request contains a valid gateway token, timestamp, and service name.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract API Gateway headers
        logger.info("Request Headers: " + str(request.headers))
        secret_doc = KeysDocument.objects.filter(keyName="auth_server_gateway_signature").first()
        secret_key = secret_doc.valueName
       
       
        logger.info(f"secret_key ===> {secret_key}")
        gateway_token = request.headers.get("jwtGatewayToken")
        logger.info(f"gateway_token ===> {gateway_token}")
        # service_name = request.headers.get("serviceName")
        # timestamp = request.headers.get("expiresDateTimeStamp")
        payload = jwt.decode(gateway_token, secret_key, algorithms=["HS256"])  # Adjust algorithm if needed
        logger.info(f"Decoded JWT Payload: {payload}")


        ## FROM PAYLOAD
        service_name = payload.get("id")
        timestamp = payload.get("expiresDateTimeStamp")
        gateway_token = payload.get("gatewayToken")
        logger.info(f"Service Name: {service_name} | Timestamp: {timestamp} | Gateway Token: {gateway_token}")

        if not service_name or not timestamp or not gateway_token:
            return JsonResponse({"error": "Missing required headers"}, status=400)

        # Convert timestamp to a datetime object
        logger.info(f"Timestamp: {timestamp}")
        request_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        logger.info(f"Request Time: {request_time}")
        current_time = datetime.utcnow()
        logger.info(f"Current Time: {current_time}")
        time_difference = (current_time - request_time).total_seconds()
        logger.info(f"The time difference is: {time_difference}")

        # Validate timestamp (e.g., allow only requests within 1 minutes)
        if abs(time_difference) > 60:  
            return JsonResponse({"error": "Request timestamp expired or too early"}, status=403)
            
        # Validate Gateway Token
        expected_doc = KeysDocument.objects.filter(keyName="gateway_token").first()
        expected_token = expected_doc.valueName
        logger.info(f"Expected Gateway Token: {expected_token}")
        
        if not gateway_token or gateway_token != expected_token:
            return JsonResponse({"error": "Invalid Gateway Token"}, status=403)

        # Validate Service Name
        allowed_services = ["AUTHSERVICE"]
        if service_name not in allowed_services:
            logger.info(f"Service Name: {service_name}")
            return JsonResponse({"error": "Unauthorized service"}, status=403)

        return self.get_response(request)

