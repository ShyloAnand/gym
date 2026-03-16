from django.http import HttpResponse
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product,Fit
from .models import UserProfile
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_image = request.FILES.get('profile_image')

        # Validation
        if not all([full_name, phone, username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        # Create or update profile safely
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = phone
        if profile_image:
            profile.image = profile_image   # ✔ correct field name
        profile.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "register.html")

def sports(request):
    products = Product.objects.all()
    return render(request, 'sports.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    # If product already in cart, increase quantity
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('sports')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        product.quantity = quantity
        product.subtotal = product.price * quantity
        total += product.subtotal
        products.append(product)

    context = {
        'products': products,
        'total': total
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('cart')


from .models import DietUser, DietPlan


def diet_plan(request):
    if request.method == 'POST':
        name = request.POST['name']
        dob = request.POST['dob']
        height = int(request.POST['height'])
        weight = int(request.POST['weight'])
        goal = request.POST['goal']   # get selected option

        user = DietUser.objects.create(
            name=name,
            dob=dob,
            height=height,
            weight=weight
        )

        # get plan according to selected goal
        plan = DietPlan.objects.filter(goal=goal).first()

        return render(request, 'diet_result.html', {
            'user': user,
            'plan': plan
        })

    return render(request, 'diet_form.html')
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')



def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()

    return render(request, 'sports.html', {
        'products': products,
        'query': query
    })

def fitness(request):
    products = Fit.objects.all()
    return render(request, 'fitness.html', {'products': products})

def payment(request):
    return render(request, 'payment.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Enter both username and password.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")

def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        
        # Update User fields
        request.user.first_name = request.POST.get("first_name")
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update profile image
        if request.FILES.get("image"):
            profile.image = request.FILES.get("image")

        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("home")

    return render(request, "edit_profile.html")












