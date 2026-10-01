from fastapi import FastAPI
from sqladmin import Admin
<<<<<<< HEAD

from mysite.admin.views import UserProfileAdmin, RefreshTokenAdmin
from mysite.database.db import engine


def setup_admin(mysite: FastAPI):
    admin = Admin(mysite, engine)
    admin.add_view(UserProfileAdmin)
=======
from mysite.database.db import engine
from mysite.admin.views import UserAdmin, ProductAdmin, OrderAdmin, RefreshTokenAdmin

def setup_admin(app: FastAPI):
    admin = Admin(app=app, engine=engine, title="Delivery Operator Admin")
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
>>>>>>> 79752a4 (chain)
    admin.add_view(RefreshTokenAdmin)