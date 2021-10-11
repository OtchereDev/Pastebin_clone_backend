from api.views import DeletePaste, GetUser, GetUserProfile, GetUserSettings, NewFolder, NewPaste, RetrievePaste, RetrieveUserCodeFolder, RetrieveUserCodeFolderContent, Top10Paste, UpdatePaste,fieldReset,UpdateUserProfile,UpdateUserSettings
from django.urls import path,include
# from djoser.social

app_name='api'

urlpatterns = [
    path('reset/<str:type>/confirm/<str:uid>/<str:token>/',fieldReset),
    path('get_user_profile/',GetUserProfile.as_view(),name='get_user_profile'),
    path('get_user_settings/',GetUserSettings.as_view(),name='get_user_settings'),
    path('new/',NewPaste.as_view(),name='new_paste'),
    path('bin/<str:uuid>/update/',UpdatePaste.as_view(),name='update_paste'),
    path('bin/<str:uuid>/delete/',DeletePaste.as_view(),name='delete_paste'),
    path('update/profile/',UpdateUserProfile.as_view(),name='update_profile'),
    path('update/settings/',UpdateUserSettings.as_view(),name='update_settings'),
    path('new_folder/',NewFolder.as_view(),name='new_folder'),
    path('check-user/',GetUser.as_view(),name='get_user'),
    path('all_folders/',RetrieveUserCodeFolder.as_view(),name='all_folders'),
    path('folder/<uuid:uuid>/',RetrieveUserCodeFolderContent.as_view(),name='retrieve_folder'),
    path('top_paste/',Top10Paste.as_view(),name='top_ten_paste'),
    path('bin/<uuid:uuid>/',RetrievePaste.as_view(),name='retrieve_bin'),
    path('auth/', include('djoser.urls')),
    path('auth/account/', include('djoser.urls.jwt')),
    path('auth/social/', include('djoser.social.urls')),
]
