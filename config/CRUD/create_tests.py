import unittest

from django.db.utils import IntegrityError
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
        for product in self.products:
            product.delete()
        self.category.delete()
        self.promotion.delete()

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

        with self.assertRaises(IntegrityError):
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

        with self.assertRaises(IntegrityError):
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

        with self.assertRaises(IntegrityError):
            Product.objects.create(**newProductDetails)

    def testCreateProductWithoutImageUrlShouldRaiseException(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": None,
            "description": "TestDescription",
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        with self.assertRaises(IntegrityError):
            Product.objects.create(**newProductDetails)

    def testCreateProductWithoutDescriptionShouldRaiseException(self):
        newProductDetails = {
            "name": "TestProduct",
            "price": 10.0,
            "stock": 10,
            "image_url": "https://example.pl/img=2137",
            "description": None,
            "promotion_id": self.promotion.id,
            "category_id": self.category.id
        }

        with self.assertRaises(IntegrityError):
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

        with self.assertRaises(IntegrityError):
            Product.objects.create(**newProductDetails)

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

    def testCreateCategoryWithoutNameShouldRaiseException(self):
        newCategoryDetails = {
            "name": None,
            "description": "TestDescription"
        }

        with self.assertRaises(IntegrityError):
            Category.objects.create(**newCategoryDetails)

    def testCreateCategoryWithoutDescriptionShouldRaiseException(self):
        newCategoryDetails = {
            "name": "TestCategory",
            "description": None
        }

        with self.assertRaises(IntegrityError):
            Category.objects.create(**newCategoryDetails)

    def testCreatePromotionWithoutNameShouldRaiseException(self):
        newPromotionDetails = {
            "name": None,
            "description": "TestDescription",
            "discount": 12.2
        }

        with self.assertRaises(IntegrityError):
            Promotion.objects.create(**newPromotionDetails)

    def testCreatePromotionWithoutDescriptionShouldRaiseException(self):
        newPromotionDetails = {
            "name": "TestName",
            "description": None,
            "discount": 12.2
        }

        with self.assertRaises(IntegrityError):
            Promotion.objects.create(**newPromotionDetails)

    def testCreatePromotionWithoutDiscountShouldRaiseException(self):
        newPromotionDetails = {
            "name": "TestName",
            "description": "TestDescription",
            "discount": None
        }

        with self.assertRaises(IntegrityError):
            Promotion.objects.create(**newPromotionDetails)

    @unittest.skip('todo: walidacja ujemnych liczb')
    def testCreatePromotionWhenInvalidDiscountShouldRaiseException(self):
        newPromotionDetails = {
            "name": "TestName",
            "description": "TestDescription",
            "discount": -10
        }

        with self.assertRaises(IntegrityError):
            Promotion.objects.create(**newPromotionDetails)

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
