from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm
from basketapp.models import Basket
from mainapp.models import Product


class OrderList(ListView):
    model = Order
    # template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



class OrderCreate(CreateView):
    model = Order
    # template_name = 'ordersapp/order_form.html'

    fields = []
    success_url = reverse_lazy('order:orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            Basket.objects.filter(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    # template_name = 'ordersapp/order_form.html'

    fields = []
    success_url = reverse_lazy('order:orders')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)           
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price           

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)

class OrderDelete(DeleteView):
    model = Order
    # template_name = 'ordersapp/order_confirm_delete.html'
    success_url = reverse_lazy('order:orders')


class OrderDetail(DetailView):
    model = Order
    # template_name = 'ordersapp/order_detail.html'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:orders'))


@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quaintity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.objects.get(pk=instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()

@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quaintity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()

def get_product_price(request, pk):
    if request.is_ajax():
        product_item = Product.objects.filter(pk=int(pk)).first()
        if product_item:
            return JsonResponse({'price': product_item.price})
        else:
            return JsonResponse({'price': 0})


