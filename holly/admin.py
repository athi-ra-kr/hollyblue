from django.contrib import admin
from .models import FloorPlan, Enquiry, KitchenItem, KitchenAccessory, GeneralModule

# 1. Floor Plan Admin
@admin.register(FloorPlan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)

# 2. Enquiry Admin (Includes 'Data Saved?' check)
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'location', 'status', 'total_amount', 'created_at', 'has_details')
    list_filter = ('status', 'created_at', 'location')
    search_fields = ('name', 'mobile', 'email', 'location')
    readonly_fields = ('created_at',)

    # Helper to see if JSON data is saved
    def has_details(self, obj):
        return "✅ Yes" if obj.details and len(obj.details) > 5 else "❌ No"
    has_details.short_description = 'Data Saved?'

# 3. Kitchen Item Admin
@admin.register(KitchenItem)
class KitchenItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'kitchen_shape', 'unit_type', 'material', 'price')
    list_filter = ('kitchen_shape', 'unit_type', 'material')
    search_fields = ('name', 'specification')

# 4. Kitchen Accessory Admin
@admin.register(KitchenAccessory)
class KitchenAccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_type', 'material', 'price')
    list_filter = ('unit_type', 'material')
    search_fields = ('name', 'specification')

# 5. General Module Admin (Your requested code)
@admin.register(GeneralModule)
class GeneralModuleAdmin(admin.ModelAdmin):
    list_display = ('category', 'sub_type', 'material', 'length', 'height', 'price')
    list_filter = ('category', 'material')
    search_fields = ('category', 'specification', 'sub_type')
