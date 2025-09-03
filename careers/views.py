import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from .serializers import CareerSerializer, CareerCreateSerializer, CareerUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Configura logger
logger = logging.getLogger(__name__)

class CareersView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
        
    BASE_API_URL = settings.CODELEAP_API_URL

    # GET todos os posts
    def get(self, request):
        logger.info("GET /careers chamado")
        response = requests.get(f'{self.BASE_API_URL}')
        
        logger.debug(f"Resposta da API externa (status={response.status_code})")
        if response.status_code != 200:
            logger.error(f"Falha ao obter dados: {response.text}")
            return Response({"error": "Falha ao obter dados"}, status=response.status_code)

        data = response.json().get("results", [])
        logger.info(f"Retornando {len(data)} posts")
        serializer = CareerSerializer(instance=data, many=True)
        return Response(serializer.data)

    # POST novo post
    def post(self, request):
        logger.info("POST /careers chamado")
        logger.debug(f"Payload recebido: {request.data}")

        data = request.data.copy()
        data["username"] = request.user.username
        serializer = CareerCreateSerializer(data=data)
        
        if serializer.is_valid():
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            logger.debug(f"Payload validado: {serializer.validated_data}")
            try:
                response = requests.post(
                    f'{self.BASE_API_URL}',
                    json=serializer.validated_data,
                    headers=headers
                )
                logger.debug(f"Resposta da API externa (status={response.status_code}): {response.text}")
            except Exception as e:
                logger.exception("Erro ao chamar API externa no POST")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response.status_code in (200, 201):
                return Response(response.json(), status=response.status_code)
            return Response({"error": "Falha ao criar post"}, status=response.status_code)

        logger.warning(f"Payload inválido: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH para atualizar parcialmente
    def patch(self, request, id=None):
        logger.info(f"PATCH /careers/{id} chamado")
        logger.debug(f"Payload recebido: {request.data}")
        serializer = CareerUpdateSerializer(data=request.data, partial=True)
        
        if serializer.is_valid():
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            logger.debug(f"Payload validado: {serializer.validated_data}")
            try:
                response = requests.patch(
                    f'{self.BASE_API_URL}{id}/',
                    json=serializer.validated_data,
                    headers=headers
                )
                logger.debug(f"Resposta da API externa (status={response.status_code}): {response.text}")
            except Exception as e:
                logger.exception("Erro ao chamar API externa no PATCH")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response.status_code == 200:
                return Response(response.json())
            return Response({"error": "Falha ao atualizar post"}, status=response.status_code)

        logger.warning(f"Payload inválido: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE para remover
    def delete(self, request, id=None):
        logger.info(f"DELETE /careers/{id} chamado")
        try:
            response = requests.delete(f'{self.BASE_API_URL}{id}/')
            logger.debug(f"Resposta da API externa (status={response.status_code}): {response.text}")
        except Exception as e:
            logger.exception("Erro ao chamar API externa no DELETE")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response.status_code in (200, 204):
            return Response({"message": "Post deletado com sucesso"}, status=response.status_code)
        return Response({"error": "Falha ao deletar post"}, status=response.status_code)