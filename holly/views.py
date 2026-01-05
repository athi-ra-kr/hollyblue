from django.shortcuts import render,redirect
from .import models

# Create your views here.
# def index(request):
#     return render(request,'index.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail  # Import for sending emails
import json

# IMPORT ALL YOUR MODELS
from .models import (
    Enquiry,
    EnquiryDetail,  # Make sure you have created this model in models.py
    FloorPlan,
    KitchenItem,
    KitchenAccessory,
    GeneralModule
)


# ==========================================
# 1. FRONTEND VIEWS
# ==========================================

def home(request):
    plans = FloorPlan.objects.all()
    return render(request, 'home.html', {'plans': plans})


def step2(request):
    """
    Loads ALL data needed for the frontend selection tool:
    1. Kitchen Items
    2. Kitchen Accessories
    3. General Modules (TV Unit, Wardrobe, etc.)
    """
    kitchen_items = list(KitchenItem.objects.all().values())
    accessories = list(KitchenAccessory.objects.all().values())
    modules = list(GeneralModule.objects.all().values())

    context = {
        'kitchen_items_json': json.dumps(kitchen_items, cls=DjangoJSONEncoder),
        'accessories_json': json.dumps(accessories, cls=DjangoJSONEncoder),
        'modules_json': json.dumps(modules, cls=DjangoJSONEncoder),
    }
    return render(request, 'step2.html', context)


# ==========================================
# 2. ADMIN PAGES
# ==========================================

def admin_login(request):
    return render(request, 'admin-login.html')


