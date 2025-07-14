from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .models import Inventory, TransferLog, DeliveryRoute, AgentLog
from .serializers import *
from datetime import datetime, timedelta


@extend_schema_view(
    list=extend_schema(
        summary="List all inventory items",
        description="Retrieve a list of all inventory items across all stores",
        responses={200: InventorySerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create new inventory item",
        description="Add a new product to inventory",
        responses={201: InventorySerializer}
    ),
    retrieve=extend_schema(
        summary="Get inventory item details",
        description="Retrieve details of a specific inventory item by ID",
        responses={200: InventorySerializer}
    ),
    update=extend_schema(
        summary="Update inventory item",
        description="Update all fields of an inventory item",
        responses={200: InventorySerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update inventory item",
        description="Update specific fields of an inventory item",
        responses={200: InventorySerializer}
    ),
    destroy=extend_schema(
        summary="Delete inventory item",
        description="Remove an inventory item from the system",
        responses={204: None}
    )
)
class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory items.
    
    Provides CRUD operations for inventory management including:
    - Listing all inventory items
    - Creating new inventory entries
    - Retrieving, updating, and deleting specific items
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @extend_schema(
        summary="Get low stock items",
        description="Retrieve inventory items with quantity below specified threshold",
        parameters=[
            OpenApiParameter(
                name='threshold',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Stock threshold (default: 10)',
                default=10
            )
        ],
        responses={200: InventorySerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get inventory items with low stock."""
        threshold = int(request.query_params.get('threshold', 10))
        low_stock_items = self.queryset.filter(quantity__lt=threshold)
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all transfer logs",
        description="Retrieve a list of all product transfers between stores",
        responses={200: TransferLogSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create new transfer log",
        description="Log a new product transfer between stores",
        responses={201: TransferLogSerializer}
    ),
    retrieve=extend_schema(
        summary="Get transfer log details",
        description="Retrieve details of a specific transfer log by ID",
        responses={200: TransferLogSerializer}
    ),
    update=extend_schema(
        summary="Update transfer log",
        description="Update all fields of a transfer log",
        responses={200: TransferLogSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update transfer log",
        description="Update specific fields of a transfer log",
        responses={200: TransferLogSerializer}
    ),
    destroy=extend_schema(
        summary="Delete transfer log",
        description="Remove a transfer log from the system",
        responses={204: None}
    )
)
class TransferLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transfer logs.
    
    Tracks all product movements between different store locations
    including quantities, timestamps, and reasons for transfers.
    """
    queryset = TransferLog.objects.all()
    serializer_class = TransferLogSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all delivery routes",
        description="Retrieve a list of all delivery routes and their status",
        responses={200: DeliveryRouteSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create new delivery route",
        description="Schedule a new delivery route",
        responses={201: DeliveryRouteSerializer}
    ),
    retrieve=extend_schema(
        summary="Get delivery route details",
        description="Retrieve details of a specific delivery route by ID",
        responses={200: DeliveryRouteSerializer}
    ),
    update=extend_schema(
        summary="Update delivery route",
        description="Update all fields of a delivery route",
        responses={200: DeliveryRouteSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update delivery route",
        description="Update specific fields of a delivery route",
        responses={200: DeliveryRouteSerializer}
    ),
    destroy=extend_schema(
        summary="Delete delivery route",
        description="Remove a delivery route from the system",
        responses={204: None}
    )
)
class DeliveryRouteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing delivery routes.
    
    Handles scheduling, tracking, and status updates for deliveries
    between different locations in the supply chain.
    """
    queryset = DeliveryRoute.objects.all()
    serializer_class = DeliveryRouteSerializer

    @extend_schema(
        summary="Get active deliveries",
        description="Retrieve delivery routes that are currently scheduled or delayed",
        responses={200: DeliveryRouteSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get currently active (scheduled/delayed) deliveries."""
        active_deliveries = self.queryset.filter(status__in=['scheduled', 'delayed'])
        serializer = self.get_serializer(active_deliveries, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all agent logs",
        description="Retrieve a list of all actions performed by automated agents",
        responses={200: AgentLogSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create new agent log",
        description="Log a new action performed by an automated agent",
        responses={201: AgentLogSerializer}
    ),
    retrieve=extend_schema(
        summary="Get agent log details",
        description="Retrieve details of a specific agent log by ID",
        responses={200: AgentLogSerializer}
    ),
    update=extend_schema(
        summary="Update agent log",
        description="Update all fields of an agent log",
        responses={200: AgentLogSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update agent log",
        description="Update specific fields of an agent log",
        responses={200: AgentLogSerializer}
    ),
    destroy=extend_schema(
        summary="Delete agent log",
        description="Remove an agent log from the system",
        responses={204: None}
    )
)
class AgentLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing agent logs.
    
    Records and tracks all actions performed by automated agents
    in the system for audit and monitoring purposes.
    """
    queryset = AgentLog.objects.all()
    serializer_class = AgentLogSerializer


@extend_schema(
    summary="Run fake agent simulation",
    description="""
    Simulates an automated agent performing inventory rebalancing operations.
    
    This endpoint demonstrates the agent workflow by:
    1. Reducing inventory quantity for milk in Whitefield store
    2. Creating a transfer log from KR Puram to Whitefield
    3. Scheduling a delivery route with 2-hour ETA
    4. Logging the agent action for audit purposes
    
    This is a demonstration endpoint showing how the system handles
    automated inventory management and rebalancing.
    """,
    methods=['POST'],
    request=None,
    responses={
        200: OpenApiResponse(
            description="Agent simulation completed successfully",
            examples=[
                {
                    "application/json": {
                        "message": "Transfer completed. ETA 2:40 PM.",
                        "explanation": "10 crates of milk rebalanced from KR Puram to Whitefield due to low stock."
                    }
                }
            ]
        ),
        400: OpenApiResponse(description="Bad request - simulation failed"),
        500: OpenApiResponse(description="Internal server error")
    },
    tags=['Agent Operations']
)
@api_view(['POST'])
def run_fake_agent(request):
    """
    Simulate automated agent performing inventory rebalancing.
    
    This endpoint demonstrates the complete workflow of an automated
    inventory management agent including stock monitoring, transfer
    scheduling, and delivery route planning.
    """
    try:
        # 1. Fake inventory changes for Walmart hackathon
        milk = Inventory.objects.get(product_name="Great Value Milk", store_location="Walmart Supercenter #1234")
        eggs = Inventory.objects.get(product_name="Great Value Eggs", store_location="Walmart Supercenter #1234")
        bread = Inventory.objects.get(product_name="Wonder Bread", store_location="Walmart Supercenter #1234")

        milk.quantity -= 8  # Simulate drop in milk stock
        eggs.quantity -= 12 # Simulate drop in eggs stock
        bread.quantity -= 5 # Simulate drop in bread stock
        milk.save()
        eggs.save()
        bread.save()

        # 2. Create transfers for multiple products
        TransferLog.objects.create(
            from_store="Walmart Distribution Center - Dallas",
            to_store="Walmart Supercenter #1234",
            product=milk,
            quantity=20,
            reason="Restocking Great Value Milk due to high demand (July 4th BBQ)"
        )
        TransferLog.objects.create(
            from_store="Walmart Distribution Center - Dallas",
            to_store="Walmart Supercenter #1234",
            product=eggs,
            quantity=30,
            reason="Eggs restock for weekend breakfast rush"
        )
        TransferLog.objects.create(
            from_store="Walmart Distribution Center - Dallas",
            to_store="Walmart Supercenter #1234",
            product=bread,
            quantity=15,
            reason="Wonder Bread restock for sandwich promotion"
        )

        # 3. Create delivery routes for each product
        DeliveryRoute.objects.create(
            route_id="milk-dallas-1234-20250714",
            start_point="Walmart Distribution Center - Dallas",
            end_point="Walmart Supercenter #1234",
            eta=datetime.now() + timedelta(hours=2),
            status="scheduled",
            disruption_notes="Heavy traffic on I-635 due to construction"
        )
        DeliveryRoute.objects.create(
            route_id="eggs-dallas-1234-20250714",
            start_point="Walmart Distribution Center - Dallas",
            end_point="Walmart Supercenter #1234",
            eta=datetime.now() + timedelta(hours=2, minutes=30),
            status="scheduled",
            disruption_notes="Minor delay expected due to rain"
        )
        DeliveryRoute.objects.create(
            route_id="bread-dallas-1234-20250714",
            start_point="Walmart Distribution Center - Dallas",
            end_point="Walmart Supercenter #1234",
            eta=datetime.now() + timedelta(hours=1, minutes=45),
            status="scheduled",
            disruption_notes="On time"
        )

        # 4. Agent logs for each action
        AgentLog.objects.create(
            agent_name="Rebalancer",
            action="Moved 20 units of Great Value Milk to Walmart Supercenter #1234 for July 4th BBQ demand."
        )
        AgentLog.objects.create(
            agent_name="Rebalancer",
            action="Moved 30 units of Great Value Eggs to Walmart Supercenter #1234 for weekend breakfast rush."
        )
        AgentLog.objects.create(
            agent_name="Rebalancer",
            action="Moved 15 units of Wonder Bread to Walmart Supercenter #1234 for sandwich promotion."
        )

        # 5. Return detailed Walmart-style explanation
        return Response({
            "message": "Transfers completed. Milk, eggs, and bread restocked at Walmart Supercenter #1234.",
            "explanation": (
                "20 units of Great Value Milk, 30 units of Great Value Eggs, and 15 units of Wonder Bread "
                "were rebalanced from Dallas Distribution Center to Walmart Supercenter #1234. "
                "Reasons: July 4th BBQ demand spike, weekend breakfast rush, and sandwich promotion. "
                "Delivery routes scheduled with minor delays due to traffic and weather."
            )
        })
    except Inventory.DoesNotExist:
        return Response(
            {"error": "Required inventory not found in Walmart Supercenter #1234"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Agent simulation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )