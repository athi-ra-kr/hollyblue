from django.db import models
import json


# ==========================================
# 1. EXISTING MODELS (Unchanged)
# ==========================================

class FloorPlan(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='floorplans/')

    def __str__(self):
        return self.name


class KitchenItem(models.Model):
    name = models.CharField(max_length=100)
    kitchen_shape = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)
    material = models.CharField(max_length=50)

    # Dimensions needed for calculation logic
    length = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    specification = models.TextField(blank=True)
    image = models.ImageField(upload_to='kitchen/', blank=True, null=True)

    def __str__(self):
        return self.name


class KitchenAccessory(models.Model):
    name = models.CharField(max_length=100)
    unit_type = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True)

    length = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    specification = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GeneralModule(models.Model):
    # Handles TV Unit, Wardrobe, Mirror, etc.
    category = models.CharField(max_length=100)  # e.g. "TV Unit"
    sub_type = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=50)

    # Dimensions
    length = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    specification = models.TextField(blank=True)
    image = models.ImageField(upload_to='modules/', blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.sub_type}"


# ==========================================
# 2. UPDATED ENQUIRY MODELS
# ==========================================

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=200)
    sqft = models.CharField(max_length=50, null=True, blank=True)

    # Updated: Added default value
    status = models.CharField(max_length=50, default='Pending')

    total_amount = models.CharField(max_length=50)

    # We keep 'details' as a backup, but mostly use EnquiryDetail now
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Helper method to parse JSON if needed (optional but good for safety)
    def get_details_list(self):
        try:
            if self.details:
                return json.loads(self.details)
            return []
        except:
            return []

    def __str__(self):
        return f"{self.name} - {self.mobile}"


class EnquiryDetail(models.Model):
    # This links individual items to the main Enquiry
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='items')

    category = models.CharField(max_length=100)
    item_name = models.CharField(max_length=200)
    material = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    # Using DecimalField for better price math
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.item_name} ({self.category})"