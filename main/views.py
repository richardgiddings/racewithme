from django.shortcuts import render
from users.models import Profile

def user_profile(request):

    profile = Profile.objects.get(user=request.user)

    print(profile.user.username)

    return render(request, template_name='main/user_profile.html', 
                  context={'profile': profile})