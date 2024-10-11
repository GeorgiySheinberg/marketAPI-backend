Регистрация происходит с использованием библиотеки djoser
POST /auth/users/ - в форме email и пароль

авторизация по authtoken. 
POST   /auth/token/login/

Список продуктов: 
/products/

Расширенная инфа по 1 продукту: 
product/<int:pk>/

Корзина:
basket/

Заказы: 
orders/
POST запрос формирует заказ из корзины


Изменение адреса:
PATCH lk/address/


Загрузка yaml файла партнёра:
update/
