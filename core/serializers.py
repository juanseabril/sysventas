from rest_framework import serializers
from .models import Cliente, Producto, Venta, DetalleVenta

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'valor_producto', 'iva_calculado', 'cantidad']

    def create(self, validated_data):
        venta = validated_data.get('venta')
        if not venta:
            raise serializers.ValidationError("El campo 'venta' es requerido.")
        return super().create(validated_data)


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')          
        consecutivo = f"{Venta.objects.count() + 1}" 
        venta = Venta.objects.create(consecutivo=consecutivo, **validated_data)
        for detalle_data in detalles_data:
            detalle_data['venta'] = venta
            DetalleVenta.objects.create(**detalle_data)

        return venta




