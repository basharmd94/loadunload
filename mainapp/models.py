from django.db import models

class Party(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Item(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class LoadUnload(models.Model):
    LOAD = 'Load'
    UNLOAD = 'Unload'
    TRANSACTION_TYPE_CHOICES = [
        (LOAD, 'Load'),
        (UNLOAD, 'Unload'),
    ]

    BOX_TYPE_CHOICES = [
        ('Bale', 'Bale'),
        ('Box', 'Box'),
        ('Bag', 'Bag'),
        ('Drum', 'Drum'),
        ('Cartoon', 'Cartoon'),
    ]

    QTY_TYPE_CHOICES = [
        ('kg', 'Kilogram'),
        ('meter', 'Meter'),
        ('pcs', 'Pieces'),
    ]

    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    truck_no = models.CharField(max_length=50)
    challan_no = models.CharField(max_length=50)
    supplier = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='supplied_transactions', null=True, blank=True)
    customer = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='customer_transactions', null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    box_type = models.CharField(max_length=20, choices=BOX_TYPE_CHOICES)
    box_qty = models.PositiveIntegerField()
    qty_type = models.CharField(max_length=10, choices=QTY_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_qty = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.challan_no} ({self.truck_no})"
