from django.test import TestCase, Client
from django.core.management import call_command

from mainapp.models import ProductCategory, Product

class TestMainAppTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(name='test1')
        product_1 = Product.objects.create(name='prod1_test', category=category)
        product_2 = Product.objects.create(name='prod2_test', category=category)

        self.client = Client()
    
    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)        

    def test_mainapp_shop(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)


    def tearDown(self):
        pass
