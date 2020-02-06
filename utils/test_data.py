class TestData:

    def get_cart_item(self):
        return {
            "product_id": 1,
            "quantity": 1,
            "variant": "M"
        }

    def get_checkout_payload(self):
        return {
            "shipping_address": {
                "name": "Test User",
                "street": "123 Test Lane",
                "city": "Kathmandu",
                "zip": "44600",
                "country": "NP"
            },
            "payment_method": "credit_card",
            "card_last4": "4242"
        }

    def get_new_user(self):
        return {
            "name": "QA Test User",
            "email": "qatest@rivia.com",
            "password": "QATest@123"
        }
# test data
