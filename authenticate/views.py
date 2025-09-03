import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        logger.info("POST /token/ chamado")
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            logger.debug(f"Tokens obtidos: {tokens.keys()}")

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            res = Response({'success': True})

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            logger.info(f"Cookies setados para usuário: {request.data.get('username')}")
            return res
        except Exception as e:
            logger.exception("Erro ao gerar tokens")
            return Response({'success': False}, status=500)


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        logger.info("POST /token/refresh chamado")
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                logger.warning("Refresh token não encontrado nos cookies")
                return Response({'refreshed': False}, status=401)

            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            res = Response({'refreshed': True})
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            logger.info("Access token atualizado com sucesso")
            return res
        except Exception as e:
            logger.exception("Erro ao atualizar token")
            return Response({'refreshed': False}, status=500)


class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Verificação de autenticação para usuário: {request.user.username}")
        return Response({'authenticated': True})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("POST /auth/register chamado")
        logger.debug(f"Payload recebido: {request.data}")

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"Usuário criado com sucesso: {user.username}")
                return Response(serializer.data, status=201)
            except Exception as e:
                logger.exception("Erro ao salvar usuário")
                return Response({'error': str(e)}, status=500)

        logger.warning(f"Payload inválido: {serializer.errors}")
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Logout chamado para usuário: {request.user.username}")
        try:
            res = Response({'success': True})
            res.delete_cookie('access_token', path='/', samesite='None')
            res.delete_cookie('refresh_token', path='/', samesite='None')
            logger.info("Cookies removidos com sucesso")
            return res
        except Exception as e:
            logger.exception("Erro ao remover cookies")
            return Response({'success': False}, status=500)
