from django.urls import path
from studentbookadminfrontend.views.content_management_views import *
# from studentbookadminfrontend.views.content_management_views import GeneralContentVideoAPIView
 
urlpatterns = [

    path("video_upload", UploadVideoAPIView.as_view(), name="video-upload"),
    # path("videos/<int:class_id>/<int:subject_id>/<int:semester>/<int:chapter>/",ChapterVideosAPIView.as_view(),name="chapter-videos"),
    path("videos/<int:course_id>/<int:subject_id>",ChaptersWithSubchaptersAPI.as_view(),name="chapter-videos"),
    # path("classes_with_subjects/", ClassWIthSubjectsView.as_view()),
    path('class_list', ClassListAPIView.as_view()),
    # This URL handles GET (list) and POST (create)
    path('general_videos', GeneralContentVideoAPIView.as_view(), name='general-video-list'),
    # This URL handles GET (detail)
    path('general_videos/<int:pk>/', GeneralContentVideoAPIView.as_view(), name='general-video-detail'),
    # This URL handles general_content_id (dropdown)
    path('general_content/', MainContentAPIView.as_view())


]