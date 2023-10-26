import unittest

from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from .models import Product, Category, Promotion

class CreateProductTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.products = []
        newCategoryDetails = {
            "name": "TestCategory",
            "description": "TestDescription"
        }
        self.category = Category.objects.create(**newCategoryDetails)

        newPromotionDetails = {
            "name": "TestPromotion",
            "description": "TestDescription",
            "discount": 33.33
        }
        self.promotion = Promotion.objects.create(**newPromotionDetails)

    @classmethod
    def tearDownClass(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Promotion.objects.all().delete()

    def testCreateProductWithoutNameShouldRaiseException(self):
        newProductDetails = {
            "name": None,
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        with self.assertRaises(ValidationError):
            Product.objects.create(**newProductDetails)

    def testCreateProductWithoutPriceShouldRaiseException(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": None,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        with self.assertRaises(ValidationError):
            Product.objects.create(**newProductDetails)

    def testCreateProductWithoutStockShouldRaiseException(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": None,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        with self.assertRaises(ValidationError):
            Product.objects.create(**newProductDetails)

    def testCreateProductWithoutCategoryShouldRaiseException(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": None
        }

        with self.assertRaises(Category.DoesNotExist):
            Product.objects.create(**newProductDetails)

    def testCreateCategoryWithoutNameShouldRaiseException(self):
        newCategoryDetails = {
            "name": None,
            "description": "TestDescriptionNoName"
        }

        with self.assertRaises(ValidationError):
            Category.objects.create(**newCategoryDetails)

    def testCreatePromotionWithoutNameShouldRaiseException(self):
        newPromotionDetails = {
            "name": None,
            "description": "TestDescription",
            "discount": 12.2
        }

        with self.assertRaises(ValidationError):
            Promotion.objects.create(**newPromotionDetails)

    def testCreatePromotionWithoutDiscountShouldRaiseException(self):
        newPromotionDetails = {
            "name": "TestName",
            "description": "TestDescription",
            "discount": None
        }

        with self.assertRaises(ValidationError):
            Promotion.objects.create(**newPromotionDetails)

    def testCreatePromotionWhenInvalidDiscountShouldRaiseException(self):
        newPromotionDetails = {
            "name": "TestName",
            "description": "TestDescription",
            "discount": -10
        }

        with self.assertRaises(ValidationError):
            Promotion.objects.create(**newPromotionDetails)
            
    def testCreateProductWithoutPromotionIdShouldCorrectlyCreate(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": None,
            "category_id": self.category.id
        }

        created_product = Product.objects.create(**newProductDetails)

        expected_product = Product.objects.get(name=newProductDetails["name"])
        for field in newProductDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))
            
    def testCreatePromotionWithoutDescriptionShouldCorrectlyCreate(self):
        newPromotionDetails = {
            "name": "TestNameNoDescription",
            "description": None,
            "discount": 12.2
        }
        created_product = Promotion.objects.create(**newPromotionDetails)
        
        expected_product = Promotion.objects.get(name=newPromotionDetails["name"])
        for field in newPromotionDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))
            
    def testCreateProductWithoutImageUrlShouldCorrectlyCreate(self):
        newProductDetails = {
            "name": "TestProductNoImageURL",
            "price": 10.0,
            "stock": 10,
            "image_url": None,
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }
        created_product = Product.objects.create(**newProductDetails)
        
        expected_product = Product.objects.get(name=newProductDetails["name"])
        for field in newProductDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))

    def testCreateCategoryWithoutDescriptionShouldCorrectlyCreate(self):
        newCategoryDetails = {
            "name": "TestCategoryNoDescription",
            "description": None
        }
        created_category = Category.objects.create(**newCategoryDetails)
        
        expected_category = Category.objects.get(name=newCategoryDetails["name"])
        for field in newCategoryDetails:
            self.assertEqual(getattr(created_category, field), getattr(expected_category, field))
            
    def testCreateProductWithoutDescriptionCorrectlyCreate(self):
        newProductDetails = {
            "name": "TestProductNoDescription",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": None,
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }
        created_product = Product.objects.create(**newProductDetails)
        
        expected_product = Product.objects.get(name=newProductDetails["name"])
        for field in newProductDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))

    def testCreateValidProduct(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        created_product = Product.objects.create(**newProductDetails)

        expected_product = Product.objects.get(name=newProductDetails["name"])
        for field in newProductDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))

    def testCreateValidCategory(self):
        newCategoryDetails = {
            "name": "TestCategory1",
            "description": "TestDescription"
        }

        created_product = Category.objects.create(**newCategoryDetails)

        expected_product = Category.objects.get(name=newCategoryDetails["name"])
        for field in newCategoryDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))

    def testCreateValidPromotion(self):
        newPromotionDetails = {
            "name": "TestPromotion1",
            "description": "TestDescription",
            "discount": 33.33
        }
        created_product = Promotion.objects.create(**newPromotionDetails)

        expected_product = Promotion.objects.get(name=newPromotionDetails["name"])
        for field in newPromotionDetails:
            self.assertEqual(getattr(created_product, field), getattr(expected_product, field))


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
        Product.objects.all().delete()
        Category.objects.all().delete()
        Promotion.objects.all().delete()

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
        Product.objects.all().delete()
        Category.objects.all().delete()
        Promotion.objects.all().delete()

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

    def testUpdatePromotion(self):
        self.promotion = Promotion.objects.create(name="Test Promotion", description="This is a test promotion.", discount=10.0)
        self.product.promotion = self.promotion
        self.product.name = "test name"
        self.product.price = 10
        category = Category.objects.create(name="Test Category")
        self.product.category = category
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).promotion, self.promotion)
        self.promotion.delete()

    def testUpdatePromotionManyToManyRelationship(self):
        self.promotion = Promotion.objects.create(name="Test Promotion", description="This is a test promotion.", discount=10.0)
        self.product.promotion = self.promotion
        self.product.name = "test name"
        self.product.price = 10
        category = Category.objects.create(name="Test Category")
        self.product.category = category
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).promotion, self.promotion)
        self.promotion.delete()

    def testUpdatePromotionToNull(self):
        self.product.promotion = None
        self.product.name = "test name"
        self.product.price = 10
        category = Category.objects.create(name="Test Category")
        self.product.category = category
        self.product.save()
        self.assertIsNone(Product.objects.get(id = self.product.id).promotion)

    def testUpdatePromotionToNullManyToManyRelationship(self):
        self.product.promotion = None
        self.product.name = "test name"
        self.product.price = 10
        category = Category.objects.create(name="Test Category")
        self.product.category = category
        self.product.save()
        self.assertIsNone(Product.objects.get(id = self.product.id).promotion)

    def testUpdatePromotionToNonExistentPromotion(self):
        nonExistentPromotionId = 999
        with self.assertRaises(Promotion.DoesNotExist):
            self.product.promotion = Promotion.objects.get(id = nonExistentPromotionId)
            self.product.save()

    def testUpdatePromotionToNonExistentPromotionManyToManyRelationship(self):
        nonExistentPromotionId = 999
        with self.assertRaises(Promotion.DoesNotExist):
            self.product.promotion = Promotion.objects.get(id = nonExistentPromotionId)
            self.product.save()


    def testUpdateCategoryManyToManyRelationship(self):
        self.category = Category.objects.create(name="Test Category", description="This is a test category.")
        self.product.category = self.category
        self.product.name = "test name"
        self.product.price = 10
        self.product.save()
        self.assertEqual(Product.objects.get(id = self.product.id).category, self.category)
        self.category.delete()


    def testUpdateCategoryToNullManyToManyRelationship(self):
        self.product.name = "test name"
        self.product.price = 10
        self.product.category = None