def admin_dashboard(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')
    return render(request, 'admin-dashboard.html', {
        'enquiries': enquiries,
        'total_enquiries': enquiries.count()
    })


def admin_floorplans(request):
    plans = FloorPlan.objects.all()
    return render(request, 'admin-floorplans.html', {'plans': plans})


def admin_kitchen(request):
    items = KitchenItem.objects.all()
    return render(request, 'admin-kitchen.html', {'items': items})


def admin_accessories(request):
    items = KitchenAccessory.objects.all()
    return render(request, 'admin-accessories.html', {'items': items})


def admin_modules(request, category):
    # Filters modules by category (e.g., 'TV Unit', 'Wardrobe')
    items = GeneralModule.objects.filter(category=category)
    return render(request, 'admin-modules.html', {
        'items': items,
        'category_name': category
    })


# ==========================================
# 3. FLOOR PLAN APIs
# ==========================================

@csrf_exempt
def add_floorplan(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name and image:
            FloorPlan.objects.create(name=name, image=image)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid data'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_floorplan(request, id):
    try:
        plan = FloorPlan.objects.get(id=id)
        plan.delete()
        return JsonResponse({'status': 'success'})
    except FloorPlan.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Plan not found'})


@csrf_exempt
def update_floorplan(request, id):
    if request.method == 'POST':
        try:
            plan = FloorPlan.objects.get(id=id)
            plan.name = request.POST.get('name', plan.name)
            if request.FILES.get('image'):
                plan.image = request.FILES.get('image')
            plan.save()
            return JsonResponse({'status': 'success'})
        except FloorPlan.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'})
    return JsonResponse({'status': 'error'})


# ==========================================
# 4. KITCHEN APIs
# ==========================================

@csrf_exempt
def add_kitchen(request):
    if request.method == 'POST':
        try:
            KitchenItem.objects.create(
                name=request.POST.get('name'),
                kitchen_shape=request.POST.get('kitchen_shape'),
                unit_type=request.POST.get('unit_type'),
                material=request.POST.get('material'),
                length=request.POST.get('length', 0),
                depth=request.POST.get('depth', 0),
                height=request.POST.get('height', 0),
                price=request.POST.get('price'),
                specification=request.POST.get('specification'),
                image=request.FILES.get('image')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_kitchen(request, id):
    try:
        KitchenItem.objects.get(id=id).delete()
        return JsonResponse({'status': 'success'})
    except KitchenItem.DoesNotExist:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def update_kitchen(request, id):
    if request.method == 'POST':
        try:
            item = KitchenItem.objects.get(id=id)
            item.name = request.POST.get('name', item.name)
            item.kitchen_shape = request.POST.get('kitchen_shape', item.kitchen_shape)
            item.unit_type = request.POST.get('unit_type', item.unit_type)
            item.material = request.POST.get('material', item.material)
            item.length = request.POST.get('length', item.length)
            item.depth = request.POST.get('depth', item.depth)
            item.height = request.POST.get('height', item.height)
            item.price = request.POST.get('price', item.price)
            item.specification = request.POST.get('specification', item.specification)

            if request.FILES.get('image'):
                item.image = request.FILES.get('image')

            item.save()
            return JsonResponse({'status': 'success'})
        except KitchenItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'})
    return JsonResponse({'status': 'error'})


# ==========================================
# 5. ACCESSORY APIs
# ==========================================

@csrf_exempt
def add_accessory(request):
    if request.method == 'POST':
        try:
            KitchenAccessory.objects.create(
                name=request.POST.get('name'),
                unit_type=request.POST.get('unit_type'),
                material=request.POST.get('material'),
                price=request.POST.get('price'),
                image=request.FILES.get('image'),
                length=request.POST.get('length', 0),
                depth=request.POST.get('depth', 0),
                height=request.POST.get('height', 0),
                specification=request.POST.get('specification', '')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_accessory(request, id):
    try:
        KitchenAccessory.objects.get(id=id).delete()
        return JsonResponse({'status': 'success'})
    except KitchenAccessory.DoesNotExist:
        return JsonResponse({'status': 'error'})


@csrf_exempt
def update_accessory(request, id):
    if request.method == 'POST':
        try:
            item = KitchenAccessory.objects.get(id=id)
            item.name = request.POST.get('name', item.name)
            item.unit_type = request.POST.get('unit_type', item.unit_type)
            item.material = request.POST.get('material', item.material)
            item.length = request.POST.get('length', item.length)
            item.depth = request.POST.get('depth', item.depth)
            item.height = request.POST.get('height', item.height)
            item.price = request.POST.get('price', item.price)
            item.specification = request.POST.get('specification', item.specification)

            if request.FILES.get('image'):
                item.image = request.FILES.get('image')

            item.save()
            return JsonResponse({'status': 'success'})
        except KitchenAccessory.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'})
    return JsonResponse({'status': 'error'})


# ==========================================
# 6. GENERAL MODULE APIs (TV Unit, Wardrobe, etc.)
# ==========================================

@csrf_exempt
def add_module(request):
    if request.method == 'POST':
        try:
            module = GeneralModule.objects.create(
                category=request.POST.get('category'),
                sub_type=request.POST.get('sub_type', ''),
                material=request.POST.get('material'),
                length=request.POST.get('length', 0),
                depth=request.POST.get('depth', 0),
                height=request.POST.get('height', 0),
                price=request.POST.get('price'),
                specification=request.POST.get('specification', ''),
                image=request.FILES.get('image')
            )
            return JsonResponse({'status': 'success', 'id': module.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_module(request, id):
    try:
        GeneralModule.objects.get(id=id).delete()
        return JsonResponse({'status': 'success'})
    except GeneralModule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'})


@csrf_exempt
def update_module(request, id):
    if request.method == 'POST':
        try:
            item = GeneralModule.objects.get(id=id)
            item.sub_type = request.POST.get('sub_type', item.sub_type)
            item.material = request.POST.get('material', item.material)
            item.length = request.POST.get('length', item.length)
            item.depth = request.POST.get('depth', item.depth)
            item.height = request.POST.get('height', item.height)
            item.price = request.POST.get('price', item.price)
            item.specification = request.POST.get('specification', item.specification)

            if request.FILES.get('image'):
                item.image = request.FILES.get('image')

            item.save()
            return JsonResponse({'status': 'success'})
        except GeneralModule.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Not found'})
    return JsonResponse({'status': 'error'})


# ==========================================
# 7. ENQUIRY APIs (UPDATED)
# ==========================================

@csrf_exempt
def submit_enquiry(request):
    """
    Saves the main enquiry info AND saves individual items
    into the EnquiryDetail table.
    Sends email notification.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 1. Create the Main Enquiry Record
            enquiry = Enquiry.objects.create(
                name=data.get('name'),
                email=data.get('email', ''),
                mobile=data.get('mobile'),
                location=data.get('location'),
                sqft=data.get('sqft', ''),
                status=data.get('status', ''),  # Matches 'status_type' in your snippet
                total_amount=str(data.get('total_amount', '')).replace('₹', '').replace(',', '').strip()
            )

            # 2. Save Each Item in the Cart to EnquiryDetail Table
            cart_items = data.get('details', [])

            for item in cart_items:
                EnquiryDetail.objects.create(
                    enquiry=enquiry,
                    category=item.get('category', 'General'),
                    item_name=item.get('title', 'Unknown Item'),
                    material=item.get('material', ''),
                    size=item.get('size', ''),
                    price=item.get('price', 0)
                )

            # =====================================================
            # 3. SEND EMAIL NOTIFICATION
            # =====================================================
            try:
                send_mail(
                    'New Enquiry Received - HollyBlue',
                    f'Client: {data.get("name")}\nMobile: {data.get("mobile")}\nAmount: {data.get("total_amount")}',
                    'your-email@gmail.com',  # REPLACE with your sender email (must match settings.py)
                    ['admin@hollyblue.com'],  # REPLACE with the admin's email address
                    fail_silently=True,  # Set to True so email errors don't crash the enquiry
                )
            except Exception as e:
                print("Email sending failed:", e)

            return JsonResponse({'status': 'success', 'message': 'Enquiry Saved!', 'enquiry_id': enquiry.id})
        except Exception as e:
            print("Enquiry Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid Method'}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_enquiry(request, id):
    try:
        enquiry = Enquiry.objects.get(id=id)
        enquiry.delete()
        # Cascading delete will automatically remove related EnquiryDetails
        return JsonResponse({'status': 'success', 'message': 'Deleted successfully'})
    except Enquiry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Enquiry not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def update_enquiry(request, id):
    try:
        data = json.loads(request.body)
        enquiry = Enquiry.objects.get(id=id)
        enquiry.name = data.get('name', enquiry.name)
        enquiry.mobile = data.get('mobile', enquiry.mobile)
        enquiry.location = data.get('location', enquiry.location)
        enquiry.status = data.get('status', enquiry.status)
        enquiry.total_amount = data.get('total_amount', enquiry.total_amount)
        enquiry.save()
        return JsonResponse({'status': 'success', 'message': 'Updated successfully'})
    except Enquiry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)


def enquiry_invoice(request, id):
    # Generates the Invoice / PDF View
    enquiry = get_object_or_404(Enquiry, id=id)

    # Fetch related details using the reverse relationship
    # (Assuming EnquiryDetail has a ForeignKey to Enquiry with related_name='details' or default set)
    cart_items = EnquiryDetail.objects.filter(enquiry=enquiry)

    context = {
        'enq': enquiry,
        'cart_items': cart_items
    }
    return render(request, 'invoice.html', context)