
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [ 
    path('/signup', signup_page, name='signup'),      
    path('/login', login_page, name='login_page'),      
    path('/logout', logout_page, name='logout_page'), 


    path('/forgot_password', forgot_password, name='forgot_password'),      
    path('/message_page', message_page, name='message_page'),      
    path('/reset_password/<str:reset_code>', reset_password, name='reset_password'),      
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

