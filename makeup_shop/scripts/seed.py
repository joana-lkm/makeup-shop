
# Lightweight script to create sample categories and products.
# Run: python manage.py shell < scripts/seed.py
from shop.models import Category, Product
cat, _ = Category.objects.get_or_create(name='Lips', slug='lips')
Product.objects.get_or_create(category=cat, name='Matte Lipstick', slug='matte-lipstick', defaults={
    'description':'Rich matte lipstick with long-lasting pigment.',
    'price':9.99,
})
cat2, _ = Category.objects.get_or_create(name='Eyes', slug='eyes')
Product.objects.get_or_create(category=cat2, name='Mascara', slug='mascara', defaults={
    'description':'Volumizing mascara for dramatic lashes.',
    'price':12.50,
})
print('Sample products created.')
