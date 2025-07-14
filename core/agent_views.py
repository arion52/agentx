from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Q
import json
import uuid

from .agent_models import (
    Store, Product, DemandForecast, StockRebalanceAction,
    RouteOptimization, ExternalDisruption, VisionInspection,
    AgentExplanation, CortexCoordination, AgentMetrics
)
from .agent_serializers import (
    StoreSerializer, ProductSerializer, DemandForecastSerializer,
    StockRebalanceActionSerializer, RouteOptimizationSerializer,
    ExternalDisruptionSerializer, VisionInspectionSerializer,
    AgentExplanationSerializer, CortexCoordinationSerializer,
    AgentMetricsSerializer, DashboardSummarySerializer, AgentHealthSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="List all stores",
        description="Retrieve all stores and warehouses in the supply chain network",
        responses={200: StoreSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create new store",
        description="Add a new store or warehouse to the network",
        responses={201: StoreSerializer}
    )
)
class StoreViewSet(viewsets.ModelViewSet):
    """Manage stores and warehouses in the supply chain"""
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @extend_schema(
        summary="Get stores by type",
        description="Filter stores by type (store, warehouse, fulfillment_center, distribution_center)",
        parameters=[
            OpenApiParameter(
                name='store_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Type of store to filter by'
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        store_type = request.query_params.get('store_type')
        if store_type:
            stores = self.queryset.filter(store_type=store_type)
        else:
            stores = self.queryset.all()
        serializer = self.get_serializer(stores, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve all products in the catalog",
        responses={200: ProductSerializer(many=True)}
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    """Manage product catalog"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List demand forecasts",
        description="Retrieve demand predictions from the Inventory Agent (LNN)",
        responses={200: DemandForecastSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create demand forecast",
        description="Add a new demand prediction (typically from LNN model)",
        responses={201: DemandForecastSerializer}
    )
)
class DemandForecastViewSet(viewsets.ModelViewSet):
    """Manage demand forecasts from Inventory Agent"""
    queryset = DemandForecast.objects.all()
    serializer_class = DemandForecastSerializer

    @extend_schema(
        summary="Get recent forecasts",
        description="Get forecasts created in the last N days",
        parameters=[
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of days to look back (default: 7)',
                default=7
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def recent(self, request):
        days = int(request.query_params.get('days', 7))
        cutoff_date = timezone.now() - timedelta(days=days)
        forecasts = self.queryset.filter(created_at__gte=cutoff_date)
        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get high confidence forecasts",
        description="Get forecasts with confidence above threshold",
        parameters=[
            OpenApiParameter(
                name='confidence',
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description='Minimum confidence level (0-1, default: 0.8)',
                default=0.8
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def high_confidence(self, request):
        confidence = float(request.query_params.get('confidence', 0.8))
        forecasts = self.queryset.filter(confidence_score__gte=confidence)
        serializer = self.get_serializer(forecasts, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List rebalance actions",
        description="Retrieve stock rebalance actions from the Rebalancer Agent",
        responses={200: StockRebalanceActionSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create rebalance action",
        description="Create a new stock rebalance action",
        responses={201: StockRebalanceActionSerializer}
    )
)
class StockRebalanceActionViewSet(viewsets.ModelViewSet):
    """Manage stock rebalance actions from Rebalancer Agent"""
    queryset = StockRebalanceAction.objects.all()
    serializer_class = StockRebalanceActionSerializer

    @extend_schema(
        summary="Get pending actions",
        description="Get rebalance actions that are pending approval or execution"
    )
    @action(detail=False, methods=['get'])
    def pending(self, request):
        actions = self.queryset.filter(status__in=['pending', 'approved'])
        serializer = self.get_serializer(actions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get critical actions",
        description="Get high-priority rebalance actions"
    )
    @action(detail=False, methods=['get'])
    def critical(self, request):
        actions = self.queryset.filter(urgency__in=['high', 'critical'])
        serializer = self.get_serializer(actions, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List route optimizations",
        description="Retrieve optimized routes from the Route Planner Agent",
        responses={200: RouteOptimizationSerializer(many=True)}
    )
)
class RouteOptimizationViewSet(viewsets.ModelViewSet):
    """Manage route optimizations from Route Planner Agent"""
    queryset = RouteOptimization.objects.all()
    serializer_class = RouteOptimizationSerializer

    @extend_schema(
        summary="Get active routes",
        description="Get routes that are currently active or planned"
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        routes = self.queryset.filter(route_status__in=['planned', 'active'])
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get delayed routes",
        description="Get routes that are currently delayed"
    )
    @action(detail=False, methods=['get'])
    def delayed(self, request):
        routes = self.queryset.filter(route_status='delayed')
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List external disruptions",
        description="Retrieve disruptions detected by the Delay Monitor Agent",
        responses={200: ExternalDisruptionSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create disruption alert",
        description="Log a new external disruption (weather, traffic, etc.)",
        responses={201: ExternalDisruptionSerializer}
    )
)
class ExternalDisruptionViewSet(viewsets.ModelViewSet):
    """Manage external disruptions from Delay Monitor Agent"""
    queryset = ExternalDisruption.objects.all()
    serializer_class = ExternalDisruptionSerializer

    @extend_schema(
        summary="Get active disruptions",
        description="Get disruptions that are currently active"
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        now = timezone.now()
        disruptions = self.queryset.filter(
            start_time__lte=now
        ).filter(
            Q(end_time__gte=now) | Q(end_time__isnull=True)
        )
        serializer = self.get_serializer(disruptions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get critical disruptions",
        description="Get high-severity disruptions"
    )
    @action(detail=False, methods=['get'])
    def critical(self, request):
        disruptions = self.queryset.filter(severity__in=['high', 'critical'])
        serializer = self.get_serializer(disruptions, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List vision inspections",
        description="Retrieve inspection results from the Vision Inspector Agent (YOLO)",
        responses={200: VisionInspectionSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create vision inspection",
        description="Log results from a YOLO-based store inspection",
        responses={201: VisionInspectionSerializer}
    )
)
class VisionInspectionViewSet(viewsets.ModelViewSet):
    """Manage vision inspections from Vision Inspector Agent"""
    queryset = VisionInspection.objects.all()
    serializer_class = VisionInspectionSerializer

    @extend_schema(
        summary="Get inspections requiring action",
        description="Get inspections that flagged issues requiring attention"
    )
    @action(detail=False, methods=['get'])
    def action_required(self, request):
        inspections = self.queryset.filter(action_required=True)
        serializer = self.get_serializer(inspections, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get urgent inspections",
        description="Get high-priority inspection alerts"
    )
    @action(detail=False, methods=['get'])
    def urgent(self, request):
        inspections = self.queryset.filter(priority='urgent')
        serializer = self.get_serializer(inspections, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List agent explanations",
        description="Retrieve explanations from the Explainer Agent (GPT-4)",
        responses={200: AgentExplanationSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Request explanation",
        description="Request a natural language explanation from GPT-4",
        responses={201: AgentExplanationSerializer}
    )
)
class AgentExplanationViewSet(viewsets.ModelViewSet):
    """Manage explanations from Explainer Agent"""
    queryset = AgentExplanation.objects.all()
    serializer_class = AgentExplanationSerializer

    @extend_schema(
        summary="Get recent explanations",
        description="Get explanations from the last N hours",
        parameters=[
            OpenApiParameter(
                name='hours',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Hours to look back (default: 24)',
                default=24
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def recent(self, request):
        hours = int(request.query_params.get('hours', 24))
        cutoff_time = timezone.now() - timedelta(hours=hours)
        explanations = self.queryset.filter(created_at__gte=cutoff_time)
        serializer = self.get_serializer(explanations, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List cortex coordinations",
        description="Retrieve coordination events from the Cortex Manager",
        responses={200: CortexCoordinationSerializer(many=True)}
    )
)
class CortexCoordinationViewSet(viewsets.ModelViewSet):
    """Manage coordination events from Cortex Manager"""
    queryset = CortexCoordination.objects.all()
    serializer_class = CortexCoordinationSerializer

    @extend_schema(
        summary="Get active coordinations",
        description="Get coordination events that are in progress"
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        coordinations = self.queryset.filter(status='in_progress')
        serializer = self.get_serializer(coordinations, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List agent metrics",
        description="Retrieve performance metrics for all agents",
        responses={200: AgentMetricsSerializer(many=True)}
    )
)
class AgentMetricsViewSet(viewsets.ModelViewSet):
    """Manage agent performance metrics"""
    queryset = AgentMetrics.objects.all()
    serializer_class = AgentMetricsSerializer

    @extend_schema(
        summary="Get metrics by agent",
        description="Get metrics for a specific agent",
        parameters=[
            OpenApiParameter(
                name='agent_name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Name of the agent'
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def by_agent(self, request):
        agent_name = request.query_params.get('agent_name')
        if agent_name:
            metrics = self.queryset.filter(agent_name=agent_name)
        else:
            metrics = self.queryset.all()
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)


# Dashboard and system-wide endpoints

@extend_schema(
    summary="Get dashboard summary",
    description="Get comprehensive dashboard data for the AgentX++ system",
    responses={200: DashboardSummarySerializer}
)
@api_view(['GET'])
def dashboard_summary(request):
    """Get comprehensive dashboard summary"""
    
    # Calculate summary statistics
    total_stores = Store.objects.count()
    total_products = Product.objects.count()
    active_rebalances = StockRebalanceAction.objects.filter(
        status__in=['pending', 'approved', 'in_progress']
    ).count()
    pending_inspections = VisionInspection.objects.filter(
        action_required=True
    ).count()
    current_disruptions = ExternalDisruption.objects.filter(
        start_time__lte=timezone.now()
    ).filter(
        Q(end_time__gte=timezone.now()) | Q(end_time__isnull=True)
    ).count()
    recent_explanations = AgentExplanation.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).count()
    
    # Agent health status (simplified for demo)
    agent_status = {
        'InventoryAgent': 'healthy',
        'RebalancerAgent': 'healthy', 
        'RoutePlannerAgent': 'healthy',
        'DelayMonitorAgent': 'warning',
        'VisionInspectorAgent': 'healthy',
        'ExplainerAgent': 'healthy',
        'CortexManager': 'healthy'
    }
    
    # Recent activity
    recent_forecasts = DemandForecast.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    )[:5]
    
    active_routes = RouteOptimization.objects.filter(
        route_status__in=['planned', 'active']
    )[:5]
    
    critical_alerts = [
        "Low stock alert: Milk at Whitefield store",
        "Route delay: KR Puram to BTM Layout +30min due to traffic",
        "Vision alert: Spoilage detected at Indiranagar store"
    ]
    
    summary_data = {
        'total_stores': total_stores,
        'total_products': total_products,
        'active_rebalances': active_rebalances,
        'pending_inspections': pending_inspections,
        'current_disruptions': current_disruptions,
        'recent_explanations': recent_explanations,
        'agent_status': agent_status,
        'recent_forecasts': DemandForecastSerializer(recent_forecasts, many=True).data,
        'active_routes': RouteOptimizationSerializer(active_routes, many=True).data,
        'critical_alerts': critical_alerts
    }
    
    return Response(summary_data)


@extend_schema(
    summary="Get agent health status",
    description="Get health and performance status of all AI agents",
    responses={200: AgentHealthSerializer(many=True)}
)
@api_view(['GET'])
def agent_health(request):
    """Get health status of all AI agents"""
    
    # This would typically query real metrics, but for demo we'll use mock data
    agent_health_data = [
        {
            'agent_name': 'InventoryAgent',
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(minutes=5),
            'response_time_avg': 245.5,
            'success_rate': 99.2,
            'error_count_24h': 1
        },
        {
            'agent_name': 'RebalancerAgent', 
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(minutes=12),
            'response_time_avg': 1205.8,
            'success_rate': 98.8,
            'error_count_24h': 2
        },
        {
            'agent_name': 'RoutePlannerAgent',
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(minutes=8),
            'response_time_avg': 892.3,
            'success_rate': 99.1,
            'error_count_24h': 0
        },
        {
            'agent_name': 'DelayMonitorAgent',
            'status': 'warning',
            'last_activity': timezone.now() - timedelta(minutes=45),
            'response_time_avg': 3405.2,
            'success_rate': 95.5,
            'error_count_24h': 8
        },
        {
            'agent_name': 'VisionInspectorAgent',
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(minutes=2),
            'response_time_avg': 1825.1,
            'success_rate': 97.8,
            'error_count_24h': 3
        },
        {
            'agent_name': 'ExplainerAgent',
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(minutes=15),
            'response_time_avg': 2150.7,
            'success_rate': 99.5,
            'error_count_24h': 1
        },
        {
            'agent_name': 'CortexManager',
            'status': 'healthy',
            'last_activity': timezone.now() - timedelta(seconds=30),
            'response_time_avg': 125.3,
            'success_rate': 99.9,
            'error_count_24h': 0
        }
    ]
    
    return Response(agent_health_data)


@extend_schema(
    summary="Simulate agent activity",
    description="Trigger a complex multi-agent workflow simulation",
    methods=['POST'],
    responses={200: OpenApiResponse(description="Simulation completed")}
)
@api_view(['POST'])
def simulate_agent_workflow(request):
    """Simulate a complex multi-agent workflow"""
    
    # This simulates the kind of complex workflow described in the hackathon plan
    simulation_log = []
    
    # 1. Inventory Agent detects low stock
    try:
        # Create a mock forecast showing low demand
        forecast = DemandForecast.objects.create(
            store=Store.objects.first(),
            product=Product.objects.first(),
            forecast_date=timezone.now().date(),
            predicted_demand=5,
            confidence_score=0.92,
            external_factors={'weather': 'heavy_rain', 'event': 'cricket_match'},
            created_by_agent='InventoryAgent'
        )
        simulation_log.append("✅ InventoryAgent: Created demand forecast")
        
        # 2. Rebalancer Agent creates action
        rebalance = StockRebalanceAction.objects.create(
            source_store=Store.objects.filter(store_type='warehouse').first(),
            target_store=Store.objects.filter(store_type='store').first(),
            product=Product.objects.first(),
            quantity=25,
            urgency='high',
            reason='Low stock detected by InventoryAgent forecast',
            created_by_agent='RebalancerAgent'
        )
        simulation_log.append("✅ RebalancerAgent: Created rebalance action")
        
        # 3. Route Planner creates optimized route
        route = RouteOptimization.objects.create(
            rebalance_action=rebalance,
            start_location=rebalance.source_store,
            end_location=rebalance.target_store,
            total_distance_km=15.7,
            estimated_duration_hours=1.2,
            estimated_cost=450.00,
            created_by_agent='RoutePlannerAgent'
        )
        simulation_log.append("✅ RoutePlannerAgent: Created optimized route")
        
        # 4. Delay Monitor detects disruption
        disruption = ExternalDisruption.objects.create(
            event_type='traffic',
            title='Heavy traffic on Hosur Road',
            description='Accident causing 30min delays',
            severity='medium',
            affected_areas=['Hosur Road', 'Electronic City'],
            start_time=timezone.now(),
            created_by_agent='DelayMonitorAgent'
        )
        disruption.affected_routes.add(route)
        simulation_log.append("✅ DelayMonitorAgent: Detected traffic disruption")
        
        # 5. Vision Inspector flags an issue
        inspection = VisionInspection.objects.create(
            store=rebalance.target_store,
            image_path='/inspections/store_shelf_001.jpg',
            inspection_type='shelf_stock',
            detected_objects=[
                {'object': 'empty_shelf', 'confidence': 0.95, 'bbox': [100, 200, 300, 400]},
                {'object': 'product_box', 'confidence': 0.88, 'bbox': [50, 150, 150, 250]}
            ],
            anomalies_found=['empty_shelf_section', 'misplaced_products'],
            action_required=True,
            priority='high',
            created_by_agent='VisionInspectorAgent'
        )
        simulation_log.append("✅ VisionInspectorAgent: Detected shelf issues")
        
        # 6. Cortex Manager coordinates response
        coordination = CortexCoordination.objects.create(
            event_type='disruption_handled',
            involved_agents=['RebalancerAgent', 'RoutePlannerAgent', 'DelayMonitorAgent'],
            coordination_data={
                'original_route_id': str(route.route_id),
                'disruption_id': str(disruption.disruption_id),
                'action_taken': 'route_updated'
            },
            priority='medium',
            status='completed',
            execution_timeline=[
                {'step': 1, 'action': 'Detected disruption', 'timestamp': timezone.now().isoformat()},
                {'step': 2, 'action': 'Notified RoutePlanner', 'timestamp': timezone.now().isoformat()},
                {'step': 3, 'action': 'Updated route ETA', 'timestamp': timezone.now().isoformat()}
            ],
            created_by_agent='CortexManager',
            completed_at=timezone.now()
        )
        simulation_log.append("✅ CortexManager: Coordinated multi-agent response")
        
        # 7. Explainer Agent creates explanation
        explanation = AgentExplanation.objects.create(
            query="Why was today's delivery delayed and what actions were taken?",
            context_data={
                'rebalance_id': str(rebalance.action_id),
                'route_id': str(route.route_id),
                'disruption_id': str(disruption.disruption_id)
            },
            explanation_text=f"""Today's delivery was delayed due to heavy traffic on Hosur Road caused by an accident. 
            The system automatically detected this disruption and took the following actions:
            
            1. The InventoryAgent predicted high demand and low stock at {rebalance.target_store.name}
            2. The RebalancerAgent scheduled a transfer of {rebalance.quantity} units from {rebalance.source_store.name}
            3. The RoutePlannerAgent optimized a 15.7km route with 1.2 hour estimated duration
            4. The DelayMonitorAgent detected traffic disruptions and updated the ETA
            5. The VisionInspectorAgent identified shelf issues requiring attention
            6. The CortexManager coordinated all agents to ensure smooth operations
            
            The delivery will now arrive approximately 30 minutes later than originally scheduled, but stock levels will be maintained.""",
            confidence_level='high',
            data_sources=['DelayMonitorAgent', 'RoutePlannerAgent', 'RebalancerAgent'],
            created_by_agent='ExplainerAgent'
        )
        simulation_log.append("✅ ExplainerAgent: Generated comprehensive explanation")
        
        return Response({
            'status': 'success',
            'message': 'Multi-agent workflow simulation completed successfully',
            'simulation_log': simulation_log,
            'coordination_id': str(coordination.coordination_id),
            'explanation': explanation.explanation_text,
            'affected_entities': {
                'forecast_id': str(forecast.forecast_id),
                'rebalance_id': str(rebalance.action_id),
                'route_id': str(route.route_id),
                'disruption_id': str(disruption.disruption_id),
                'inspection_id': str(inspection.inspection_id)
            }
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Simulation failed: {str(e)}',
            'simulation_log': simulation_log
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
