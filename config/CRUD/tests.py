from django.test import TestCase
from .models import Product

# Create your tests here.
class CreateProductTests(TestCase):
    @classmethod
    def setUpClass(self):       # setUpClass is called once at the beginning of the test run (setUp is called before each test)
        self.products = []
    
    @classmethod
    def tearDownClass(self):         # tearDown is called once at the end of the test run (tearDownClass is called after each test)
        for product in self.products:
            product.delete()
    
    def testCreateBasicProduct(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg"
        }
        self.products.append(Product.objects.create(name = newProductDetails["name"], price = newProductDetails["price"], stock = newProductDetails["stock"], image_url = newProductDetails["image_url"]))
        self.assertEqual(Product.objects.get(name = newProductDetails["name"]).name, newProductDetails["name"])


class ReadProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.product = Product.objects.create(name = "TestProduct", price = 10.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
        
    @classmethod
    def tearDownClass(self):
        self.product.delete()
        
    def testReadBasicProduct(self):
        self.assertEqual(Product.objects.get(id = self.product.id).name, "TestProduct")
        self.assertEqual(Product.objects.get(id = self.product.id).price, 10.0)
        self.assertEqual(Product.objects.get(id = self.product.id).stock, 10)
        self.assertEqual(Product.objects.get(id = self.product.id).image_url, "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
      
        
class UpdateProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.product = Product.objects.create(name = "TestProduct", price = 10.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
        
    @classmethod
    def tearDownClass(self):
        self.product.delete()
        
    def testUpdateBasicProduct(self):
        self.product.name = "NewTestProduct"
        self.product.price = 20.0
        self.product.stock = 20
        self.product.image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg"
        self.product.save()
        self.assertEqual(Product.objects.get(name = "NewTestProduct").name, "NewTestProduct")
        self.assertEqual(Product.objects.get(name = "NewTestProduct").price, 20.0)
        self.assertEqual(Product.objects.get(name = "NewTestProduct").stock, 20)
        self.assertEqual(Product.objects.get(name = "NewTestProduct").image_url, "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
        
class DeleteProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.product = Product.objects.create(name = "TestProduct", price = 10.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
        
    @classmethod
    def tearDownClass(self):
        try:
            self.product.delete()
        except:
            pass
    
    def testDeleteBasicProduct(self):
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id = self.product.id)