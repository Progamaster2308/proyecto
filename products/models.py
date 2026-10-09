from django.db import models

# Modelo de Categorias
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

# Modelo de productos
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='get_products', verbose_name='Categoria')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def crear_con_categoria_default(cls, name, price, description=""):
        """Factory Method para instanciar un producto con una categoría por defecto ('General')"""
        default_category, created = Category.objects.get_or_create(name='General')
        return cls.objects.create(
            name=name,
            category=default_category,
            description=description,
            price=price
        )