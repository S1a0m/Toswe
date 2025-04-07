from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.v1.admin import users, products, orders, notifications, announcements
from .routes.v1.mobile import products as mob_products, orders as mob_orders, notifications as mob_notifs
from .routes.v1.common import auth


app = FastAPI(
    title="Toswe Backend API",
    version="1.0.0"
)

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # Change in production
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(notifications.router)
app.include_router(announcements.router)

app.include_router(mob_products.router)
app.include_router(mob_orders.router)
app.include_router(mob_notifs.router)

app.include_router(auth.router)