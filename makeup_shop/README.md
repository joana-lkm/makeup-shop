
# Makeup Shop (Django)

This is a starter Django project named **makeup_shop** modeled as a small e-commerce site for cosmetics.

## What's included
- Django project and `shop` app
- Models: Category, Product, CartItem
- Templates: product list, product detail, cart
- Admin registration for models
- Simple DRF API endpoints for products and categories
- Static CSS and media setup
- `requirements.txt`

## Run locally (recommended steps)
1. Create a virtualenv and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser to access admin:
   ```bash
   python manage.py createsuperuser
   ```
4. Run the dev server:
   ```bash
   python manage.py runserver
   ```

Then open http://127.0.0.1:8000/ (or in PyCharm run the project).

