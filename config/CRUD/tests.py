from django.test import TestCase
from .models import Product, Category, Promotion

# Create your tests here.
class CreateProductTests(TestCase):
    @classmethod
    def setUpClass(self):       # setUpClass is called once at the beginning of the test run (setUp is called before each test)
        self.products = []
        self.category = Category.objects.create(name = "DefaultCategory", description = "DefaultDescription")
    
    @classmethod
    def tearDownClass(self):         # tearDown is called once at the end of the test run (tearDownClass is called after each test)
        for product in self.products:
            product.delete()
    
    def testCreateBasicProduct(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg",
            "category": self.category
        }
        self.products.append(Product.objects.create(name = newProductDetails["name"], price = newProductDetails["price"], stock = newProductDetails["stock"], image_url = newProductDetails["image_url"], category=newProductDetails["category"]))
        self.assertEqual(Product.objects.get(name = newProductDetails["name"]).name, newProductDetails["name"])
        
    def testCreateProductWithCategory(self):
        newCategoryDetails = {
            "name": "TestCategory",
            "description": "TestDescription"
        }
        category = Category.objects.create(name = newCategoryDetails["name"], description = newCategoryDetails["description"])
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg",
            "category": category
        }
        self.products.append(Product.objects.create(name = newProductDetails["name"], price = newProductDetails["price"], stock = newProductDetails["stock"], image_url = newProductDetails["image_url"], category = newProductDetails["category"]))
        self.assertEqual(Product.objects.get(name = newProductDetails["name"]).category.name, category.name)
        # teardown
        category.delete()
        
    def testCreateProductWithPromotion(self):
        newPromotionDetails = {
            "name": "TestPromotion",
            "description": "TestDescription",
            "discount": 0.5
        }
        promotion = Promotion.objects.create(name = newPromotionDetails["name"], description = newPromotionDetails["description"], discount = newPromotionDetails["discount"])
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg",
            "promotion": promotion,
            "category": self.category
        }
        self.products.append(Product.objects.create(name = newProductDetails["name"], price = newProductDetails["price"], stock = newProductDetails["stock"], image_url = newProductDetails["image_url"], promotion = newProductDetails["promotion"], category = newProductDetails["category"]))
        self.assertEqual(Product.objects.get(name = newProductDetails["name"]).promotion.name, promotion.name)
        # teardown
        promotion.delete()
        
        


class ReadProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.category = Category.objects.create(name = "TestCategory", description = "TestCategoryDescription")
        self.promotion = Promotion.objects.create(name = "TestPromotion", description = "TestPromotionDescription", discount = 10.0)
        self.product1 = Product.objects.create(name = "TestProduct1", price = 10.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg", description = "TestProduct1Description", category = self.category, promotion = self.promotion)
        self.product2 = Product.objects.create(name = "TestProduct2", price = 20.0, stock = 20, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg", description = "TestProduct2Description", category = self.category, promotion = self.promotion)
        self.product3 = Product.objects.create(name = "TestProduct3", price = 20.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg", description = "TestProduct3Description", category = self.category, promotion = self.promotion)

    @classmethod
    def tearDownClass(self):
        self.category.delete()
        self.promotion.delete()
        self.product1.delete()
        self.product2.delete()
        self.product3.delete()

    def testReadBasicCategory(self):
        self.assertEqual(Category.objects.get(id = self.category.id).name, "TestCategory")
        self.assertEqual(Category.objects.get(id = self.category.id).description, "TestCategoryDescription")

    def testReadBasicPromotion(self):
        self.assertEqual(Promotion.objects.get(id = self.promotion.id).name, "TestPromotion")
        self.assertEqual(Promotion.objects.get(id = self.promotion.id).description, "TestPromotionDescription")
        self.assertEqual(Promotion.objects.get(id = self.promotion.id).discount, 10.0)

    def testReadBasicProduct(self):
        self.assertEqual(Product.objects.get(id = self.product1.id).name, "TestProduct1")
        self.assertEqual(Product.objects.get(id = self.product1.id).price, 10.0)
        self.assertEqual(Product.objects.get(id = self.product1.id).stock, 10)
        self.assertEqual(Product.objects.get(id = self.product1.id).image_url, "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg")
        self.assertEqual(Product.objects.get(id = self.product1.id).description, "TestProduct1Description")

    def testReadPromotionAndCategory(self):
        self.assertEqual(self.product1.promotion, self.promotion)
        self.assertEqual(self.product1.category, self.category)

    def testReadNonexistentCategory(self):
        nonExistentCategoryId = 999
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id = nonExistentCategoryId)
    
    def testReadNonexistentPromotion(self):
        nonExistentPromotionId = 999
        with self.assertRaises(Promotion.DoesNotExist):
            Promotion.objects.get(id = nonExistentPromotionId)

    def testReadNonexistentProduct(self):
        nonExistentProductId = 999  
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id = nonExistentProductId)

    def testReadProductPromotionManyToManyRelationship(self):
        self.promotion.products.add(self.product1, self.product2, self.product3)
        productsInPromotion = self.promotion.products.all()

        self.assertEqual(len(productsInPromotion), 3)
        self.assertIn(self.product1, productsInPromotion)
        self.assertIn(self.product2, productsInPromotion)
        self.assertIn(self.product3, productsInPromotion)

    def testReadPromotionProductManyToManyRelationship(self):
        self.assertEqual(self.product1.promotion, self.promotion)
        self.assertEqual(self.product2.promotion, self.promotion)
        self.assertEqual(self.product3.promotion, self.promotion)

    def testReadProductPromotionRelationship(self):
        promotion = Product.objects.get(id=self.product1.id).promotion
        self.assertEqual(promotion, self.promotion)

    def testReadProductCategoryRelationship(self):
        category = Product.objects.get(id=self.product1.id).category
        self.assertEqual(category, self.category)

    def testReadFilterProductsByPrice(self):
        filteredProducts = Product.objects.all().filter(price = 20.0)
        self.assertEqual(len(filteredProducts), 2)
        self.assertIn(self.product2, filteredProducts)
        self.assertIn(self.product3, filteredProducts)  
        
    def testReadFilterProductsByStock(self):
        filteredProducts = Product.objects.all().filter(stock = 10)
        self.assertEqual(len(filteredProducts), 2)
        self.assertIn(self.product1, filteredProducts)
        self.assertIn(self.product3, filteredProducts)  

    def testReadSortedProductsByName(self):
        sortedProducts = Product.objects.order_by('name')
        self.assertEqual(list(sortedProducts), [self.product1, self.product2, self.product3])

    def testReadAllProducts(self):
        allProducts = Product.objects.values_list('name', flat=True).order_by('name')

        expectedProducts = [
            "TestProduct1",
            "TestProduct2",
            "TestProduct3",
        ]
        
        self.assertQuerysetEqual(allProducts, expectedProducts, transform = str)
        


class UpdateProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.category = Category.objects.create(name = "TestCategory", description = "TestDescription")
        self.product = Product.objects.create(name = "TestProduct", price = 10.0, stock = 10, image_url = "https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?cs=srgb&dl=pexels-math-90946.jpg&fm=jpg", category=self.category)

    @classmethod
    def tearDownClass(self):
        try:
            self.product.delete()
        except:
            pass
        try:
            self.category.delete()
        except:
            pass

    def testUpdateBasicProduct(self):
        updatedProductDetails = {
            "name": "UpdatedTestProduct",
            "price": 20.0,
            "stock": 20,
            "image_url": "https://upload.wikimedia.org/wikipedia/en/e/ea/TwinPeaks_openingshotcredits.jpg"
        }
        self.product.name = updatedProductDetails["name"]
        self.product.price = updatedProductDetails["price"]
        self.product.stock = updatedProductDetails["stock"]
        self.product.image_url = updatedProductDetails["image_url"]
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).name, updatedProductDetails["name"])
        self.assertEqual(Product.objects.get(id = self.product.id).price, updatedProductDetails["price"])
        self.assertEqual(Product.objects.get(id = self.product.id).stock, updatedProductDetails["stock"])
        self.assertEqual(Product.objects.get(id = self.product.id).image_url, updatedProductDetails["image_url"])

    def testUpdateProductCategory(self):
        newCategoryDetails = {
            "name": "NewTestCategory",
            "description": "NewTestDescription"
        }
        category = Category.objects.create(name = newCategoryDetails["name"], description = newCategoryDetails["description"])
        self.product.category = category
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).category.name, newCategoryDetails["name"])
        self.assertEqual(Product.objects.get(id = self.product.id).category.description, newCategoryDetails["description"])
        # teardown
        category.delete()

    def testUpdateProductCategoryManyToManyRelationship(self):
        newCategoryDetails = {
            "name": "NewTestCategory",
            "description": "NewTestDescription"
        }
        category = Category.objects.create(name = newCategoryDetails["name"], description = newCategoryDetails["description"])
        self.product.category = category
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).category.name, newCategoryDetails["name"])
        self.assertEqual(Product.objects.get(id = self.product.id).category.description, newCategoryDetails["description"])
        # teardown
        category.delete()

    def testUpdateNonexistentProduct(self):
        nonExistentProductId = 999

        with self.assertRaises(Product.DoesNotExist):
            product = Product.objects.get(id=nonExistentProductId)
            product.name = "Nowa nazwa"
            product.save()

    def testUpdateProductWithInvalidData(self):
        invalidProductDetails = {
            "name": "",
            "price": -10.0,
            "stock": -10,
            "image_url": ""
        }
        self.product.name = invalidProductDetails["name"]
        self.product.price = invalidProductDetails["price"]
        self.product.stock = invalidProductDetails["stock"]
        self.product.image_url = invalidProductDetails["image_url"]
        with self.assertRaises(Exception):
            self.product.save()
        self.assertNotEqual(Product.objects.get(id = self.product.id).name, invalidProductDetails["name"])
        self.assertNotEqual(Product.objects.get(id = self.product.id).price, invalidProductDetails["price"])
        self.assertNotEqual(Product.objects.get(id = self.product.id).stock, invalidProductDetails["stock"])
        self.assertNotEqual(Product.objects.get(id = self.product.id).image_url, invalidProductDetails["image_url"])
        
        
class DeleteProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.category = Category.objects.create(name="Test Category", description="This is a test category.")
        self.promotion = Promotion.objects.create(name="Test Promotion", description="This is a test promotion.", discount=10.0)
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10,
            description="This is a test product.",
            category=self.category,
            promotion=self.promotion
        )
        self.product.save()
        self.category.save()
        self.promotion.save()
    @classmethod
    def tearDownClass(self):
        try:
            self.product.delete()
            self.product2.delete()
        except:
            pass
        try:
            self.category.delete()
            self.category2.delete()
        except:
            pass
        try:
            self.promotion.delete()
            self.promotion2.delete()
        except:
            pass

    
    def testDeleteBasicProduct(self):
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id = self.product.id)


    def testDeleteCategoryCascadesToProduct(self):
        self.category.delete()

        with self.assertRaises(Product.DoesNotExist):
            product = Product.objects.get(id=self.product.id)

    def testDeletePromotionSetsProductPromotionToNull(self):
        self.setUpClass()
        self.product.promotion = self.promotion
        self.category.save()
        self.product.save()

        self.promotion.delete()

        self.product.refresh_from_db()

        self.assertIsNone(self.product.promotion)

    def testDeleteProductDoesNotDeletePromotion(self):
        self.setUpClass()
        self.product.delete()

        promotion = Promotion.objects.get(id=self.promotion.id)
        self.assertIsNotNone(promotion)

    def testDeletePromotionDoesNotDeleteRelatedProducts(self):
        self.setUpClass()
        self.promotion.delete()

        product = Product.objects.get(id=self.product.id)
        self.assertIsNotNone(product)

    def testDeleteCategoryDoesNotAffectUnrelatedProducts(self):
        self.setUpClass()
        self.category2 = Category.objects.create(name="Test Category", description="This is a another test category.")
        self.product2 = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10,
            description="This is a test product.",
            category=self.category2,
            promotion=self.promotion
        )

        self.category.delete()
        self.product2.save()

        product2_after = Product.objects.get(id=self.product2.id)
        self.assertIsNotNone(product2_after)

        try:
            self.category2.delete()
        except:
            pass

        try:
            self.product2.delete()
        except:
            pass

    def testDeletePromotionDoesNotAffectProductsWithoutPromotion(self):
        self.setUpClass()
        self.product2 = Product.objects.create(
            name="Test Product",
            price=100.0,
            stock=10,
            description="This is a test product.",
            category=self.category
        )

        self.promotion.delete()

        self.product2.refresh_from_db()
        try:
            product_after = Product.objects.get(id=self.product2.id)
            self.assertIsNotNone(product_after)
        except Product.DoesNotExist:
            self.fail("Product without promotion was deleted.")