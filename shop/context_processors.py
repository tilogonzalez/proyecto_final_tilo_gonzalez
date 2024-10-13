from .models import Profile
from shop_messages.models import Notification

def profile_context(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            pass
    return {'profile': profile}

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, read=False).count()
        return {'notification_count': count}    
    return {'notification_count': 0}
