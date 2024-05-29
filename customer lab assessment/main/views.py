from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id', None)
        if account_id is not None:
            return self.queryset.filter(account__account_id=account_id)
        return self.queryset

@api_view(['POST'])
def handle_incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"error": "Unauthenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    if request.content_type != 'application/json':
        return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    destinations = account.destinations.all()
    
    for destination in destinations:
        headers = destination.headers
        method = destination.http_method
        url = destination.url
        
        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method in ['POST', 'PUT']:
            response = requests.request(method, url, headers=headers, json=data)
        
        if not response.ok:
            return Response({"error": f"Failed to send data to {url}"}, status=response.status_code)

    return Response({"status": "Data sent to all destinations successfully"})
