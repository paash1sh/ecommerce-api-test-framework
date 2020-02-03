# ecommerce-api-test-framework

API test framework for an e-commerce platform covering product catalog, cart operations, checkout flow, and order management. Built with Python `requests` and `unittest`, with Postman collections for manual/exploratory testing.

## Tech Stack

- Python 3.6
- requests 2.23.0
- unittest (stdlib)
- Postman v7 collections

## Test Coverage

| Endpoint | Tests |
|----------|-------|
| `POST /api/auth/login` | Valid login, token returned |
| `GET /api/products` | List products, search |
| `GET /api/products/:id` | Valid ID, 404 on missing |
| `POST /api/cart/add` | Add item, validate response |
| `GET /api/cart` | Get items, total price |
| `PUT /api/cart/:id` | Update quantity |
| `DELETE /api/cart/:id` | Remove item |
| `POST /api/checkout` | Create order, missing address 400, invalid payment 422 |

## Setup

```bash
pip install -r requirements.txt
export BASE_URL=http://ecommerce.rivia.internal
```

## Running Tests

```bash
# All tests
python -m unittest discover tests/

# Specific module
python -m unittest tests.test_api.CartAPITest
```

## Postman

Import `collections/ecommerce_api.postman_collection.json` into Postman. Set the `base_url` and `token` environment variables before running.

## Structure

```
tests/           # Python unittest test cases
utils/           # APIClient and TestData helpers
collections/     # Postman collection JSON
reports/         # Test output reports
```
# init
