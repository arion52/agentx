# AgentX++ API Documentation

## Overview

The AgentX++ Inventory Management API is a comprehensive RESTful service built with Django REST Framework that provides advanced multi-agent AI capabilities for supply chain management. The system features 7 specialized AI agents working in coordination to automate inventory management, route optimization, and real-time decision making.

## Base URL

```
http://localhost:8000/api/
```

## AI Agents

The system includes 7 specialized AI agents:

1. **Inventory Agent (LNN)** - Demand forecasting using Liquid Neural Networks
2. **Rebalancer Agent** - Intelligent stock rebalancing and transfer optimization
3. **Route Planner Agent** - Dynamic route optimization with traffic awareness
4. **Delay Monitor Agent** - Real-time disruption detection and monitoring
5. **Vision Inspector Agent (YOLO)** - Computer vision-based store inspections
6. **Explainer Agent (GPT-4)** - Natural language explanations and insights
7. **Cortex Manager** - Multi-agent coordination and orchestration

## Authentication

Currently uses Django's session authentication. For production, implement token-based authentication.

## Content Type

All requests and responses use JSON format:
```
Content-Type: application/json
```

## Standard Response Format

### Success Response
```json
{
  "data": {
    // Response data here
  },
  "message": "Success message",
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error description",
  "status": "error",
  "code": 400
}
```

## Endpoints

### Dashboard & System Monitoring

#### Get Dashboard Summary
```http
GET /api/dashboard/summary/
```

**Response:**
```json
{
  "total_stores": 7,
  "total_products": 10,
  "active_rebalances": 3,
  "pending_inspections": 2,
  "current_disruptions": 1,
  "recent_explanations": 5,
  "agent_status": {
    "InventoryAgent": "healthy",
    "RebalancerAgent": "healthy",
    "RoutePlannerAgent": "healthy",
    "DelayMonitorAgent": "warning",
    "VisionInspectorAgent": "healthy",
    "ExplainerAgent": "healthy",
    "CortexManager": "healthy"
  },
  "recent_forecasts": [...],
  "active_routes": [...],
  "critical_alerts": [...]
}
```

#### Get Agent Health Status
```http
GET /api/dashboard/agent-health/
```

**Response:**
```json
[
  {
    "agent_name": "InventoryAgent",
    "status": "healthy",
    "last_activity": "2025-07-14T10:25:00Z",
    "response_time_avg": 245.5,
    "success_rate": 99.2,
    "error_count_24h": 1
  }
]
```

#### Simulate Multi-Agent Workflow
```http
POST /api/agents/simulate-workflow/
```

This endpoint demonstrates complex multi-agent coordination:
1. Inventory Agent creates demand forecast
2. Rebalancer Agent triggers stock transfer
3. Route Planner optimizes delivery route
4. Delay Monitor detects disruptions
5. Vision Inspector flags store issues
6. Cortex Manager coordinates all agents
7. Explainer Agent provides summary

**Response:**
```json
{
  "status": "success",
  "message": "Multi-agent workflow simulation completed successfully",
  "simulation_log": [
    "✅ InventoryAgent: Created demand forecast",
    "✅ RebalancerAgent: Created rebalance action",
    "✅ RoutePlannerAgent: Created optimized route",
    "✅ DelayMonitorAgent: Detected traffic disruption",
    "✅ VisionInspectorAgent: Detected shelf issues",
    "✅ CortexManager: Coordinated multi-agent response",
    "✅ ExplainerAgent: Generated comprehensive explanation"
  ],
  "coordination_id": "uuid-string",
  "explanation": "Detailed explanation of workflow...",
  "affected_entities": {...}
}
```

### AI Agent Endpoints

#### 1. Inventory Agent (LNN Forecasting)

##### List Demand Forecasts
```http
GET /api/agents/forecasts/
```

##### Create Demand Forecast
```http
POST /api/agents/forecasts/
```

**Request Body:**
```json
{
  "store": 1,
  "product": 1,
  "forecast_date": "2025-07-15",
  "predicted_demand": 75,
  "confidence_score": 0.92,
  "forecast_horizon_days": 7,
  "external_factors": {
    "weather": "heavy_rain",
    "event": "cricket_match"
  }
}
```

