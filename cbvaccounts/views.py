from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render

from django.views.generic import View, ListView
from django.views.generic.edit import DeleteView
from .forms import CustomerForm, OrderForm, CreateUserForm

from django.contrib import messages

# from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from django.contrib.auth.models import User, Group

from .filters import OrderFilter
from django.forms import inlineformset_factory

from django.utils.decorators import method_decorator

# Create your views here.

class RegisterPage(View):
    def get(self, request):
        form = CreateUserForm()
        context = {'form':form}
        return render(request, 'cbvaccounts/register.html', context)
    
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for '+ username)
            return redirect("/login/")
        context = {'form':form}
        return render(request, 'cbvaccounts/register.html', context)

class LoginPage(View):
    def get(self, request):
        return render(request, 'cbvaccounts/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
        return render(request, 'cbvaccounts/login.html')

class LogoutUser(View):
    def get(self, request):
        print("logout")
        logout(request)
        return redirect('/login/')

class Home(View):
    @method_decorator(login_required)
    def get(self, request):
        orders = Order.objects.all()
        customers = Customer.objects.all()

        total_customers = customers.count()
        print(orders)
        print(customers)
        # total_customers = customers.count()

        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()
        out_for_deliery = orders.filter(status='Out for delivery').count()

        context = {
            'orders':orders,
            'customers':customers,
            'total_orders':total_orders,
            'delivered':delivered,
            'pending':pending,
            'out_for_deliery':out_for_deliery,
        }
        return render(request, 'cbvaccounts/dashboard.html', context)        

class UserPage(View):
    @method_decorator(login_required)
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer)
        print(customer)
        print(orders)

        print('orders : ', orders)
        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()
        out_for_deliery = orders.filter(status='Out for delivery').count()

        context = {
            'orders':orders,
            'total_orders':total_orders,
            'delivered':delivered,
            'pending':pending,
            'out_for_deliery':out_for_deliery,
        }
        return render(request, 'cbvaccounts/user.html', context)

class AccountSettings(View):
    @method_decorator(login_required)
    def get(self, request):
        customer = request.user.customer
        form = CustomerForm(instance=customer)
        return render(request, 'cbvaccounts/account_Settings.html')

    def post(self, request):
        customer = request.user.customer
        
        form = CustomerForm(request.POST, request.FILES ,instance=customer)

        if form.is_valid():
            form.save()
        
        context = {
            'form':form
        }
        return render(request, 'cbvaccounts/account_Settings.html', context)

class Products(ListView):
    model = Product


class CustomerPage(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.get(id=kwargs['pk'])
        
        print('get pk', customers)


        orders = Order.objects.filter(customer=customers)
        order_count = orders.count()

        myFilter = OrderFilter(request.GET, queryset=orders)
        orders = myFilter.qs

        context = {
            'customer':customers, 
            'orders':orders, 
            'order_count':order_count,
            'myFilter':myFilter,
        }
        return render(request, 'cbvaccounts/customer.html', context)

    def post(self, request, *args, **kwargs):
        customers = Customer.objects.get(id=kwargs['pk'])
        print('post pk', customers)

        orders = Order.objects.filter(customer=customers)
        order_count = orders.count()

        myFilter = OrderFilter(request.GET, queryset=orders)
        orders = myFilter.qs

        context = {
            'customer':customers, 
            'orders':orders, 
            'order_count':order_count,
            'myFilter':myFilter,
        }
        return render(request, 'cbvaccounts/customer.html', context)

class CreateOrder(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
        customer = Customer.objects.get(id=kwargs['pk'])
        form = OrderFormSet(queryset=Order.objects.none(),instance=customer)

        # form = OrderFormSet(request.POST, instance=customer)
            

        context = {'form':form}
        return render(request, 'cbvaccounts/order_form.html', context)

    def post(self, request, *args, **kwargs):
        OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
        customer = Customer.objects.get(id=kwargs['pk'])
        print('CUSTOMER ',customer)
        form = OrderFormSet(queryset=Order.objects.none(),instance=customer)
        # form = OrderForm(initial={'customer':customer})
            # print('Pricing Post: ', request.POST)
            # form = OrderForm(request.POST)
        form = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("home")

        context = {'form':form}
        return render(request, 'cbvaccounts/order_form.html', context)

class UpdateOrder(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        form = OrderForm(instance=order)

        context = {
            'form':form
        } 
        return render(request, 'cbvaccounts/order_form.html', context)
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        form = OrderForm(instance=order)

        if form.is_valid():
            form.save()
            return redirect("home")

        context = {
            'form':form
        }
        return render(request, 'cbvaccounts/order_form.html', context)

class DeleteOrder(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        context = {
            'item':order
        }
        return render(request, 'cbvaccounts/delete.html', context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        order.delete()        
        context = {
            'item':order
        }
        return render(request, 'cbvaccounts/delete.html', context)