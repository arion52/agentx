"""
Background tasks for AI agents
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import json
import random
from .agent_models import (
    Store, Product, DemandForecast, StockRebalanceAction,
    RouteOptimization, ExternalDisruption, VisionInspection,
    AgentExplanation, CortexCoordination, AgentMetrics
)


@shared_task
def inventory_agent_forecast_task(store_id, product_id):
    """
    Simulate LNN-based demand forecasting
    In real implementation, this would run the actual LNN model
    """
    try:
        store = Store.objects.get(id=store_id)
        product = Product.objects.get(id=product_id)
        
        # Mock LNN prediction with some realistic variation
        base_demand = random.randint(10, 100)
        confidence = random.uniform(0.75, 0.95)
        
        # Simulate external factors affecting demand
        external_factors = {}
        if random.random() > 0.7:  # 30% chance of external factors
            external_factors = {
                'weather': random.choice(['sunny', 'rainy', 'cloudy']),
                'event': random.choice(['cricket_match', 'festival', 'normal']),
                'traffic': random.choice(['light', 'medium', 'heavy'])
            }
            if external_factors['event'] == 'cricket_match':
                base_demand = int(base_demand * 1.5)  # Higher demand during matches
        
        forecast = DemandForecast.objects.create(
            store=store,
            product=product,
            forecast_date=timezone.now().date(),
            predicted_demand=base_demand,
            confidence_score=confidence,
            external_factors=external_factors,
            created_by_agent='InventoryAgent'
        )
        
        # Log agent metrics
        AgentMetrics.objects.create(
            agent_name='InventoryAgent',
            metric_type='response_time',
            metric_value=random.uniform(200, 500),
            unit='ms'
        )
        
        return {
            'status': 'success',
            'forecast_id': str(forecast.forecast_id),
            'predicted_demand': base_demand,
            'confidence': confidence
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task 
def rebalancer_agent_task():
    """
    Analyze inventory and create rebalance actions
    """
    try:
        # Find stores with potential rebalancing needs
        # This is simplified - real implementation would use complex algorithms
        
        actions_created = 0
        
        # Check recent forecasts for low stock predictions
        recent_forecasts = DemandForecast.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24),
            predicted_demand__gte=50  # High demand threshold
        )
        
        for forecast in recent_forecasts:
            # Check if rebalance already exists
            existing = StockRebalanceAction.objects.filter(
                target_store=forecast.store,
                product=forecast.product,
                status__in=['pending', 'approved', 'in_progress']
            ).exists()
            
            if not existing:
                # Find source store (simplified logic)
                source_stores = Store.objects.filter(
                    store_type__in=['warehouse', 'fulfillment_center']
                ).exclude(id=forecast.store.id)
                
                if source_stores.exists():
                    source_store = source_stores.first()
                    
                    rebalance = StockRebalanceAction.objects.create(
                        source_store=source_store,
                        target_store=forecast.store,
                        product=forecast.product,
                        quantity=max(20, forecast.predicted_demand),
                        urgency='medium',
                        reason=f'High demand forecast: {forecast.predicted_demand} units predicted',
                        created_by_agent='RebalancerAgent'
                    )
                    actions_created += 1
        
        # Log metrics
        AgentMetrics.objects.create(
            agent_name='RebalancerAgent',
            metric_type='throughput',
            metric_value=actions_created,
            unit='actions'
        )
        
        return {
            'status': 'success',
            'actions_created': actions_created
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def route_planner_agent_task(rebalance_action_id):
    """
    Create optimized routes for rebalance actions
    """
    try:
        rebalance = StockRebalanceAction.objects.get(id=rebalance_action_id)
        
        # Mock route optimization (real implementation would use routing algorithms)
        distance = random.uniform(5.0, 50.0)
        duration = distance / 30.0  # Assume 30 km/h average speed
        cost = distance * 15.0  # Cost per km
        
        # Add some traffic variability
        traffic_factor = random.uniform(1.0, 1.5)
        duration *= traffic_factor
        
        route = RouteOptimization.objects.create(
            rebalance_action=rebalance,
            start_location=rebalance.source_store,
            end_location=rebalance.target_store,
            total_distance_km=round(distance, 1),
            estimated_duration_hours=round(duration, 1),
            estimated_cost=round(cost, 2),
            traffic_conditions=random.choice(['light', 'medium', 'heavy']),
            created_by_agent='RoutePlannerAgent'
        )
        
        # Update rebalance action status
        rebalance.status = 'approved'
        rebalance.save()
        
        AgentMetrics.objects.create(
            agent_name='RoutePlannerAgent',
            metric_type='response_time',
            metric_value=random.uniform(800, 1500),
            unit='ms'
        )
        
        return {
            'status': 'success',
            'route_id': str(route.route_id),
            'distance_km': route.total_distance_km,
            'duration_hours': route.estimated_duration_hours
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def delay_monitor_agent_task():
    """
    Monitor for external disruptions
    """
    try:
        disruptions_found = 0
        
        # Simulate finding disruptions (real implementation would use APIs)
        if random.random() > 0.8:  # 20% chance of finding a disruption
            event_types = ['weather', 'traffic', 'strike', 'festival', 'sports_event']
            event_type = random.choice(event_types)
            
            disruption_data = {
                'weather': {
                    'title': 'Heavy rainfall expected',
                    'description': 'IMD predicts heavy rainfall in Bangalore',
                    'severity': 'medium'
                },
                'traffic': {
                    'title': 'Accident on Outer Ring Road',
                    'description': 'Multi-vehicle accident causing delays',
                    'severity': 'high'
                },
                'strike': {
                    'title': 'Transport workers strike',
                    'description': 'City bus drivers on strike',
                    'severity': 'high'
                },
                'festival': {
                    'title': 'Ganesh Chaturthi celebrations',
                    'description': 'Festival processions affecting traffic',
                    'severity': 'medium'
                },
                'sports_event': {
                    'title': 'India vs Pakistan cricket match',
                    'description': 'High viewership expected to affect demand',
                    'severity': 'low'
                }
            }
            
            event_info = disruption_data[event_type]
            
            disruption = ExternalDisruption.objects.create(
                event_type=event_type,
                title=event_info['title'],
                description=event_info['description'],
                severity=event_info['severity'],
                affected_areas=['Bangalore', 'Whitefield', 'Electronic City'],
                start_time=timezone.now(),
                end_time=timezone.now() + timedelta(hours=random.randint(2, 12)),
                data_source='MockAPI',
                created_by_agent='DelayMonitorAgent'
            )
            
            disruptions_found = 1
        
        AgentMetrics.objects.create(
            agent_name='DelayMonitorAgent',
            metric_type='throughput',
            metric_value=disruptions_found,
            unit='disruptions'
        )
        
        return {
            'status': 'success',
            'disruptions_found': disruptions_found
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def vision_inspector_agent_task(store_id, image_path):
    """
    Simulate YOLO-based vision inspection
    """
    try:
        store = Store.objects.get(id=store_id)
        
        # Mock YOLO detection results
        detected_objects = []
        anomalies = []
        action_required = False
        
        # Simulate detection of various objects
        object_types = ['product_box', 'empty_shelf', 'price_tag', 'customer', 'staff']
        for obj_type in object_types:
            if random.random() > 0.6:  # 40% chance of detecting each object type
                confidence = random.uniform(0.7, 0.98)
                bbox = [
                    random.randint(0, 500),
                    random.randint(0, 400),
                    random.randint(100, 200),
                    random.randint(100, 150)
                ]
                detected_objects.append({
                    'object': obj_type,
                    'confidence': round(confidence, 2),
                    'bbox': bbox
                })
        
        # Check for anomalies
        if random.random() > 0.7:  # 30% chance of anomalies
            possible_anomalies = [
                'empty_shelf_section',
                'misplaced_products', 
                'price_tag_missing',
                'spoiled_products',
                'cleanliness_issue'
            ]
            anomalies = random.sample(possible_anomalies, random.randint(1, 2))
            action_required = True
        
        inspection = VisionInspection.objects.create(
            store=store,
            image_path=image_path,
            inspection_type='shelf_stock',
            detected_objects=detected_objects,
            anomalies_found=anomalies,
            action_required=action_required,
            priority='high' if action_required else 'low',
            created_by_agent='VisionInspectorAgent'
        )
        
        AgentMetrics.objects.create(
            agent_name='VisionInspectorAgent',
            metric_type='response_time',
            metric_value=random.uniform(1500, 3000),
            unit='ms'
        )
        
        return {
            'status': 'success',
            'inspection_id': str(inspection.inspection_id),
            'objects_detected': len(detected_objects),
            'anomalies_found': len(anomalies),
            'action_required': action_required
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def explainer_agent_task(query, context_data):
    """
    Generate explanations using GPT-4 (mocked for demo)
    """
    try:
        # Mock GPT-4 response generation
        # Real implementation would call OpenAI API
        
        explanations = {
            'inventory': "The inventory levels show a concerning trend with several products approaching critical thresholds. Our AI forecasting suggests immediate action is needed.",
            'rebalance': "The rebalancing action was triggered by predictive analytics showing an 85% probability of stockout in the next 48 hours.",
            'route': "The route optimization considers real-time traffic data, fuel costs, and delivery priorities to minimize total delivery time.",
            'disruption': "External disruptions are automatically detected through multiple data sources including weather APIs, traffic feeds, and news monitoring.",
            'inspection': "Computer vision analysis identified potential issues that require human verification and corrective action."
        }
        
        # Determine explanation type based on context
        explanation_type = 'general'
        if 'rebalance' in context_data:
            explanation_type = 'rebalance'
        elif 'route' in context_data:
            explanation_type = 'route'
        elif 'disruption' in context_data:
            explanation_type = 'disruption'
        elif 'inspection' in context_data:
            explanation_type = 'inspection'
        elif 'inventory' in context_data:
            explanation_type = 'inventory'
        
        base_explanation = explanations.get(explanation_type, 
            "I analyzed the available data and coordinated with other AI agents to provide this comprehensive response.")
        
        # Add context-specific details
        if context_data:
            context_summary = f" Based on the following data: {json.dumps(context_data, indent=2)}"
            full_explanation = base_explanation + context_summary
        else:
            full_explanation = base_explanation
        
        explanation = AgentExplanation.objects.create(
            query=query,
            context_data=context_data,
            explanation_text=full_explanation,
            confidence_level='high',
            data_sources=['InventoryAgent', 'RebalancerAgent', 'RoutePlannerAgent'],
            tokens_used=random.randint(100, 500),
            response_time_ms=random.randint(1500, 3500),
            created_by_agent='ExplainerAgent'
        )
        
        AgentMetrics.objects.create(
            agent_name='ExplainerAgent',
            metric_type='response_time',
            metric_value=explanation.response_time_ms,
            unit='ms'
        )
        
        return {
            'status': 'success',
            'explanation_id': str(explanation.explanation_id),
            'explanation_text': full_explanation,
            'tokens_used': explanation.tokens_used
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def cortex_manager_task(event_type, involved_agents, coordination_data):
    """
    Coordinate multi-agent activities
    """
    try:
        coordination = CortexCoordination.objects.create(
            event_type=event_type,
            involved_agents=involved_agents,
            coordination_data=coordination_data,
            priority='medium',
            status='in_progress',
            execution_timeline=[],
            created_by_agent='CortexManager'
        )
        
        # Simulate coordination steps
        timeline = []
        for i, agent in enumerate(involved_agents):
            timeline.append({
                'step': i + 1,
                'agent': agent,
                'action': f'Coordinated with {agent}',
                'timestamp': timezone.now().isoformat(),
                'status': 'completed'
            })
        
        coordination.execution_timeline = timeline
        coordination.status = 'completed'
        coordination.completed_at = timezone.now()
        coordination.save()
        
        AgentMetrics.objects.create(
            agent_name='CortexManager',
            metric_type='response_time',
            metric_value=random.uniform(100, 300),
            unit='ms'
        )
        
        return {
            'status': 'success',
            'coordination_id': str(coordination.coordination_id),
            'agents_coordinated': len(involved_agents),
            'execution_steps': len(timeline)
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


# Periodic tasks for continuous monitoring
@shared_task
def periodic_system_health_check():
    """
    Regular health check of all agent systems
    """
    agents = [
        'InventoryAgent', 'RebalancerAgent', 'RoutePlannerAgent',
        'DelayMonitorAgent', 'VisionInspectorAgent', 'ExplainerAgent',
        'CortexManager'
    ]
    
    health_status = {}
    
    for agent in agents:
        # Check recent activity
        recent_metrics = AgentMetrics.objects.filter(
            agent_name=agent,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        )
        
        if recent_metrics.exists():
            avg_response_time = recent_metrics.filter(
                metric_type='response_time'
            ).aggregate(avg_time=timezone.now())
            
            health_status[agent] = {
                'status': 'healthy',
                'last_activity': recent_metrics.latest('timestamp').timestamp,
                'metrics_count': recent_metrics.count()
            }
        else:
            health_status[agent] = {
                'status': 'warning',
                'last_activity': None,
                'metrics_count': 0
            }
    
    return {
        'status': 'success',
        'timestamp': timezone.now().isoformat(),
        'agent_health': health_status
    }