##### Get High Confidence Forecasts
```http
GET /api/agents/forecasts/high_confidence/?confidence=0.9
```

##### Get Recent Forecasts
```http
GET /api/agents/forecasts/recent/?days=7
```

#### 2. Rebalancer Agent

##### List Stock Rebalance Actions
```http
GET /api/agents/rebalances/
```

##### Create Rebalance Action
```http
POST /api/agents/rebalances/
```

**Request Body:**
```json
{
  "source_store": 1,
  "target_store": 2,
  "product": 1,
  "quantity": 50,
  "urgency": "high",
  "reason": "Predicted stockout based on demand forecast"
}
```

##### Get Pending Actions
```http
GET /api/agents/rebalances/pending/
```

##### Get Critical Actions
```http
GET /api/agents/rebalances/critical/
```

#### 3. Route Planner Agent

##### List Route Optimizations
```http
GET /api/agents/route-optimizations/
```

##### Create Route Optimization
```http
POST /api/agents/route-optimizations/
```

**Request Body:**
```json
{
  "rebalance_action": 1,
  "start_location": 1,
  "end_location": 2,
  "total_distance_km": 15.7,
  "estimated_duration_hours": 1.2,
  "estimated_cost": 450.00,
  "traffic_conditions": "medium",
  "waypoints": [
    {"lat": 12.9716, "lng": 77.5946, "name": "Checkpoint 1"}
  ],
  "alternative_routes": [...]
}
```

##### Get Active Routes
```http
GET /api/agents/route-optimizations/active/
```

##### Get Delayed Routes
```http
GET /api/agents/route-optimizations/delayed/
```

#### 4. Delay Monitor Agent

##### List External Disruptions
```http
GET /api/agents/disruptions/
```

##### Create Disruption Alert
```http
POST /api/agents/disruptions/
```

**Request Body:**
```json
{
  "event_type": "weather",
  "title": "Heavy rainfall expected",
  "description": "IMD predicts heavy rainfall affecting delivery routes",
  "severity": "medium",
  "affected_areas": ["Whitefield", "Electronic City"],
  "start_time": "2025-07-14T15:00:00Z",
  "end_time": "2025-07-14T22:00:00Z",
  "impact_radius_km": 10.0,
  "data_source": "WeatherAPI"
}
```

##### Get Active Disruptions
```http
GET /api/agents/disruptions/active/
```

##### Get Critical Disruptions
```http
GET /api/agents/disruptions/critical/
```

#### 5. Vision Inspector Agent (YOLO)

##### List Vision Inspections
```http
GET /api/agents/inspections/
```

##### Create Vision Inspection
```http
POST /api/agents/inspections/
```

**Request Body:**
```json
{
  "store": 1,
  "image_path": "/inspections/store_shelf_001.jpg",
  "inspection_type": "shelf_stock",
  "detected_objects": [
    {
      "object": "empty_shelf",
      "confidence": 0.95,
      "bbox": [100, 200, 300, 400]
    }
  ],
  "anomalies_found": ["empty_shelf_section", "misplaced_products"],
  "action_required": true,
  "priority": "high"
}
```

##### Get Inspections Requiring Action
```http
GET /api/agents/inspections/action_required/
```

##### Get Urgent Inspections
```http
GET /api/agents/inspections/urgent/
```

#### 6. Explainer Agent (GPT-4)

##### List Agent Explanations
```http
GET /api/agents/explanations/
```

##### Request Explanation
```http
POST /api/agents/explanations/
```

**Request Body:**
```json
{
  "query": "Why was today's delivery delayed and what actions were taken?",
  "context_data": {
    "rebalance_id": "uuid-string",
    "route_id": "uuid-string",
    "disruption_id": "uuid-string"
  }
}
```

**Response:**
```json
{
  "explanation_id": "uuid-string",
  "query": "Why was today's delivery delayed...",
  "explanation_text": "Today's delivery was delayed due to heavy traffic on Hosur Road caused by an accident. The system automatically detected this disruption and took the following actions: ...",
  "confidence_level": "high",
  "data_sources": ["DelayMonitorAgent", "RoutePlannerAgent"],
  "tokens_used": 325,
  "response_time_ms": 2150
}
```

##### Get Recent Explanations
```http
GET /api/agents/explanations/recent/?hours=24
```

