Absolutely! Here's your complete **ER diagram schema** written in **`dbdiagram.io` DSL** format.

---

### 🔧 Paste the below into [https://dbdiagram.io](https://dbdiagram.io):

```dbml
Table CustomUser {
  id int [pk]
  username varchar
  email varchar
  role varchar
}

Table Pizza {
  id int [pk]
  name varchar
  description text
  price decimal
  type varchar
  is_available boolean
}

Table Cart {
  id int [pk]
  user_id int [ref: > CustomUser.id]
  created_at datetime
}

Table CartItem {
  id int [pk]
  cart_id int [ref: > Cart.id]
  pizza_id int [ref: > Pizza.id]
  quantity int
}

Table Order {
  id int [pk]
  user_id int [ref: > CustomUser.id]
  delivery_partner_id int [ref: > CustomUser.id]
  status varchar
  total_price decimal
  payment_mode varchar
  payment_status varchar
  created_at datetime
}

Table OrderItem {
  id int [pk]
  order_id int [ref: > Order.id]
  pizza_id int [ref: > Pizza.id]
  quantity int
}

Table DeliveryComment {
  id int [pk]
  order_id int [ref: > Order.id]
  partner_id int [ref: > CustomUser.id]
  comment text
  timestamp datetime
}

Table Rating {
  id int [pk]
  user_id int [ref: > CustomUser.id]
  pizza_id int [ref: > Pizza.id]
  rating int
  comment text
  created_at datetime
}
```

---

### 📝 Steps to Use

1. Go to [https://dbdiagram.io](https://dbdiagram.io)
2. Click "New Diagram"
3. Paste the code above into the left editor
4. Your ERD will render live on the right!
5. You can download as PNG, share, or export.

---

Would you like me to include this in a `.docx` or `.pdf` as well with descriptions?
