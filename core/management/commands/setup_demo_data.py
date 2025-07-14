"""
Setup sample data for AgentX++ system demo
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.agent_models import Store, Product
from core.models import Inventory
import random


class Command(BaseCommand):
    help = 'Setup sample data for AgentX++ demo'

    def handle(self, *args, **options):
        self.stdout.write('Setting up AgentX++ sample data...')
        
        # Create stores
        stores_data = [
            {'store_id': 'WH001', 'name': 'Central Warehouse', 'location': 'Electronic City', 'store_type': 'warehouse', 'capacity': 5000},
            {'store_id': 'FC001', 'name': 'Fulfillment Center North', 'location': 'Hebbal', 'store_type': 'fulfillment_center', 'capacity': 3000},
            {'store_id': 'ST001', 'name': 'Whitefield Store', 'location': 'Whitefield', 'store_type': 'store', 'capacity': 500},
            {'store_id': 'ST002', 'name': 'Koramangala Store', 'location': 'Koramangala', 'store_type': 'store', 'capacity': 400},
            {'store_id': 'ST003', 'name': 'Indiranagar Store', 'location': 'Indiranagar', 'store_type': 'store', 'capacity': 450},
            {'store_id': 'ST004', 'name': 'BTM Layout Store', 'location': 'BTM Layout', 'store_type': 'store', 'capacity': 350},
            {'store_id': 'ST005', 'name': 'KR Puram Store', 'location': 'KR Puram', 'store_type': 'store', 'capacity': 300},
        ]
        
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                store_id=store_data['store_id'],
                defaults=store_data
            )
            if created:
                self.stdout.write(f'✅ Created store: {store.name}')
        
        # Create products
        products_data = [
            {'product_id': 'MILK001', 'name': 'Milk (1L)', 'category': 'Dairy', 'unit_price': 55.00, 'unit_weight': 1.0, 'shelf_life_days': 3},
            {'product_id': 'BREAD001', 'name': 'Bread (400g)', 'category': 'Bakery', 'unit_price': 25.00, 'unit_weight': 0.4, 'shelf_life_days': 2},
            {'product_id': 'RICE001', 'name': 'Rice (1kg)', 'category': 'Grains', 'unit_price': 45.00, 'unit_weight': 1.0, 'shelf_life_days': 365},
            {'product_id': 'EGGS001', 'name': 'Eggs (12 pcs)', 'category': 'Dairy', 'unit_price': 65.00, 'unit_weight': 0.6, 'shelf_life_days': 14},
            {'product_id': 'BISCUIT001', 'name': 'Biscuits (200g)', 'category': 'Snacks', 'unit_price': 35.00, 'unit_weight': 0.2, 'shelf_life_days': 90},
            {'product_id': 'TEA001', 'name': 'Tea (250g)', 'category': 'Beverages', 'unit_price': 125.00, 'unit_weight': 0.25, 'shelf_life_days': 730},
            {'product_id': 'SUGAR001', 'name': 'Sugar (1kg)', 'category': 'Essentials', 'unit_price': 42.00, 'unit_weight': 1.0, 'shelf_life_days': 365},
            {'product_id': 'OIL001', 'name': 'Cooking Oil (1L)', 'category': 'Essentials', 'unit_price': 95.00, 'unit_weight': 0.9, 'shelf_life_days': 365},
            {'product_id': 'CHIPS001', 'name': 'Potato Chips (100g)', 'category': 'Snacks', 'unit_price': 20.00, 'unit_weight': 0.1, 'shelf_life_days': 60},
            {'product_id': 'SOAP001', 'name': 'Bath Soap (100g)', 'category': 'Personal Care', 'unit_price': 25.00, 'unit_weight': 0.1, 'shelf_life_days': 1095},
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                product_id=product_data['product_id'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'✅ Created product: {product.name}')
        
        # Create inventory entries for each product at each store
        stores = Store.objects.all()
        products = Product.objects.all()
        
        for store in stores:
            for product in products:
                # Generate realistic inventory quantities based on store type
                if store.store_type == 'warehouse':
                    quantity = random.randint(500, 2000)
                elif store.store_type == 'fulfillment_center':
                    quantity = random.randint(200, 800)
                else:  # retail store
                    quantity = random.randint(10, 100)
                
                # Create both legacy inventory entry and new system entry
                inventory, created = Inventory.objects.get_or_create(
                    product_id=product.product_id,
                    product_name=product.name,
                    store_location=store.location,
                    defaults={
                        'quantity': quantity,
                        'expiry_date': timezone.now().date() + timezone.timedelta(days=product.shelf_life_days) if product.shelf_life_days else None,
                    }
                )
                
                if created:
                    self.stdout.write(f'✅ Created inventory: {product.name} at {store.name} ({quantity} units)')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Successfully set up AgentX++ demo data!\n'
                f'📦 {Store.objects.count()} stores created\n'
                f'🛍️ {Product.objects.count()} products created\n'
                f'📊 {Inventory.objects.count()} inventory entries created\n'
                f'\nYou can now run the agent simulations and view the dashboard!'
            )
        )
