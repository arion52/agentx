from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, agent_views

# Main router for existing endpoints
router = DefaultRouter()
router.register(r'inventory', views.InventoryViewSet)
router.register(r'transfers', views.TransferLogViewSet)
router.register(r'routes', views.DeliveryRouteViewSet)
router.register(r'logs', views.AgentLogViewSet)

# Agent system router for new endpoints
agent_router = DefaultRouter()
agent_router.register(r'stores', agent_views.StoreViewSet)
agent_router.register(r'products', agent_views.ProductViewSet)
agent_router.register(r'forecasts', agent_views.DemandForecastViewSet)
agent_router.register(r'rebalances', agent_views.StockRebalanceActionViewSet)
agent_router.register(r'route-optimizations', agent_views.RouteOptimizationViewSet)
agent_router.register(r'disruptions', agent_views.ExternalDisruptionViewSet)
agent_router.register(r'inspections', agent_views.VisionInspectionViewSet)
agent_router.register(r'explanations', agent_views.AgentExplanationViewSet)
agent_router.register(r'coordinations', agent_views.CortexCoordinationViewSet)
agent_router.register(r'metrics', agent_views.AgentMetricsViewSet)

urlpatterns = [
    # Legacy endpoints (maintain compatibility)
    path('', include(router.urls)),
    path('run-fake-agent/', views.run_fake_agent, name='run-fake-agent'),
    
    # New agent system endpoints
    path('agents/', include(agent_router.urls)),
    
    # Dashboard and system endpoints
    path('dashboard/summary/', agent_views.dashboard_summary, name='dashboard-summary'),
    path('dashboard/agent-health/', agent_views.agent_health, name='agent-health'),
    path('agents/simulate-workflow/', agent_views.simulate_agent_workflow, name='simulate-workflow'),
]