#### 7. Cortex Manager (Orchestration)

##### List Coordination Events
```http
GET /api/agents/coordinations/
```

##### Get Active Coordinations
```http
GET /api/agents/coordinations/active/
```

**Response:**
```json
[
  {
    "coordination_id": "uuid-string",
    "event_type": "disruption_handled",
    "involved_agents": ["RebalancerAgent", "RoutePlannerAgent", "DelayMonitorAgent"],
    "priority": "medium",
    "status": "in_progress",
    "execution_timeline": [
      {
        "step": 1,
        "action": "Detected disruption",
        "timestamp": "2025-07-14T10:30:00Z"
      }
    ]
  }
]
```

### Support System Endpoints

#### Stores Management
```http
GET /api/agents/stores/
POST /api/agents/stores/
GET /api/agents/stores/by_type/?store_type=warehouse
```

#### Products Management
```http
GET /api/agents/products/
POST /api/agents/products/
```

#### Agent Metrics
```http
GET /api/agents/metrics/
GET /api/agents/metrics/by_agent/?agent_name=InventoryAgent
```

### Legacy Endpoints (Maintained for Compatibility)

#### 1. Inventory Management

#### List Inventory Items
```http
GET /api/inventory/
```

**Query Parameters:**
- `page` (integer): Page number for pagination
- `page_size` (integer): Number of items per page (max: 100)
- `store_location` (string): Filter by store location
- `product_name` (string): Filter by product name

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/inventory/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "product_id": "MILK001",
      "product_name": "Milk",
      "store_location": "Whitefield",
      "quantity": 45,
      "expiry_date": "2025-07-20",
      "last_updated": "2025-07-14T10:30:00Z"
    }
  ]
}
```

#### Create Inventory Item
```http
POST /api/inventory/
```

**Request Body:**
```json
{
  "product_id": "BREAD001",
  "product_name": "Bread",
  "store_location": "Koramangala",
  "quantity": 30,
  "expiry_date": "2025-07-16"
}
```

#### Get Low Stock Items
```http
GET /api/inventory/low_stock/?threshold=10
```

#### 2. Transfer Logs

#### List Transfer Logs
```http
GET /api/transfers/
```

#### Create Transfer Log
```http
POST /api/transfers/
```

**Request Body:**
```json
{
  "from_store": "Central Warehouse",
  "to_store": "Koramangala",
  "product": 1,
  "quantity": 15,
  "reason": "Restocking request"
}
```

#### 3. Delivery Routes

#### List Delivery Routes
```http
GET /api/routes/
```

#### Create Delivery Route
```http
POST /api/routes/
```

**Request Body:**
```json
{
  "route_id": "ROUTE001",
  "start_point": "Central Warehouse",
  "end_point": "Koramangala",
  "eta": "2025-07-14T15:30:00Z",
  "status": "scheduled",
  "disruption_notes": ""
}
```

#### Get Active Deliveries
```http
GET /api/routes/active/
```

#### 4. Agent Logs

#### List Agent Logs
```http
GET /api/logs/
```

#### Create Agent Log
```http
POST /api/logs/
```

**Request Body:**
```json
{
  "agent_name": "StockMonitor",
  "action": "Detected low stock in Whitefield store for product Milk"
}
```

#### 5. Legacy Agent Operations

#### Run Agent Simulation
```http
POST /api/run-fake-agent/
```

This endpoint simulates an automated inventory management agent workflow:

1. Reduces milk inventory in Whitefield store
2. Creates a transfer log from KR Puram to Whitefield
3. Schedules a delivery route
4. Logs the agent action

**Response:**
```json
{
  "message": "Transfer completed. ETA 2:40 PM.",
  "explanation": "10 crates of milk rebalanced from KR Puram to Whitefield due to low stock."
}
```

## New AgentX++ Features

### Multi-Agent Coordination
The system now supports complex workflows where multiple AI agents work together:
- **Event-driven processing** where one agent's output triggers another
- **Conflict resolution** through the Cortex Manager
- **Real-time coordination** with status tracking and execution timelines
- **Background processing** using Celery for AI model integration

### Advanced Analytics
- **Agent performance metrics** with response times and success rates
- **System health monitoring** with real-time status updates
- **Predictive analytics** using LNN-based demand forecasting
- **Computer vision analytics** with YOLO-based anomaly detection

### Real-time Capabilities
- **Live dashboard updates** showing agent status and KPIs
- **Event streaming** for disruption monitoring and alerts
- **Background task processing** for AI model computations
- **WebSocket support** for real-time frontend integration

## Integration Examples

### React Frontend Integration
```javascript
// Get dashboard data
const dashboardData = await fetch('/api/dashboard/summary/').then(r => r.json());

