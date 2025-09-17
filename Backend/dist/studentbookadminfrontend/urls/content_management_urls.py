from django.urls import path
from studentbookadminfrontend.views.content_management_views import *
 
urlpatterns = [

    path("video_upload", UploadVideoAPIView.as_view(), name="video-upload"),
    # path("videos/<int:class_id>/<int:subject_id>/<int:semester>/<int:chapter>/",ChapterVideosAPIView.as_view(),name="chapter-videos"),
    path("videos/<int:course_id>/<int:subject_id>",ChaptersWithSubchaptersAPI.as_view(),name="chapter-videos"),
    # path("classes_with_subjects/", ClassWIthSubjectsView.as_view()),
    path('class_list', ClassListAPIView.as_view()),

 
]
 
 