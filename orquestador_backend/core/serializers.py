from rest_framework import serializers

class ProcessStartSerializer(serializers.Serializer):
    process_type = serializers.CharField()
    user_id = serializers.CharField()
