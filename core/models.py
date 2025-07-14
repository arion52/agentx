from django.db import models
from django.utils import timezone

class Inventory(models.Model):
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    store_location = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

class TransferLog(models.Model):
    from_store = models.CharField(max_length=255)
    to_store = models.CharField(max_length=255)
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

class DeliveryRoute(models.Model):
    route_id = models.CharField(max_length=100)
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    eta = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('delayed', 'Delayed'),
        ('delivered', 'Delivered')
    ])
    disruption_notes = models.TextField(blank=True)

class AgentLog(models.Model):
    agent_name = models.CharField(max_length=255)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
