from rest_framework import serializers
from .agent_models import (
    Store, Product, DemandForecast, StockRebalanceAction, 
    RouteOptimization, ExternalDisruption, VisionInspection,
    AgentExplanation, CortexCoordination, AgentMetrics
)


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model"""
    class Meta:
        model = Store
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""
    class Meta:
        model = Product
        fields = '__all__'


class DemandForecastSerializer(serializers.ModelSerializer):
    """Serializer for demand forecasts from Inventory Agent"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = DemandForecast
        fields = '__all__'


class StockRebalanceActionSerializer(serializers.ModelSerializer):
    """Serializer for rebalance actions"""
    source_store_name = serializers.CharField(source='source_store.name', read_only=True)
    target_store_name = serializers.CharField(source='target_store.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = StockRebalanceAction
        fields = '__all__'


class RouteOptimizationSerializer(serializers.ModelSerializer):
    """Serializer for route optimization"""
    start_location_name = serializers.CharField(source='start_location.name', read_only=True)
    end_location_name = serializers.CharField(source='end_location.name', read_only=True)
    rebalance_details = StockRebalanceActionSerializer(source='rebalance_action', read_only=True)
    
    class Meta:
        model = RouteOptimization
        fields = '__all__'


class ExternalDisruptionSerializer(serializers.ModelSerializer):
    """Serializer for external disruptions"""
    affected_routes_count = serializers.IntegerField(source='affected_routes.count', read_only=True)
    
    class Meta:
        model = ExternalDisruption
        fields = '__all__'


class VisionInspectionSerializer(serializers.ModelSerializer):
    """Serializer for vision inspections"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = VisionInspection
        fields = '__all__'


class AgentExplanationSerializer(serializers.ModelSerializer):
    """Serializer for agent explanations"""
    query_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentExplanation
        fields = '__all__'
    
    def get_query_preview(self, obj):
        return obj.query[:100] + "..." if len(obj.query) > 100 else obj.query


class CortexCoordinationSerializer(serializers.ModelSerializer):
    """Serializer for cortex coordination"""
    duration_seconds = serializers.SerializerMethodField()
    
    class Meta:
        model = CortexCoordination
        fields = '__all__'
    
    def get_duration_seconds(self, obj):
        if obj.completed_at and obj.created_at:
            return (obj.completed_at - obj.created_at).total_seconds()
        return None


class AgentMetricsSerializer(serializers.ModelSerializer):
    """Serializer for agent metrics"""
    class Meta:
        model = AgentMetrics
        fields = '__all__'


# Dashboard summary serializers
class DashboardSummarySerializer(serializers.Serializer):
    """Summary data for the main dashboard"""
    total_stores = serializers.IntegerField()
    total_products = serializers.IntegerField()
    active_rebalances = serializers.IntegerField()
    pending_inspections = serializers.IntegerField()
    current_disruptions = serializers.IntegerField()
    recent_explanations = serializers.IntegerField()
    
    # Agent health metrics
    agent_status = serializers.DictField()
    
    # Recent activity
    recent_forecasts = DemandForecastSerializer(many=True)
    active_routes = RouteOptimizationSerializer(many=True)
    critical_alerts = serializers.ListField()


class AgentHealthSerializer(serializers.Serializer):
    """Health status of all agents"""
    agent_name = serializers.CharField()
    status = serializers.CharField()  # healthy, warning, error, offline
    last_activity = serializers.DateTimeField()
    response_time_avg = serializers.FloatField()
    success_rate = serializers.FloatField()
    error_count_24h = serializers.IntegerField()
