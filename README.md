# AgentX Inventory Management API

A Django REST Framework-based API for managing inventory, transfers, delivery routes, and automated agent operations.

## Features

- **Inventory Management**: Track products across multiple store locations
- **Transfer Logging**: Record product movements between stores
- **Delivery Routes**: Schedule and track deliveries with status updates
- **Agent Operations**: Log automated agent actions and simulate workflows
- **Comprehensive API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Quick Start

### Prerequisites

- Python 3.8+
- Django 5.1+
- PostgreSQL (configured in settings)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd agentx
```

2. Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install django djangorestframework django-cors-headers drf-spectacular psycopg2-binary
```

4. Run migrations
```bash
python manage.py migrate
```

5. Load sample data (optional)
```bash
python manage.py loaddata core/fixtures/data.json
```

6. Start the development server
```bash
python manage.py runserver
```

## API Documentation

### Interactive Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### API Endpoints

#### Inventory Management
- `GET /api/inventory/` - List all inventory items
- `POST /api/inventory/` - Create new inventory item
- `GET /api/inventory/{id}/` - Get specific inventory item
- `PUT /api/inventory/{id}/` - Update inventory item
- `PATCH /api/inventory/{id}/` - Partially update inventory item
- `DELETE /api/inventory/{id}/` - Delete inventory item
- `GET /api/inventory/low_stock/` - Get items with low stock (query param: threshold)

#### Transfer Logs
- `GET /api/transfers/` - List all transfer logs
- `POST /api/transfers/` - Create new transfer log
- `GET /api/transfers/{id}/` - Get specific transfer log
- `PUT /api/transfers/{id}/` - Update transfer log
- `PATCH /api/transfers/{id}/` - Partially update transfer log
- `DELETE /api/transfers/{id}/` - Delete transfer log

#### Delivery Routes
- `GET /api/routes/` - List all delivery routes
- `POST /api/routes/` - Create new delivery route
- `GET /api/routes/{id}/` - Get specific delivery route
- `PUT /api/routes/{id}/` - Update delivery route
- `PATCH /api/routes/{id}/` - Partially update delivery route
- `DELETE /api/routes/{id}/` - Delete delivery route
- `GET /api/routes/active/` - Get active deliveries (scheduled/delayed)

#### Agent Logs
- `GET /api/logs/` - List all agent logs
- `POST /api/logs/` - Create new agent log
- `GET /api/logs/{id}/` - Get specific agent log
- `PUT /api/logs/{id}/` - Update agent log
- `PATCH /api/logs/{id}/` - Partially update agent log
- `DELETE /api/logs/{id}/` - Delete agent log

#### Agent Operations
- `POST /api/run-fake-agent/` - Simulate automated agent workflow

## Data Models

### Inventory
```json
{
  "id": 1,
  "product_id": "MILK001",
  "product_name": "Milk",
  "store_location": "Whitefield",
  "quantity": 50,
  "expiry_date": "2025-07-20",
  "last_updated": "2025-07-14T10:30:00Z"
}
```

### Transfer Log
```json
{
  "id": 1,
  "from_store": "KR Puram",
  "to_store": "Whitefield",
  "product": 1,
  "quantity": 10,
  "timestamp": "2025-07-14T10:30:00Z",
  "reason": "Stock too low in Whitefield"
}
```

### Delivery Route
```json
{
  "id": 1,
  "route_id": "milk-transfer-001",
  "start_point": "KR Puram",
  "end_point": "Whitefield",
  "eta": "2025-07-14T12:30:00Z",
  "status": "scheduled",
  "disruption_notes": ""
}
```

### Agent Log
```json
{
  "id": 1,
  "agent_name": "Rebalancer",
  "action": "Moved 10 milk units to Whitefield due to stock drop.",
  "timestamp": "2025-07-14T10:30:00Z"
}
```

## Example Usage

### Get Low Stock Items
```bash
curl -X GET "http://localhost:8000/api/inventory/low_stock/?threshold=20"
```

### Create New Inventory Item
```bash
curl -X POST "http://localhost:8000/api/inventory/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "BREAD001",
    "product_name": "Bread",
    "store_location": "Koramangala",
    "quantity": 30,
    "expiry_date": "2025-07-16"
  }'
```

### Log a Transfer
```bash
curl -X POST "http://localhost:8000/api/transfers/" \
  -H "Content-Type: application/json" \
  -d '{
    "from_store": "Central Warehouse",
    "to_store": "Koramangala",
    "product": 1,
    "quantity": 15,
    "reason": "Restocking request"
  }'
```

### Run Agent Simulation
```bash
curl -X POST "http://localhost:8000/api/run-fake-agent/"
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200 OK` - Successful GET, PUT, PATCH requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

Error responses include descriptive messages:
```json
{
  "error": "Milk inventory not found in Whitefield store"
}
```

## Pagination

List endpoints support pagination with the following parameters:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

Response includes pagination metadata:
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/inventory/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering and Search

### Query Parameters
- Inventory endpoints support filtering by `store_location`, `product_name`
- Transfer endpoints support filtering by `from_store`, `to_store`
- Delivery routes support filtering by `status`

Example:
```bash
curl "http://localhost:8000/api/inventory/?store_location=Whitefield&product_name=Milk"
```

## Authentication

Currently, the API allows anonymous access for development purposes. For production deployment, implement proper authentication:

1. Add authentication classes to `REST_FRAMEWORK` settings
2. Configure user permissions
3. Add API key or JWT token authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
