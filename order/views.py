import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .getniubiz import get_niubiz_token

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            token = get_niubiz_token()

            url = 'https://apisandbox.vnforappstest.com/api.authorization/v3/authorization/ecommerce/integraciones@niubiz.com.pe'
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            data = {
                "channel": "web",
                "amount": paid_amount,
                "antifraud": {
                    "clientIp": "127.0.0.1",
                    "merchantDefineData": {
                        "MDD4": "DNI",
                        "MDD21": "web"
                    }
                }
            }
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                serializer.save(user=request.user, paid_amount=paid_amount)
                # Suponiendo que la respuesta contiene una URL de redirección
                return Response({'redirect_url': response_data.get('redirectUrl')}, status=status.HTTP_201_CREATED)
            else:
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
