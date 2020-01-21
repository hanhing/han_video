from django.urls import path
from .views.base import Index
from .views.base01 import Base01
from .views.auth import Login, Admin_Manage, Logout, UpdateAdminStatus
from .views.video import ExternaVideo, ExternaVideoPost, VideoSubView, VideoSubGet, VideoStarView, StarDelete

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('base01', Base01.as_view()),  # django自带模板
    path('login', Login.as_view(), name='dashboard_login'),
    path('admin/manage', Admin_Manage.as_view(), name='admin'),
    path('logout', Logout.as_view(), name='logout'),
    path('admin/manage/update/status', UpdateAdminStatus.as_view(), name='admin_update_status'),
    path('video/externa', ExternaVideo.as_view(), name='externa_video'),
    path('video/externa_post', ExternaVideoPost.as_view(), name='externa_video_post'),
    path('video/videosub/<int:video_id>', VideoSubView.as_view(), name='video_sub'),
    path('video/videosubpost/<int:video_id>', VideoSubGet.as_view(), name='video_sub_post'),
    path('video/star', VideoStarView.as_view(), name='video_star'),
    path('video/star/delete<int:star_id>/<int:video_id>', StarDelete.as_view(), name='star_delete'),


]
