from .models import Account

def profile_photo(request):
    if request.user.is_authenticated:
        account_obj = Account.objects.get(user=request.user)
        photo = account_obj.avatar
        return {'image': photo}
    return {}
