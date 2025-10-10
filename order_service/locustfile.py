from uuid import uuid4
import random
import datetime

from locust import HttpUser, task, between
from faker import Faker


class MicroserviceUser(HttpUser):
    wait_time = between(1, 3)
    fake = Faker()
    catalog_host = "http://localhost:8000/api/products"
    order_host = "http://localhost:8080/api/orders"
    product_ids = []
    order_ids = []
    product_descriptions = []

    @task
    def get_products(self):
        # 50% запросов — с параметром description
        if self.product_descriptions and random.random() < 0.5:
            desc = random.choice(self.product_descriptions)
            start = random.randint(0, max(0, len(desc) - 10))
            substring = desc[start:start + 10].strip()
            self.client.get(self.catalog_host, params={"description": substring})
        else:
            self.client.get(self.catalog_host)

    @task
    def create_product(self):
        product_id = str(uuid4())
        description = self.fake.text(max_nb_chars=100)
        payload = {
            "id": product_id,
            "title": f"Product {random.randint(1000, 9999)}",
            "category_id": random.randint(1, 10),
            "description": description,
            "characteristics": {"color": "red", "size": "M"},
            "created_at": datetime.datetime.utcnow().isoformat(),
            "amount": random.randint(1, 100),
            "price": round(random.uniform(10, 500), 2),
        }
        response = self.client.post(self.catalog_host, json=payload)
        if response.status_code == 201:
            self.product_ids.append(product_id)
            self.product_descriptions.append(description)

    @task
    def get_product_by_id(self):
        if self.product_ids:
            product_id = random.choice(self.product_ids)
            self.client.get(f"{self.catalog_host}/{product_id}")

    @task
    def init_order(self):
        if self.product_ids:
            product_id = random.choice(self.product_ids)
            response = self.client.post(f"{self.order_host}/init", json=str(product_id))
            if response.status_code == 200:
                order = response.json()
                self.order_ids.append(order["id"])

    @task
    def get_order_by_id(self):
        if self.order_ids:
            order_id = random.choice(self.order_ids)
            self.client.get(f"{self.order_host}/{order_id}")

    @task
    def confirm_order(self):
        if self.order_ids:
            order_id = random.choice(self.order_ids)
            response = self.client.get(f"{self.order_host}/{order_id}")
            if response.status_code == 200:
                order = response.json()
                if order.get("status") != "paid":
                    confirm_response = self.client.post(f"{self.order_host}/{order_id}/confirm")
                    if confirm_response.status_code == 400:
                        print(f"[400] Confirm error: {confirm_response.text}")
