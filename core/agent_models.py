from django.db import models
from django.utils import timezone
import uuid


class Store(models.Model):
    """Store/Warehouse locations in the supply chain"""
    store_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    store_type = models.CharField(max_length=50, choices=[
        ('store', 'Retail Store'),
        ('warehouse', 'Warehouse'),
        ('fulfillment_center', 'Fulfillment Center'),
        ('distribution_center', 'Distribution Center')
    ])
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.IntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.store_type})"


class Product(models.Model):
    """Product catalog"""
    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_weight = models.FloatField(help_text="Weight in kg")
    shelf_life_days = models.IntegerField(null=True, blank=True)
    minimum_stock_level = models.IntegerField(default=10)
    maximum_stock_level = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class DemandForecast(models.Model):
    """Demand predictions from Inventory Agent (LNN)"""
    forecast_id = models.UUIDField(default=uuid.uuid4, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_demand = models.IntegerField()
    confidence_score = models.FloatField(help_text="0-1 confidence level")
    forecast_horizon_days = models.IntegerField(default=7)
    model_version = models.CharField(max_length=50, default="LNN_v1")
    external_factors = models.JSONField(default=dict, blank=True, help_text="Weather, events, etc.")
    created_by_agent = models.CharField(max_length=100, default="InventoryAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['store', 'product', 'forecast_date']
    
    def __str__(self):
        return f"Forecast: {self.product.name} at {self.store.name} - {self.predicted_demand} units"


class StockRebalanceAction(models.Model):
    """Actions from Rebalancer Agent"""
    action_id = models.UUIDField(default=uuid.uuid4, unique=True)
    source_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='outbound_rebalances')
    target_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inbound_rebalances')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    urgency = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='pending')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by_agent = models.CharField(max_length=100, default="RebalancerAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Rebalance: {self.quantity} {self.product.name} from {self.source_store.name} to {self.target_store.name}"


class RouteOptimization(models.Model):
    """Routes from Route Planner Agent"""
    route_id = models.UUIDField(default=uuid.uuid4, unique=True)
    rebalance_action = models.ForeignKey(StockRebalanceAction, on_delete=models.CASCADE)
    start_location = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='route_starts')
    end_location = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='route_ends')
    waypoints = models.JSONField(default=list, blank=True, help_text="Intermediate stops")
    total_distance_km = models.FloatField()
    estimated_duration_hours = models.FloatField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    traffic_conditions = models.CharField(max_length=50, default="normal")
    route_status = models.CharField(max_length=20, choices=[
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('delayed', 'Delayed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='planned')
    alternative_routes = models.JSONField(default=list, blank=True)
    created_by_agent = models.CharField(max_length=100, default="RoutePlannerAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Route: {self.start_location.name} → {self.end_location.name} ({self.total_distance_km}km)"


class ExternalDisruption(models.Model):
    """Events from Delay Monitor Agent"""
    disruption_id = models.UUIDField(default=uuid.uuid4, unique=True)
    event_type = models.CharField(max_length=50, choices=[
        ('weather', 'Weather'),
        ('traffic', 'Traffic'),
        ('strike', 'Strike'),
        ('accident', 'Accident'),
        ('festival', 'Festival'),
        ('sports_event', 'Sports Event'),
        ('infrastructure', 'Infrastructure'),
        ('other', 'Other')
    ])
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    affected_areas = models.JSONField(default=list, help_text="List of affected locations/routes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    impact_radius_km = models.FloatField(default=5.0)
    affected_routes = models.ManyToManyField(RouteOptimization, blank=True)
    data_source = models.CharField(max_length=100, help_text="API, news, manual, etc.")
    created_by_agent = models.CharField(max_length=100, default="DelayMonitorAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event_type.title()}: {self.title} ({self.severity})"


class VisionInspection(models.Model):
    """Results from Vision Inspector Agent (YOLO)"""
    inspection_id = models.UUIDField(default=uuid.uuid4, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=500, help_text="Path to analyzed image")
    inspection_type = models.CharField(max_length=50, choices=[
        ('shelf_stock', 'Shelf Stock Check'),
        ('spoilage', 'Spoilage Detection'),
        ('placement', 'Product Placement'),
        ('cleanliness', 'Cleanliness Check'),
        ('security', 'Security Check')
    ])
    detected_objects = models.JSONField(default=list, help_text="YOLO detection results")
    anomalies_found = models.JSONField(default=list, help_text="Issues detected")
    confidence_scores = models.JSONField(default=dict, help_text="Detection confidence levels")
    action_required = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    processed_by_model = models.CharField(max_length=100, default="YOLOv8")
    created_by_agent = models.CharField(max_length=100, default="VisionInspectorAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inspection: {self.inspection_type} at {self.store.name}"


class AgentExplanation(models.Model):
    """Natural language explanations from Explainer Agent (GPT-4)"""
    explanation_id = models.UUIDField(default=uuid.uuid4, unique=True)
    query = models.TextField(help_text="Original user question")
    context_data = models.JSONField(default=dict, help_text="Relevant data for explanation")
    explanation_text = models.TextField()
    confidence_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    data_sources = models.JSONField(default=list, help_text="Which agents/data were consulted")
    language_model = models.CharField(max_length=100, default="GPT-4")
    tokens_used = models.IntegerField(null=True, blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    user_feedback = models.CharField(max_length=20, choices=[
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('unclear', 'Unclear')
    ], null=True, blank=True)
    created_by_agent = models.CharField(max_length=100, default="ExplainerAgent")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Explanation: {self.query[:50]}..."


class CortexCoordination(models.Model):
    """Central coordination from Cortex Manager"""
    coordination_id = models.UUIDField(default=uuid.uuid4, unique=True)
    event_type = models.CharField(max_length=50, choices=[
        ('rebalance_triggered', 'Rebalance Triggered'),
        ('route_updated', 'Route Updated'),
        ('disruption_handled', 'Disruption Handled'),
        ('inspection_alert', 'Inspection Alert'),
        ('conflict_resolved', 'Conflict Resolved'),
        ('system_health_check', 'System Health Check')
    ])
    involved_agents = models.JSONField(default=list, help_text="List of agents involved")
    coordination_data = models.JSONField(default=dict, help_text="Coordination context")
    priority = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    status = models.CharField(max_length=20, choices=[
        ('initiated', 'Initiated'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='initiated')
    execution_timeline = models.JSONField(default=list, help_text="Step-by-step execution log")
    created_by_agent = models.CharField(max_length=100, default="CortexManager")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Coordination: {self.event_type} ({self.priority})"


class AgentMetrics(models.Model):
    """Performance metrics for all agents"""
    metric_id = models.UUIDField(default=uuid.uuid4, unique=True)
    agent_name = models.CharField(max_length=100)
    metric_type = models.CharField(max_length=50, choices=[
        ('response_time', 'Response Time'),
        ('accuracy', 'Accuracy'),
        ('throughput', 'Throughput'),
        ('error_rate', 'Error Rate'),
        ('success_rate', 'Success Rate'),
        ('resource_usage', 'Resource Usage')
    ])
    metric_value = models.FloatField()
    unit = models.CharField(max_length=20, help_text="ms, %, count, etc.")
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['agent_name', 'metric_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.agent_name}: {self.metric_type} = {self.metric_value} {self.unit}"
