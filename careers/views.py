from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from .serializers import CareerSerializer, CareerCreateSerializer, CareerUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class CareersView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
        
    BASE_API_URL = settings.CODELEAP_API_URL  # https://api.codeleap.com/careers/

    # GET todos os posts
    def get(self, request):
        response = requests.get(f'{self.BASE_API_URL}')
        
        if response.status_code != 200:
            return Response({"error": "Falha ao obter dados"}, status=response.status_code)

        data = response.json().get("results", [])
        serializer = CareerSerializer(instance=data, many=True)
        return Response(serializer.data)

    # POST novo post
    def post(self, request):
        serializer = CareerCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.post(
                f'{self.BASE_API_URL}',
                json=serializer.validated_data,
                headers=headers
            )
            if response.status_code in (200, 201):
                return Response(response.json(), status=response.status_code)
            return Response({"error": "Falha ao criar post"}, status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH para atualizar parcialmente
    def patch(self, request, id=None):
        serializer = CareerUpdateSerializer(data=request.data, partial=True)
        
        if serializer.is_valid():
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.patch(
                f'{self.BASE_API_URL}{id}/',
                json=serializer.validated_data,
                headers=headers
            )
            if response.status_code == 200:
                return Response(response.json())
            return Response({"error": "Falha ao atualizar post"}, status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE para remover
    def delete(self, request, id=None):
        response = requests.delete(f'{self.BASE_API_URL}{id}/')
        
        if response.status_code in (200, 204):
            return Response({"message": "Post deletado com sucesso"}, status=response.status_code)
        return Response({"error": "Falha ao deletar post"}, status=response.status_code)