class DeleteProductTests(TestCase):
    @classmethod
    def setUp(self):
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
        
    @classmethod
    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Promotion.objects.all().delete()

    def test_delete_category(self):
        self.category.delete()
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category.id)

    def test_delete_non_existent_category(self):
        with self.assertRaises(Category.DoesNotExist):
            non_existent_category = Category.objects.get(id=9999)
            non_existent_category.delete()

    def test_delete_promotion(self):
        self.setUpClass()
        self.promotion.delete()
        with self.assertRaises(Promotion.DoesNotExist):
            Promotion.objects.get(id=self.promotion.id)

    def test_delete_non_existent_promotion(self):
        with self.assertRaises(Promotion.DoesNotExist):
            non_existent_promotion = Promotion.objects.get(id=9999)
            non_existent_promotion.delete()

    def test_delete_product(self):
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

    def test_delete_non_existent_product(self):
        with self.assertRaises(Product.DoesNotExist):
            non_existent_product = Product.objects.get(id=9999)
            non_existent_product.delete()

    def testDeleteCategoryCascadesToProduct(self):
        self.category.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

    def testDeletePromotionSetsProductPromotionToNull(self):
        self.product.promotion = self.promotion
        self.category.save()
        self.product.save()

        self.promotion.delete()

        self.product.refresh_from_db()

        self.assertIsNone(self.product.promotion)

    def testDeleteProductDoesNotDeletePromotion(self):
        self.product.delete()

        promotion = Promotion.objects.get(id=self.promotion.id)
        self.assertIsNotNone(promotion)

    def testDeletePromotionDoesNotDeleteRelatedProducts(self):
        self.promotion.delete()

        product = Product.objects.get(id=self.product.id)
        self.assertIsNotNone(product)

    def testDeleteCategoryDoesNotAffectUnrelatedProducts(self):
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

    def testDeletePromotionDoesNotAffectProductsWithoutPromotion(self):
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

