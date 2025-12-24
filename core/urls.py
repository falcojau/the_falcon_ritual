"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from e_shop.views import HomeView, RegisterView, UserLoginView, logout_view, ContactView
from e_shop.views import ProductListView, CategoryProductListView, ProductDetailView, MyOrdersViews
from e_shop.views import remove_from_cart_view, view_cart, add_to_cart_view, decrement_cart_view, checkout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', ProductListView.as_view(), name='home'),

    path('category/<slug:slug>/', CategoryProductListView.as_view(), name='category_filter'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/decrement/<int:product_id>/', decrement_cart_view, name='decrement_cart'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    
    path('checkout/', checkout_view, name='checkout'),
    path('orders/', MyOrdersViews.as_view(), name='my_orders'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)