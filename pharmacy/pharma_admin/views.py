from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Medicines, ProductItems, Ayurveda, Skincare
from django.shortcuts import get_object_or_404
from app.models import MyOrders

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin/admin_home.html')

# @user_passes_test(is_admin)
# def view_users(request):
#     # You can replace this with actual query like: users = CustomUser.objects.all()
#     context = {'users': []}
#     return render(request, 'admin_users.html', context)

@user_passes_test(is_admin)
def view_orders(request):
    # Fetch all orders from the database
    orders = MyOrders.objects.all()
    
    # Pass the orders to the template context
    context = {'orders': orders}
    
    return render(request, 'admin/admin_orders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        expiration = request.POST.get('expiration')

        # Create product based on category
        if category == 'medicines':
            Medicines.objects.create(medicine_name=name, medicine_image=image, medicine_price=price, medicine_descripton=description, medicine_exp=expiration)
        elif category == 'productitems':
            ProductItems.objects.create(prod_name=name, prod_image=image, prod_price=price, prod_descripton=description, prod_exp=expiration)
        elif category == 'ayurveda':
            Ayurveda.objects.create(med_name=name, med_image=image, med_price=price, med_descripton=description, med_exp=expiration)
        elif category == 'skincare':
            Skincare.objects.create(skinc_name=name, skinc_image=image, skinc_price=price, skinc_descripton=description, skinc_exp=expiration)

        return redirect('admin-manage-inventory')

    return render(request, 'admin/admin_add_product.html')

@user_passes_test(lambda u: u.is_superuser)
def manage_inventory(request):
    medicines = Medicines.objects.all()
    product_items = ProductItems.objects.all()
    ayurveda = Ayurveda.objects.all()
    skincare = Skincare.objects.all()

    return render(request, 'admin/admin_inventory.html', {
        'medicines': medicines,
        'product_items': product_items,
        'ayurveda': ayurveda,
        'skincare': skincare,
    })

@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id, category):
    if category == 'medicines':
        product = get_object_or_404(Medicines, id=product_id)
    elif category == 'productitems':
        product = get_object_or_404(ProductItems, id=product_id)
    elif category == 'ayurveda':
        product = get_object_or_404(Ayurveda, id=product_id)
    elif category == 'skincare':
        product = get_object_or_404(Skincare, id=product_id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.expiration = request.POST['expiration']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('admin-manage-inventory')

    return render(request, 'admin/admin_edit_product.html', {'product': product, 'category': category})

@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id, category):
    if category == 'medicines':
        product = get_object_or_404(Medicines, id=product_id)
    elif category == 'productitems':
        product = get_object_or_404(ProductItems, id=product_id)
    elif category == 'ayurveda':
        product = get_object_or_404(Ayurveda, id=product_id)
    elif category == 'skincare':
        product = get_object_or_404(Skincare, id=product_id)

    product.delete()
    return redirect('admin-manage-inventory')
