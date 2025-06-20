Here's a **Postman testing guide** for each role: **Customer**, **Delivery Partner**, and **Admin** — including headers, endpoints, and sample payloads. This assumes you're using **JWT authentication** (`Bearer <token>`).

---

## 🔐 Step 0: Common Setup for All Users

### ➕ Register (POST)

```http
POST http://127.0.0.1:8000/api/register/
Content-Type: application/json

{
  "username": "customer1",
  "email": "customer1@example.com",
  "password": "custpass123",
  "role": "customer"
}
```

Repeat for:

* `admin1` → role: `"admin"`
* `delivery1` → role: `"delivery"`

---

### 🔑 Login (POST)

```http
POST http://127.0.0.1:8000/api/login/
Content-Type: application/json

{
  "username": "customer1",
  "password": "custpass123"
}
```

Save the **access token** and use in `Authorization: Bearer <token>` header for all other requests.

---

## 👤 1. Customer Actions

### 🧾 View All Pizzas (GET)

```http
GET http://127.0.0.1:8000/api/pizzas/
(No Auth required)
```

---

### 🛒 Add to Cart (POST)

```http
POST http://127.0.0.1:8000/api/cart/
Authorization: Bearer <customer_token>
Content-Type: application/json

{
  "pizza_id": 1,
  "quantity": 2
}
```

### 📋 View Cart (GET)

```http
GET http://127.0.0.1:8000/api/cart/
Authorization: Bearer <customer_token>
```

### ❌ Clear Cart (DELETE)

```http
DELETE http://127.0.0.1:8000/api/cart/
Authorization: Bearer <customer_token>
```

---

### ✅ Checkout Cart (POST)

```http
POST http://127.0.0.1:8000/api/checkout/
Authorization: Bearer <customer_token>
Content-Type: application/json

{
  "payment_mode": "online"
}
```

---

### 🔁 View Previous Orders (GET)

```http
GET http://127.0.0.1:8000/api/orders/
Authorization: Bearer <customer_token>
```

---

### ⭐ Rate Pizza (POST)

```http
POST http://127.0.0.1:8000/api/rate-pizza/
Authorization: Bearer <customer_token>
Content-Type: application/json

{
  "pizza_id": 1,
  "rating": 5,
  "comment": "Absolutely delicious!"
}
```

---

## 🚚 2. Delivery Partner Actions

### 🚀 Update Order Status (PATCH)

```http
PATCH http://127.0.0.1:8000/api/orders/1/update-status/
Authorization: Bearer <delivery_token>
Content-Type: application/json

{
  "status": "delivered"
}
```

---

### 🗣️ Add Delivery Comment (POST)

```http
POST http://127.0.0.1:8000/api/delivery-comments/
Authorization: Bearer <delivery_token>
Content-Type: application/json

{
  "order_id": 1,
  "comment": "Customer was not home. Left at the door."
}
```

---

## 🛠️ 3. Admin Actions

### ➕ Add Pizza (POST)

```http
POST http://127.0.0.1:8000/api/pizzas/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Farmhouse",
  "description": "Veg loaded with onions, capsicum, tomatoes",
  "price": "299.00",
  "type": "veg",
  "is_available": true
}
```

---

### ✏️ Update Pizza (PATCH)

```http
PATCH http://127.0.0.1:8000/api/pizzas/1/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "price": "349.00"
}
```

---

### ❌ Delete Pizza (DELETE)

```http
DELETE http://127.0.0.1:8000/api/pizzas/1/
Authorization: Bearer <admin_token>
```

---

### 🔍 Filter Pizza by Type

```http
GET http://127.0.0.1:8000/api/pizzas/?type=veg
(No Auth required)
```

---

### 📝 Update User Details (PATCH)

```http
PATCH http://127.0.0.1:8000/api/users/3/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "email": "updated@example.com"
}
```

---

Would you like this turned into a Postman collection file or PDF to import directly into Postman?
