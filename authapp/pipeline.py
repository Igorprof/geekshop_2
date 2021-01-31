from authapp.models import ShopUserProfile, User
from social_core.exceptions import AuthForbidden
from django.conf import settings

import requests
import datetime



def save_user_profile(backend, user, response, *args, **kwargs):    
    if backend.name != 'vk-oauth2':
        return          
    
    api_url = f"https://api.vk.com/method/users.get?fields=bdate,about,sex,photo_400_orig&access_token={response['access_token']}&v=5.92"

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return
    
    data = resp.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
    if 'about' in data:
        user.shopuserprofile.about_me = data['about']
    if 'bdate' in data:
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        today = datetime.date.today()
        age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
  
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if 'photo_400_orig' in data:
        photo_data = requests.get(data['photo_400_orig'])
        with open(f'{settings.MEDIA_URL[1:-1]}/users_avatars/{user.pk}.jpg', 'wb') as photo:
            photo.write(photo_data.content)
        user.avatar = f'users_avatars/{user.pk}.jpg'
     
    user.save()