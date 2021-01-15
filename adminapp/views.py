from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from authapp.models import User
from mainapp.models import ProductCategory
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, UserAdminCreateProductForm

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    paginate_by = 3

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
   
#     context = {
#         'users': User.objects.all(),
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminRegisterForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
   
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):  # добавление контекста
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({'title': 'Geekshop - редактирование пользователя'})
        return context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user)

#     context = {'form': form, 'user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id=user_id)
#     # user.delete()
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))


class ProductCategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-product_categories-read.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoriesListView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories(request):
#     context = {
#         'product_categories': ProductCategory.objects.all(),
#     }

#     return render(request, 'adminapp/admin-product_categories-read.html', context)

class ProductCategoriesUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-product_categories-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_product_categories')
    form_class = UserAdminCreateProductForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoriesUpdateView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_update(request, product_category_id):
#     category = ProductCategory.objects.get(id=product_category_id)
#     if request.method == 'POST':
#         form = UserAdminCreateProductForm(data=request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_product_categories'))
#     else:
#         form = UserAdminCreateProductForm(instance=category)

#     context = {'form': form, 'product_category': category}
#     return render(request, 'adminapp/admin-product_categories-update-delete.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin-product_categories-create.html'
    success_url = reverse_lazy('admin_staff:admin_product_categories')
    form_class = UserAdminCreateProductForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCategoryCreateView, self).dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_create(request):
#     if request.method == 'POST':
#         form = UserAdminCreateProductForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_product_categories'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminCreateProductForm()

#     context = {'form': form}
#     return render(request, 'adminapp/admin-product_categories-create.html', context)

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin_staff:admin_product_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

# @user_passes_test(lambda u: u.is_superuser)
# def admin_product_categories_remove(request, product_category_id):
#     category = ProductCategory.objects.get(id=product_category_id)
#     category.delete()
#     return HttpResponseRedirect(reverse('admin_staff:admin_product_categories'))

