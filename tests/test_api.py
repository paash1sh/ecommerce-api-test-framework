import requests
import json
import unittest
from utils.api_client import APIClient
from utils.test_data import TestData


class CartAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.client.authenticate("testuser@rivia.com", "Test@123")
        cls.data = TestData()

    def test_add_item_to_cart(self):
        payload = self.data.get_cart_item()
        response = self.client.post("/api/cart/add", payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("cart_id", body)
        self.assertEqual(body["status"], "added")

    def test_get_cart_items(self):
        response = self.client.get("/api/cart")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body["items"], list)
        self.assertIn("total_price", body)

    def test_update_cart_quantity(self):
        cart_response = self.client.get("/api/cart")
        items = cart_response.json()["items"]
        if items:
            item_id = items[0]["id"]
            payload = {"quantity": 3}
            response = self.client.put(f"/api/cart/{item_id}", payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["quantity"], 3)

    def test_remove_item_from_cart(self):
        cart_response = self.client.get("/api/cart")
        items = cart_response.json()["items"]
        if items:
            item_id = items[0]["id"]
            response = self.client.delete(f"/api/cart/{item_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Item removed")

    def test_empty_cart(self):
        response = self.client.delete("/api/cart/clear")
        self.assertEqual(response.status_code, 200)
        verify = self.client.get("/api/cart")
        self.assertEqual(len(verify.json()["items"]), 0)


class CheckoutAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.client.authenticate("testuser@rivia.com", "Test@123")
        cls.data = TestData()

    def test_checkout_creates_order(self):
        # add item first
        cls_item = self.data.get_cart_item()
        self.client.post("/api/cart/add", cls_item)

        payload = self.data.get_checkout_payload()
        response = self.client.post("/api/checkout", payload)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertIn("order_id", body)
        self.assertEqual(body["status"], "pending")

    def test_checkout_missing_address_returns_400(self):
        payload = {"payment_method": "credit_card"}
        response = self.client.post("/api/checkout", payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_checkout_invalid_payment_method(self):
        payload = self.data.get_checkout_payload()
        payload["payment_method"] = "bitcoin"
        response = self.client.post("/api/checkout", payload)
        self.assertEqual(response.status_code, 422)


class ProductAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()

    def test_get_products_list(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body["products"], list)
        self.assertGreater(len(body["products"]), 0)

    def test_get_product_by_id(self):
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("name", body)
        self.assertIn("price", body)
        self.assertIn("stock", body)

    def test_get_nonexistent_product(self):
        response = self.client.get("/api/products/99999")
        self.assertEqual(response.status_code, 404)

    def test_product_search(self):
        response = self.client.get("/api/products?search=shirt")
        self.assertEqual(response.status_code, 200)
        products = response.json()["products"]
        for product in products:
            self.assertIn("shirt", product["name"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
# product tests
# cart tests
# checkout tests
# perf assert
