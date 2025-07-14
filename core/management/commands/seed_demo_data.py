from django.core.management.base import BaseCommand
from core.models import Inventory, TransferLog, DeliveryRoute, AgentLog
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with Walmart-style demo data for all endpoints.'

    def handle(self, *args, **options):
        # Clear old data
        Inventory.objects.all().delete()
        TransferLog.objects.all().delete()
        DeliveryRoute.objects.all().delete()
        AgentLog.objects.all().delete()

        # Inventory items
        stores = [
            "Walmart Supercenter #1234",
            "Walmart Neighborhood Market #5678",
            "Walmart Supercenter #4321",
            "Walmart Distribution Center - Dallas",
            "Walmart Distribution Center - Houston"
        ]
        products = [
            {"name": "Great Value Milk", "id": "MILK001"},
            {"name": "Great Value Eggs", "id": "EGGS001"},
            {"name": "Wonder Bread", "id": "BREAD001"},
            {"name": "Coca-Cola 12-pack", "id": "COKE012"},
            {"name": "Fresh Bananas", "id": "BANANA01"},
            {"name": "Tyson Chicken Breast", "id": "CHICK001"},
            {"name": "Lay's Classic Chips", "id": "CHIPS01"},
            {"name": "Red Bull 4-pack", "id": "RBULL04"},
            {"name": "Dole Salad Mix", "id": "SALAD01"},
            {"name": "Blue Bell Ice Cream", "id": "ICECRM1"}
        ]
        expiry_base = datetime(2025, 7, 20)
        for store in stores:
            for prod in products:
                Inventory.objects.create(
                    product_id=prod["id"],
                    product_name=prod["name"],
                    store_location=store,
                    quantity=random.randint(10, 120),
                    expiry_date=expiry_base + timedelta(days=random.randint(0, 10)),
                    last_updated=datetime.now() - timedelta(hours=random.randint(0, 48))
                )

        # Transfer logs
        transfer_reasons = [
            "Restocking for July 4th BBQ event",
            "Weekend breakfast rush",
            "Sandwich promotion",
            "Low stock alert triggered by AI agent",
            "High demand due to local sports game",
            "Seasonal sale preparation",
            "Inventory rebalancing for efficiency",
            "Fresh produce rotation",
            "New product launch",
            "Emergency restock after delivery delay"
        ]
        for i in range(20):
            prod = random.choice(products)
            from_store = random.choice(stores[3:])
            to_store = random.choice(stores[:3])
            TransferLog.objects.create(
                from_store=from_store,
                to_store=to_store,
                product=Inventory.objects.filter(product_name=prod["name"], store_location=from_store).first(),
                quantity=random.randint(5, 50),
                reason=random.choice(transfer_reasons)
            )

        # Delivery routes
        route_statuses = ["scheduled", "delayed", "delivered"]
        disruption_notes = [
            "Heavy traffic on I-635 due to construction",
            "Minor delay expected due to rain",
            "On time",
            "Accident reported near destination",
            "Road closure - rerouting",
            "Driver break required",
            "AI optimized route for fuel savings",
            "Weather alert: thunderstorm warning",
            "Delivery rescheduled due to stockout",
            "No disruptions"
        ]
        for i in range(20):
            prod = random.choice(products)
            from_store = random.choice(stores[3:])
            to_store = random.choice(stores[:3])
            DeliveryRoute.objects.create(
                route_id=f"{prod['id']}-{from_store.split()[-1]}-{to_store.split()[-1]}-{20250714+i}",
                start_point=from_store,
                end_point=to_store,
                eta=datetime.now() + timedelta(hours=random.randint(1, 5), minutes=random.randint(0, 59)),
                status=random.choice(route_statuses),
                disruption_notes=random.choice(disruption_notes)
            )

        # Agent logs
        agent_names = ["Rebalancer", "InventoryAgent", "RoutePlanner", "DelayMonitor", "VisionInspector", "ExplainerAgent"]
        actions = [
            "Moved 20 units of Great Value Milk for July 4th BBQ demand.",
            "Predicted 30% spike in eggs demand for weekend.",
            "Optimized delivery route to save 15 minutes.",
            "Detected traffic jam, rerouted delivery truck.",
            "Flagged empty shelf in produce section.",
            "Explained delivery delay due to weather.",
            "Approved emergency restock for Wonder Bread.",
            "Analyzed sales trend for Coca-Cola 12-pack.",
            "Generated forecast for Tyson Chicken Breast.",
            "Logged successful delivery of Blue Bell Ice Cream."
        ]
        for i in range(30):
            AgentLog.objects.create(
                agent_name=random.choice(agent_names),
                action=random.choice(actions)
            )

        self.stdout.write(self.style.SUCCESS('Demo data seeded for Walmart hackathon!'))
