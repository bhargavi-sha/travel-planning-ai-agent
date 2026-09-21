from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, Response

app = FastAPI(title="ShopSphere API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_origin_regex=r"http://localhost:517[0-9]",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    {"id": 1, "title": "Echo Dot (5th Gen)", "price": 49.99, "rating": 4.7, "reviews": 98214, "category": "Electronics", "image": "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=500&q=80", "prime": True},
    {"id": 2, "title": "Noise Cancelling Headphones", "price": 129.99, "rating": 4.5, "reviews": 4120, "category": "Electronics", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80", "prime": True},
    {"id": 3, "title": "Everyday Running Shoes", "price": 64.50, "rating": 4.4, "reviews": 1893, "category": "Fashion", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=80", "prime": False},
    {"id": 4, "title": "Minimal Desk Lamp", "price": 35.99, "rating": 4.6, "reviews": 726, "category": "Home", "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=80", "prime": True},
    {"id": 5, "title": "Stainless Steel Water Bottle", "price": 22.00, "rating": 4.8, "reviews": 5632, "category": "Home", "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=500&q=80", "prime": True},
    {"id": 6, "title": "Smart Fitness Watch", "price": 179.00, "rating": 4.3, "reviews": 2240, "category": "Electronics", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80", "prime": True},
]

orders = []
allowed_statuses = ["Preparation", "Shipped", "Out for delivery", "Delivered"]


class OrderCreate(BaseModel):
    items: list[dict]
    total: float


class OrderStatusUpdate(BaseModel):
    status: str


class ProductCreate(BaseModel):
    title: str
    price: float
    category: str
    image: str
    rating: float = 4.5
    reviews: int = 0
    prime: bool = False

@app.get("/api/products")
def get_products(query: str = "", category: str = "All"):
    result = products
    if category != "All":
        result = [p for p in result if p["category"] == category]
    if query:
        term = query.lower()
        result = [p for p in result if term in p["title"].lower()]
    return result

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

@app.get("/api/categories")
def get_categories():
    return ["All", "Electronics", "Fashion", "Home"]


@app.get("/api/navigation/all")
def get_all_navigation_products():
    return products


@app.get("/api/navigation/todays-deals")
def get_todays_deals():
    return [
        {
            **product,
            "original_price": round(product["price"] * 1.25, 2),
            "discount_percent": 20,
        }
        for product in products[:4]
    ]


@app.get("/api/navigation/customer-service")
def get_customer_service():
    return {
        "help_topics": ["Your orders", "Shipping and delivery", "Returns and refunds", "Account settings"],
        "contact": {"email": "support@shopsphere.demo", "hours": "Mon–Fri, 09:00–17:00"},
    }


@app.get("/api/navigation/registry")
def get_registry():
    return {
        "title": "ShopSphere Registry",
        "types": ["Wedding", "Baby", "Housewarming"],
        "message": "Create a registry and share it with friends and family.",
    }


@app.get("/api/navigation/gift-cards")
def get_gift_cards():
    return {
        "title": "ShopSphere Gift Cards",
        "amounts": [10, 25, 50, 100],
        "formats": ["Digital gift card", "Printable gift card"],
    }


@app.get("/api/navigation/sell")
def get_sell_information():
    return {
        "title": "Sell on ShopSphere",
        "steps": ["Create a seller profile", "Add your products", "Ship customer orders", "Get paid"],
        "message": "Start listing products from your seller dashboard.",
    }


@app.get("/api/navigation/fashion-deals")
def get_fashion_deals():
    fashion_products = [product for product in products if product["category"] == "Fashion"]
    return [
        {**product, "original_price": round(product["price"] * 1.3, 2), "discount_percent": 23}
        for product in fashion_products
    ]


@app.post("/api/admin/products", status_code=201)
def create_product(product: ProductCreate):
    new_product = {"id": max(item["id"] for item in products) + 1, **product.model_dump()}
    products.append(new_product)
    return new_product


@app.post("/api/orders", status_code=201)
def create_order(order: OrderCreate):
    order_id = f"SS-{len(orders) + 100001}"
    new_order = {
        "id": order_id,
        "items": order.items,
        "total": order.total,
        "status": "Preparation",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    orders.append(new_order)
    return new_order


@app.get("/api/admin/orders")
def get_admin_orders():
    return orders


@app.get("/api/admin/dashboard")
def get_admin_dashboard():
    return {
        "product_count": len(products),
        "order_count": len(orders),
        "preparation_count": sum(order["status"] == "Preparation" for order in orders),
        "shipped_count": sum(order["status"] in {"Shipped", "Out for delivery"} for order in orders),
        "delivered_count": sum(order["status"] == "Delivered" for order in orders),
    }


@app.patch("/api/admin/orders/{order_id}/status")
def update_order_status(order_id: str, update: OrderStatusUpdate):
    if update.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid order status")
    order = next((item for item in orders if item["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["status"] = update.status
    return order
