from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import run_fake_agent

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet)
router.register(r'transfers', TransferLogViewSet)
router.register(r'routes', DeliveryRouteViewSet)
router.register(r'logs', AgentLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run-fake-agent/', run_fake_agent),
    # Include all agent system endpoints
    path('', include('core.agent_urls')),
]
