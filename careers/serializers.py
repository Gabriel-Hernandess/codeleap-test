from rest_framework import serializers

# GET
class CareerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    created_datetime = serializers.DateTimeField()
    title = serializers.CharField()
    content = serializers.CharField()


# POST
class CareerCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()


# PATCH
class CareerUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()