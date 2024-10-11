import yaml

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from yaml import Loader

from marketAPI.models import ProductCategory, Product, ExtraParameter, BasketProduct, OrderProduct, Order, User
from marketAPI.serializer import DetailedProductSerializer, BasketProductSerializer, \
    OrderProductSerializer, ProductSerializer, BasketProductCreateSerializer, MarketUserSerializer

import environ

env = environ.Env()
environ.Env.read_env()

class UpdateUserAddressView(APIView):
    def patch(self, request):

        user = request.user
        serializer = MarketUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class PartnerUpdateView(APIView):

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type == 'customer':
            return JsonResponse({'Status': False, 'Error': 'Shop only'}, status=403)

        file = request.data.get('file')
        data = yaml.load(file, Loader=Loader)
        shop_id = request.user.shop.id

        for category in data.get('categories'):
            ProductCategory.objects.update_or_create(
                id=category.get('id'),
                name=category.get('name')
            )
        for good in data.get('goods'):
            Product.objects.update_or_create(
                id=good.get('id'),
                model=good.get('model'),
                name=good.get('name'),
                price=good.get('price'),
                product_quantity=good.get('quantity'),
                category_id=good.get('category'),
                shop_id=shop_id
            )
            for parameter, value in good.get('parameters').items():
                ExtraParameter.objects.update_or_create(
                    name=parameter,
                    value = value,
                    product_id = good.get('id')
                )

        return JsonResponse({'Status': 'OK'})


class ProductView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
        else:
            product = Product.objects.get(pk=pk)
            serializer = DetailedProductSerializer(product)
        return Response(serializer.data)


class BasketProductViewSet(viewsets.GenericViewSet):
    queryset = BasketProduct.objects.all()

    def list(self, request):
        serializer = BasketProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        request.data["basket"] = request.user.basket.pk
        serializer = BasketProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def update(self, request, *args, **kwargs):
        basket_product = self.get_object()
        serializer = self.get_serializer(basket_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'position created':serializer.data})
        return Response(serializer.errors, status=400)


class OrderProductModelViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

    def create(self, request, *args, **kwargs):
        # Получаем данные из корзины пользователя
        basket = request.user.basket
        basketproducts = basket.position.all()

        # Создаем заказ
        order = Order.objects.create(user=request.user,
                                     status='active',
                                     delivery_address=request.data.get("delivery_address"))

        # Добавляем позиции в заказ
        total_price = 0
        products_list = []
        for basketproduct in basketproducts:
            order_product = OrderProduct.objects.create(order=order, product=basketproduct.product, quantity=basketproduct.quantity)
            total_price += order_product.product.price * order_product.quantity
            products_list.append(f"{order_product.product.name} - {order_product.quantity} шт. по цене {order_product.product.price} руб.")


        order.total_price = total_price
        order.save()

        basket.position.all().delete()

        subject = 'Подтверждение заказа'
        message = f'Заказ №{order.id} создан успешно!\n\nСписок товаров:\n{", ".join(products_list)}\n\nОбщая стоимость: {total_price} руб.'
        from_email = env("EMAIL_HOST")
        to_email = request.user.email
        send_mail(subject, message, from_email, [to_email])
        return Response({'message': f'Заказ № {order.pk} успешно создан'}, status=status.HTTP_201_CREATED)


@receiver(post_save, sender=OrderProduct)
def send_supplier_email_async(sender, instance, created, **kwargs):
    if created:
        products = instance.order.product.all()

        for product in products:
            shop = product.shop
            supplier_email = shop.user.email
            subject = f"Order notification: {product.name} has been ordered"
            message = f"Dear {shop.name},\n\nWe have received an order for {product.name}. Please prepare the product for shipping.\n\nBest regards, [Your Company Name]"


            send_mail(subject, message, env("EMAIL_HOST"), [supplier_email], fail_silently=False)
