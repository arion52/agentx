# AgentX API Documentation

## Overview

The AgentX Inventory Management API is a RESTful service built with Django REST Framework that provides comprehensive inventory management capabilities for multi-store operations.

## Base URL

```
http://localhost:8000/api/
```

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

### 1. Inventory Management

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

### 2. Transfer Logs

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

### 3. Delivery Routes

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

### 4. Agent Logs

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

### 5. Agent Operations

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

## Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Implement rate limiting per IP/user
- Consider throttling for expensive operations

## Validation Rules

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
