from celery import Celery
from celery import shared_task
from django.core.mail import send_mail

from marketAPI.models import Order, OrderProduct

app = Celery('views',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             broker_connection_retry_on_startup=True)

app.autodiscover_tasks()


@shared_task
def send_supplier_email(order_id, product_id):
    # Получаем заказ и продукт по их идентификаторам
    order = Order.objects.get(id=order_id)
    product = OrderProduct.objects.get(id=product_id)

    # Получаем все продукты в заказе
    products = order.product.all()

    for product in products:
        shop = product.shop
        supplier_email = shop.user.email
        subject = f"Order notification: {product.name} has been ordered"
        message = f"Dear {shop.name},\n\nWe have received an order for {product.name}. Please prepare the product for shipping.\n\nBest regards, [Your Company Name]"


        send_mail(subject, message, 'georgiysheberg@gmail.com', [supplier_email], fail_silently=False)