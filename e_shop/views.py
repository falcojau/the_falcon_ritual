from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from django.contrib.auth.models import User

from e_shop.forms import RegisterUserForm, LoginUserForm, ContactForm
from e_shop.models import Product, Category, Order, OrderItem


class HomeView(TemplateView):
    template_name = 'general/home.html'


'''Register Views'''
# CCBV por Register an User
class RegisterView(CreateView):
    template_name = 'general/register.html'
    model = User
    success_url = reverse_lazy('home')
    form_class = RegisterUserForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome to The Falcon Ritual, {self.object.username}! Your account has been succesfully created.')
        # Autologin
        login(self.request, self.object)
        return response


'''Login Views'''
# CCBV por Login an existing User
class UserLoginView(FormView):
    form_class = LoginUserForm
    template_name = 'general/login.html'
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_found = authenticate(self.request, username=username, password=password)

        if user_found is not None:
            login(self.request, user_found)
            messages.info(self.request, f'Welcome {user_found.username} 🙌')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(self.request, 'User or password wrong ❌')
            return self.form_invalid(form)
        

# View based on a function for logout
def logout_view(request):
    logout(request)
    messages.info(request, f'Goodbye 👋 ​')
    return redirect('home')


'''Contact Views'''
# Method for the Contact View
class ContactView(FormView):
    template_name = 'general/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message, we will contact you shortly  🚀')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was a mistake with the form, please check the fields.')
        return super().form_invalid(form)


'''Product Views'''
# CCBV to check products' details
class ProductDetailView(DetailView):
    model = Product
    template_name = 'general/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# CCBV to see all products
class ProductListView(ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# View to filter for Category
class CategoryProductListView(ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Filter the products for the slug on the category that comes on the URL
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


'''Cart Views'''
# View to create the cart
def add_to_cart_view(request, product_id):
    cart = request.session.get('cart', {})  # If there is no cart yet, we get it
    prod_id = str(product_id)  # We conver product_id to string 

    # We add 1 prod to cart
    if prod_id in cart:
        cart[prod_id] += 1
    else:
        cart[prod_id] = 1

    request.session['cart'] = cart  # We save the cart again on the session
    
    request.session.modified = True     # Importat to let Django know the session has changed

    messages.info(request, f'Product added to the cart ✅')
    return redirect('view_cart')


# View to decrement the cart
def decrement_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    prod_id = str(product_id)

    if prod_id in cart:
        # Restamos 1 unidad
        cart[prod_id] -= 1
        
        # Si la cantidad llega a 0 (o menos), eliminamos el producto del diccionario
        if cart[prod_id] <= 0:
            del cart[prod_id]
            messages.info(request, "Product removed from the cart")
        else:
            messages.info(request, "An item has been removed")

    # Guardar y marcar modificación
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('view_cart')


# View to see the cart
def view_cart(request):
    cart = request.session.get('cart', {})
    # We get all products the user has on the cart right now
    products_in_cart = Product.objects.filter(id__in=cart.keys())
    
    total_cart = 0
    
    for p in products_in_cart:
        # We get the quantity of the dictionary using ID (as a string)
        p.quantity = cart.get(str(p.id))

        p.subtotal = p.quantity * p.price
        total_cart += p.subtotal

    return render(request, 'general/cart.html', {
        'products_in_cart': products_in_cart,
        'total_cart': total_cart,
    })


# View to delete something from the cart
def remove_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    prod_id = str(product_id)

    # If the product is on the cart, we delete it
    if prod_id in cart:
        del cart[prod_id]
        messages.success(request, "Product removed from the cart 🗑️")
    
    # We save the changes and modify the session
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


'''CheckOut Views'''
def checkout_view(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, "Your cart is empty")
        return redirect('home') # You can't pay an empty cart

    if request.method == 'POST':
        # We create the order
        order = Order.objects.create(user=request.user, total_price=0)
        total_order_price = 0

        for p_id, q in cart.items():
            product = Product.objects.get(id=p_id)
            subtotal = product.price * q
            total_order_price += subtotal

            # We create the details for the order
            OrderItem.objects.create(order=order, product=product, quantity=q, price_at_purchase=product.price)
        
        # Let's update the order and save it
        order.total_price = total_order_price
        order.save()

        # We clean the cart of the session
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, "Order completed! 🎉")
        return redirect('my_orders')

    # -- para el GET, calculamos el total para mostrarlo en la confirmación
    return render(request, 'general/checkout.html', {'cart': cart})


'''MyOrders Views'''
# CCBV to check a list of the orders
class MyOrdersViews(LoginRequiredMixin, ListView):   # LoginRequiredMixin doesn't allow anyone if not registered
    model = Order
    template_name = 'general/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # The user is only allowed to see his own orders
        return Order.objects.filter(user=self.request.user).order_by('-created_at')