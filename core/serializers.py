from rest_framework import serializers
from .models import Inventory, TransferLog, DeliveryRoute, AgentLog
from drf_spectacular.utils import extend_schema_field


class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for Inventory model.
    Handles product inventory data including quantities and expiry dates.
    """
    product_id = serializers.CharField(
        max_length=100,
        help_text="Unique identifier for the product"
    )
    product_name = serializers.CharField(
        max_length=255,
        help_text="Name of the product"
    )
    store_location = serializers.CharField(
        max_length=255,
        help_text="Store location where the product is stored"
    )
    quantity = serializers.IntegerField(
        min_value=0,
        help_text="Current quantity in stock"
    )
    expiry_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Product expiry date (optional)"
    )
    last_updated = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when the inventory was last updated"
    )

    class Meta:
        model = Inventory
        fields = '__all__'


class TransferLogSerializer(serializers.ModelSerializer):
    """
    Serializer for TransferLog model.
    Tracks product transfers between stores.
    """
    from_store = serializers.CharField(
        max_length=255,
        help_text="Source store location"
    )
    to_store = serializers.CharField(
        max_length=255,
        help_text="Destination store location"
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Inventory.objects.all(),
        help_text="Product being transferred"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Quantity being transferred"
    )
    timestamp = serializers.DateTimeField(
        read_only=True,
        help_text="When the transfer was logged"
    )
    reason = serializers.CharField(
        help_text="Reason for the transfer"
    )

    class Meta:
        model = TransferLog
        fields = '__all__'


class DeliveryRouteSerializer(serializers.ModelSerializer):
    """
    Serializer for DeliveryRoute model.
    Manages delivery route information and tracking.
    """
    route_id = serializers.CharField(
        max_length=100,
        help_text="Unique identifier for the delivery route"
    )
    start_point = serializers.CharField(
        max_length=255,
        help_text="Starting location of the delivery"
    )
    end_point = serializers.CharField(
        max_length=255,
        help_text="Destination location of the delivery"
    )
    eta = serializers.DateTimeField(
        help_text="Estimated time of arrival"
    )
    status = serializers.ChoiceField(
        choices=[
            ('scheduled', 'Scheduled'),
            ('delayed', 'Delayed'),
            ('delivered', 'Delivered')
        ],
        help_text="Current status of the delivery"
    )
    disruption_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Notes about any disruptions or delays"
    )

    class Meta:
        model = DeliveryRoute
        fields = '__all__'


class AgentLogSerializer(serializers.ModelSerializer):
    """
    Serializer for AgentLog model.
    Records actions performed by automated agents.
    """
    agent_name = serializers.CharField(
        max_length=255,
        help_text="Name of the agent that performed the action"
    )
    action = serializers.CharField(
        help_text="Description of the action performed"
    )
    timestamp = serializers.DateTimeField(
        read_only=True,
        help_text="When the action was performed"
    )

    class Meta:
        model = AgentLog
        fields = '__all__'
