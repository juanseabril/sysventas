from rest_framework.viewsets import ModelViewSet
from .models import Cliente, Producto, Venta, DetalleVenta
from .serializers import ClienteSerializer, ProductoSerializer, VentaSerializer, DetalleVentaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

@api_view(['POST'])
def register_user(request):
    """
    Endpoint para registrar nuevos usuarios.
    """
    data = request.data

    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response({"error": f"Faltan los campos: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=data['username']).exists():
        return Response({"error": "El nombre de usuario ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email y contraseña son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Credenciales incorrectas.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

    
class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.all().order_by('fecha')
    serializer_class = VentaSerializer


class DetalleVentaViewSet(ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