// Trigger agent workflow
const simulation = await fetch('/api/agents/simulate-workflow/', {
  method: 'POST'
}).then(r => r.json());

// Monitor agent health
const agentHealth = await fetch('/api/dashboard/agent-health/').then(r => r.json());
```

### Background Task Integration
```python
# Trigger LNN forecasting
from core.agent_tasks import inventory_agent_forecast_task
result = inventory_agent_forecast_task.delay(store_id=1, product_id=1)

# Process YOLO inspection
from core.agent_tasks import vision_inspector_agent_task
result = vision_inspector_agent_task.delay(store_id=1, image_path="/path/to/image.jpg")
```

### Multi-Agent Workflow
```python
# Complex workflow coordination
from core.agent_tasks import cortex_manager_task
coordination = cortex_manager_task.delay(
    event_type="rebalance_triggered",
    involved_agents=["InventoryAgent", "RebalancerAgent", "RoutePlannerAgent"],
    coordination_data={"trigger": "low_stock_alert"}
)
```

## Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Agent temporarily unavailable

## Rate Limiting

AgentX++ implements intelligent rate limiting:
- **Agent-specific limits** to prevent overloading AI models
- **Background processing** for expensive operations
- **Priority queuing** for critical agent tasks
- **Graceful degradation** when limits are reached

## Validation Rules

### Agent-Specific Validation

#### Demand Forecasts
- `confidence_score`: Required, float between 0.0 and 1.0
- `forecast_horizon_days`: Required, integer between 1 and 365
- `external_factors`: Optional JSON object with weather, events, etc.

#### Stock Rebalance Actions
- `urgency`: Required, one of: low, medium, high, critical
- `quantity`: Required, must be > 0 and <= source store capacity
- `estimated_cost`: Optional, decimal with max 2 decimal places

#### Route Optimizations
- `total_distance_km`: Required, positive float
- `estimated_duration_hours`: Required, positive float
- `traffic_conditions`: Optional, one of: light, medium, heavy
- `waypoints`: Optional array of coordinate objects

#### External Disruptions
- `severity`: Required, one of: low, medium, high, critical
- `impact_radius_km`: Required, positive float
- `affected_areas`: Required array of location strings
- `start_time`: Required, must be valid datetime
- `end_time`: Optional, must be after start_time

#### Vision Inspections
- `detected_objects`: Required array of detection objects with bbox coordinates
- `confidence_scores`: Required dict with detection confidence levels
- `action_required`: Required boolean
- `priority`: Required, one of: low, medium, high, urgent

#### Agent Explanations
- `query`: Required string, max 1000 characters
- `context_data`: Optional JSON object with relevant context
- `confidence_level`: Automatically determined, one of: low, medium, high

#### Cortex Coordinations
- `involved_agents`: Required array of agent names
- `coordination_data`: Required JSON object with coordination context
- `priority`: Required, one of: low, medium, high, critical

### Inventory
- `product_id`: Required, max 100 characters, must be unique per store
- `product_name`: Required, max 255 characters
- `store_location`: Required, max 255 characters
- `quantity`: Required, must be >= 0
- `expiry_date`: Optional, must be valid date

### Transfer Log
- `from_store`: Required, max 255 characters
- `to_store`: Required, max 255 characters, must be different from from_store
- `product`: Required, must exist in inventory
- `quantity`: Required, must be > 0
- `reason`: Required

### Delivery Route
- `route_id`: Required, max 100 characters, should be unique
- `start_point`: Required, max 255 characters
- `end_point`: Required, max 255 characters
- `eta`: Required, must be future datetime
- `status`: Required, one of: scheduled, delayed, delivered

## Examples

### Python (requests)
```python
import requests

