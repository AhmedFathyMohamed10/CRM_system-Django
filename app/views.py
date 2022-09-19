from django.shortcuts import render, redirect, get_object_or_404



# Database 
from .models import *
# Forms
from .forms import *
# InitialFactory form
from django.forms import inlineformset_factory

# Authentication views
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# decorators.py
from .decorators import unauthenticated_user, allowed_users, admin_only

# Grouping views
from django.contrib.auth.models import Group


@unauthenticated_user
def register(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Signals part --> make auto profile for user if he is normal user
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'registeration/register.html', context)



@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'registeration/login.html', context)



@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
@admin_only
def home(request):

    # Retrieve all orders
    orders = Order.objects.all()
    total_orders = orders.count()

    # Retrieve all customers
    customers = Customer.objects.all()
    total_customers = customers.count()

    # Retrieve all products
    products = Product.objects.all()
    total_products = products.count()

    # Retrieve all delivered orders
    delivered = Order.objects.filter(status='Delivered')  # Filter orders by status
    delivered_count = delivered.count()

    # Retrieve all pending orders
    pending = Order.objects.filter(status='Pending')
    pending_count = pending.count()


    context = {
        'orders': orders,
        'total_orders': total_orders,
        'customers': customers,
        'total_customers': total_customers,
        'products': products,
        'total_products': total_products,
        'delivered': delivered,
        'pending': pending,
        'delivered_count': delivered_count,
        'pending_count': pending_count,
    }

    return render(request, 'pages/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    user_orders = request.user.customer.order_set.all()  # Get all orders for the logged in customer
    user_total_orders = user_orders.count()
    user_delivered = user_orders.filter(status='Delivered').count()
    user_pending = user_orders.filter(status='Pending').count()


    context = {
        'user_orders': user_orders,
        'user_total_orders': user_total_orders,
        'user_delivered': user_delivered,
        'user_pending': user_pending,
    }
    return render(request, 'pages/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer', 'admin'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'pages/account_settings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):

    all_products = Product.objects.all()
    return render(request, 'pages/products.html', {'all_products': all_products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def search_view(request):
    if request.method == 'POST':
        searched = request.POST['query'] # Get the searched value
        products = Product.objects.filter(name__contains=searched)
        counting = products.count()
        return render(request, 'parts/search.html', {'searched': searched, 'products': products, 'counting': counting})
    else:
        return render(request, 'parts/search.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    
    # Retrieve customer by id
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return redirect('home')

    orders = customer.order_set.all()
    order_count = orders.count()


    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
    }

    return render(request, 'pages/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {
        'formset': formset,
    }

    return render(request, 'pages/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)  # Get order by id
    form = OrderForm(instance=order) # Create form with order instance

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) 
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, 'pages/order_form.html', context)


# # search function for products
# def search_view(request):
#     if request.method == 'POST':
#         search_term = request.POST.get('search') # if search term is found, get it
#         products = Product.objects.filter(name__icontains=search_term) # name__icontains = name contains search_term
#         return render(request, 'parts/search.html', {'search_term': search_term ,'products': products})
#     else:
#         return render(request, 'parts/search.html', {'products': 'You have not searched for any term'})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {
        'item': order,
    }

    return render(request, 'pages/delete_order.html', context)