from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Category, Product

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        """Prueba la creación de una nueva categoría en la base de datos"""
        category = Category.objects.create(name='Ropa')
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(category.name, 'Ropa')

    def test_list_categories(self):
        """Prueba verificar la existencia de categorías en la base de datos"""
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 1)
        self.assertEqual(categories[0].name, 'Electronica')


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        """Prueba la creación exitosa de un producto asociado a una categoría"""
        response = self.client.post('/products/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00
        })
        self.assertEqual(response.status_code, 201)

    def test_list_products(self):
        """Prueba la obtención del listado de productos"""
        response = self.client.get('/products/products/')
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        """Prueba la actualización de los datos de un producto existente"""
        response = self.client.put(f'/products/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        """Prueba la eliminación de un producto de la base de datos"""
        response = self.client.delete(f'/products/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    # Pruebas para el nuevo endpoint del Patrón Facade (/precio-final/)
    def test_precio_final_authenticated(self):
        """Prueba que el endpoint /precio-final/ devuelva 200 con token JWT (autenticado)"""
        response = self.client.get(f'/products/precio-final/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('final_price_with_discount', response.data)

    def test_precio_final_unauthorized(self):
        """Prueba que el endpoint /precio-final/ rechace el acceso con 401 si no hay token"""
        self.client.force_authenticate(user=None)  # Quitamos la autenticación
        response = self.client.get(f'/products/precio-final/{self.product.id}/')
        self.assertEqual(response.status_code, 401)