# Get inventory items
response = requests.get('http://localhost:8000/api/inventory/')
inventory = response.json()

# Create new inventory item
new_item = {
    'product_id': 'EGGS001',
    'product_name': 'Eggs',
    'store_location': 'Indiranagar',
    'quantity': 50
}
response = requests.post('http://localhost:8000/api/inventory/', json=new_item)
```

### JavaScript (fetch)
```javascript
// Get low stock items
fetch('http://localhost:8000/api/inventory/low_stock/?threshold=5')
  .then(response => response.json())
  .then(data => console.log(data));

// Create transfer log
const transferData = {
  from_store: 'Warehouse',
  to_store: 'Koramangala',
  product: 1,
  quantity: 20,
  reason: 'Weekly restock'
};

fetch('http://localhost:8000/api/transfers/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(transferData)
});
```

### cURL
```bash
# Get inventory for specific store
curl -X GET "http://localhost:8000/api/inventory/?store_location=Whitefield"

# Create delivery route
curl -X POST "http://localhost:8000/api/routes/" \
  -H "Content-Type: application/json" \
  -d '{
    "route_id": "ROUTE002",
    "start_point": "Warehouse",
    "end_point": "BTM Layout",
    "eta": "2025-07-15T10:00:00Z",
    "status": "scheduled"
  }'
```

## Troubleshooting

### Common Issues

1. **404 Not Found**
   - Check the endpoint URL
   - Ensure the resource ID exists

2. **400 Bad Request**
   - Validate request data format
   - Check required fields
   - Ensure foreign key references exist

3. **500 Internal Server Error**
   - Check server logs
   - Verify database connectivity
   - Ensure all migrations are applied

### Debug Mode

For development, enable debug mode in Django settings to get detailed error messages.

## Support

For questions or issues:
1. Check the interactive API documentation at `/api/docs/`
2. Review the error message and status code
3. Consult the Django REST Framework documentation
4. Check server logs for detailed error information

## Advanced Examples

### Multi-Agent Workflow Simulation
```python
import requests

# Trigger comprehensive agent simulation
response = requests.post('http://localhost:8000/api/agents/simulate-workflow/')
simulation = response.json()

print(f"Workflow Status: {simulation['status']}")
print(f"Coordination ID: {simulation['coordination_id']}")
print("Agent Actions:")
for log_entry in simulation['simulation_log']:
    print(f"  {log_entry}")
```

### Real-time Dashboard Integration
```javascript
// WebSocket connection for real-time updates
const ws = new WebSocket('ws://localhost:8000/ws/dashboard/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    updateDashboard(data);
};

// Fetch initial dashboard state
fetch('/api/dashboard/summary/')
    .then(response => response.json())
    .then(data => initializeDashboard(data));
```

### AI Agent Task Monitoring
```python
# Monitor background AI tasks
from celery.result import AsyncResult

# Check LNN forecasting task
result = AsyncResult('task-id-here')
if result.ready():
    forecast_data = result.get()
    print(f"Forecast: {forecast_data['predicted_demand']} units")
    print(f"Confidence: {forecast_data['confidence']}")
```

### Agent Health Monitoring
```bash
# Check agent health via CLI
curl -X GET "http://localhost:8000/api/dashboard/agent-health/" | jq '.[].status'

# Monitor specific agent metrics
curl -X GET "http://localhost:8000/api/agents/metrics/by_agent/?agent_name=InventoryAgent"
```

### Complex Query Examples
```bash
# Get high-confidence forecasts for specific store
curl "http://localhost:8000/api/agents/forecasts/?store=1&confidence_score__gte=0.9"

# Get critical rebalance actions pending approval
curl "http://localhost:8000/api/agents/rebalances/critical/"

# Get active routes affected by current disruptions
curl "http://localhost:8000/api/agents/route-optimizations/active/"

# Get recent vision inspections requiring action
curl "http://localhost:8000/api/agents/inspections/action_required/"
```

### Error Handling Examples
```python
import requests

try:
    response = requests.post('/api/agents/simulate-workflow/')
    if response.status_code == 503:
        print("Agent temporarily unavailable - retrying...")
    elif response.status_code == 400:
        print("Invalid request:", response.json()['error'])
    else:
        print("Simulation successful:", response.json())
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```
