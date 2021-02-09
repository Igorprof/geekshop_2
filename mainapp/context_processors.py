from basketapp.models import Basket

def basket(request):
    baskets = []

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user).select_related('user')
    
    return {
        'baskets':baskets
    }