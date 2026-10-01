from sqladmin import ModelView
<<<<<<< HEAD

from mysite.database.models import UserProfile, RefreshToken


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id,
        UserProfile.first_name,
        UserProfile.last_name,
        UserProfile.username,
        UserProfile.email,
        UserProfile.status,
        UserProfile.registered_date
    ]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [
        RefreshToken.id,
        RefreshToken.user_id,
        RefreshToken.token,
        RefreshToken.created_date
    ]
=======
from mysite.database.models import User, Product, Order, RefreshToken

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.phone_number, User.registered_date]
    column_searchable_list = [User.username, User.email, User.phone_number]
    column_sortable_list = [User.id, User.username, User.registered_date]
    form_excluded_columns = [User.user_token]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.category, Product.store, Product.product_name, Product.price, Product.created_date]
    column_searchable_list = [Product.category, Product.store, Product.product_name]
    column_sortable_list = [Product.id, Product.price, Product.created_date]
    name = "Product"
    name_plural = "Products"
    icon = "fa-solid fa-box"

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.product_id, Order.user_id, Order.status, Order.created_date]
    column_sortable_list = [Order.id, Order.status, Order.created_date]
    name = "Order"
    name_plural = "Orders"
    icon = "fa-solid fa-truck"

class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_date]
    column_sortable_list = [RefreshToken.id, RefreshToken.created_date]
    form_excluded_columns = [RefreshToken.token_user]
    name = "Refresh Token"
    name_plural = "Refresh Tokens"
    icon = "fa-solid fa-key"
>>>>>>> 79752a4 (chain)
