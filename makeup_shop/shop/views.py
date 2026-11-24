from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# --- Product List ---
def product_list(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


# --- Product Detail ---
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})


# --- Session Key ---
def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


# --- Add to Cart ---
@require_POST
def cart_add(request, product_id):
    session_key = _get_session_key(request)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        session_key=session_key, product=product
    )
    item.quantity += 1
    item.save()
    return redirect('shop:cart_detail')


# --- Cart Detail ---
def cart_detail(request):
    session_key = _get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)
    cart_total = sum([item.line_total() for item in items])

    return render(request, 'shop/cart.html', {
        'cart_items': items,
        'cart_total': cart_total
    })


# --- Remove from Cart ---
@require_POST
def remove_from_cart(request, product_id):
    session_key = _get_session_key(request)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(session_key=session_key, product=product).delete()
    return redirect('shop:cart_detail')


# --- Checkout Page ---
def checkout(request):
    session_key = _get_session_key(request)
    items = CartItem.objects.filter(session_key=session_key)
    cart_total = sum([item.line_total() for item in items])

    return render(request, "shop/checkout.html", {
        "cart_items": items,
        "cart_total": cart_total
    })


# --- Order Confirmed Page ---
def order_confirmed(request):
    return render(request, "shop/order_confirmed.html")


# --- Login ---
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:product_list')
        else:
            messages.error(request, "Username ose password i gabuar!")

    return render(request, 'shop/login.html')


# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('shop:login')


# --- Edit Product ---
@login_required
def edit(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)

        price = request.POST.get('price')
        if price:
            try:
                product.price = float(price)
            except ValueError:
                pass

        category_id = request.POST.get('category')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            product.category = category

        product.available = 'available' in request.POST
        product.save()

        return redirect('shop:product_detail', slug=product.slug)

    categories = Category.objects.all()

    return render(request, 'shop/edit.html', {
        'product': product,
        'categories': categories
    })


# --- Delete Product ---
@login_required
@require_POST
def delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('shop:product_list')


