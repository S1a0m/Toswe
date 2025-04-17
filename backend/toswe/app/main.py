from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes.v1.admin import users, products, orders, notifications, announcements
from .routes.v1.mobile import products as mob_products, orders as mob_orders, notifications as mob_notifs
from .routes.v1.common import auth

from app.routes.v1.web import messages as client_message
from app.routes.v1.admin import messages as admin_message


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

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(notifications.router)
app.include_router(announcements.router)
app.include_router(admin_message.router)

app.include_router(mob_products.router)
app.include_router(mob_orders.router)
app.include_router(mob_notifs.router)

app.include_router(auth.router)


app.include_router(client_message.router)