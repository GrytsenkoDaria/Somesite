from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Product, ProductType
from .forms import Productform
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class CustomSuccessMessageMixin:
    """Сообщение об удачной операции"""
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class ProductListView(ListView):
    """Список всех товаров"""
    # model = Product     # Моя модель ( таблица с БД )
    template_name = 'home.html'     # Сылка как в функции
    context_object_name = 'list_product'    # Контекстк который раньше передавал в функции

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['list_types'] = ProductType.choices
        return context
    
    def get_queryset(self):
        filter_param = self.request.GET.get('type')
        search_param = self.request.GET.get('search')
        if filter_param:
            queryset = Product.objects.filter(type=filter_param)
        elif search_param:
            queryset = Product.objects.filter(name__icontains=search_param)
        else:
            queryset = Product.objects.all()
        return queryset


# def home(request):
#
#     if request.query_params:
#         product_type = request.query_params.get('type')
#         list_product = Product.objects.get(type=product_type)
#     else:
#         list_product = Product.objects.all()
#
#     context = {
#         'list_product': list_product
#
#     }
#     return render(request, 'home.html', context)


class HomeDetailView(LoginRequiredMixin, DetailView):
    """Вывод определенного товара с БД"""
    model = Product
    template_name = 'detail.html'
    context_object_name = 'get_product'


# def detail(request, id):
#     """Вывод товара с БД"""
#     get_product = Product.objects.get(id=id)
#     context = {
#         'get_product': get_product
#     }
#     return render(request, 'detail.html', context)


class ProductCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    """Создание товара в БД"""
    model = Product
    success_msg = 'Add successful'
    template_name = 'edit_page.html'
    form_class = Productform
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['list_product'] = Product.objects.all().order_by('id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save
        return super().form_valid(form)


# def edit_page(request):
#
#     suc = False
#
#     if request.method == 'POST':    # Если в моей html странице form method имеет значние пост
#         form = Productform(request.POST)    # (request.POST) получаем параметры с браузера
#         if form.is_valid():     # Если форма валидна, тоесть все прохидит то идем дальше :)
#             form.save()     # Сохраняем значения юзера
#             suc = True
#
#     context = {
#         'list_product': Product.objects.all().order_by('id'),
#         'form': Productform(),
#         'suc': suc
#
#     }
#     return render(request, 'edit_page.html', context)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление товара в БД"""
    model = Product
    template_name = 'edit_page.html'
    form_class = Productform
    success_url = reverse_lazy('edit_page')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

# def update_page(request, id):
#
#     if request.method == 'POST':    # Если в моей html странице form method имеет значние пост
#         form = Productform(request.POST, instance=Product.objects.get(id=id))    # (request.POST) получаем параметры
#         # с браузера
#         if form.is_valid():     # Если форма валидна, тоесть все прохидит то идем дальше :)
#             form.save()     # Сохраняем значения юзера
#
#     context = {
#
#         'get_product': Product.objects.get(id=id),
#         'form': Productform(instance=Product.objects.get(id=id)),
#         'update': True
#     }
#     return render(request, 'edit_page.html', context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара"""
    model = Product
    template_name = 'edit_page.html'
    # success_url = reverse_lazy('edit_page')
    # Для работы этого класса необходимо написать форму
    # <form action="{% url 'delete_page' i.id %}" method="post">{% csrf_token %}

    def delete(self, request, *args, **kwargs):
        success_url = reverse_lazy('profile_products')
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        self.object.delete()
        return HttpResponseRedirect(success_url)
        # return HttpResponse()

# def delete_page(request, pk):
#     """Удаление товара с БД"""
#     Product.objects.get(id=pk).delete()
#     return redirect(reverse('edit_page'))


class Search(ListView):
    """Поиск товара"""

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['search'] = self.request.GET.get('search')
    #     return context


class ProfileView(ListView):
    model = Product
    template_name = 'profile.html'
    context_object_name = 'get_product'


class ProfileProductsView(ListView):
    # model = Product
    template_name = 'profile_products.html'
    context_object_name = 'get_product'

    def get_queryset(self):
        queryset = Product.objects.filter(author=self.request.user)
        return queryset
