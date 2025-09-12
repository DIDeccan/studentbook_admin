from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
import boto3, uuid
from studentbookadminbackend import settings
from studentbookadminfrontend.serializers.content_management_serializer import *
from studentbookadminfrontend.views.dashboard_views import api_response
from moviepy.editor import VideoFileClip  # Import VideoFileClip
import tempfile
import os


# class UploadVideoAPIView(APIView):
#     def post(self, request):
#         video_file = request.FILES.get("video_file")   # Uploaded file
#         class_id = request.data.get("class_id")
#         subject_id = request.data.get("subject_id")
#         semester_id = request.data.get("semester")
#         chapter_id = request.data.get("chapter")
#         subchapter = request.data.get("subchapter")
#         video_name = request.data.get("video_name")
 
#         if not video_file:
#             return api_response(
#             message="No file uploaded",
#             message_type="error",
#             status_code=status.HTTP_400_BAD_REQUEST,
       
#         )
#         # Response({"error": "No file uploaded"}, status=400)
        
#         if not all([class_id, subject_id, semester_id, chapter_id, subchapter, video_name]):
#             return api_response(
#                 message="All fields are required.",
#                 message_type="error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         # Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             student_class = Class.objects.get(id=class_id)
#         except Class.DoesNotExist:
#             return api_response(
#                 message="Invalid class ID",
#                 message_type="error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         # Response({"error": "Invalid class ID"}, status=400)

#         try:
#             subject = Subject.objects.get(id=subject_id)
#         except Subject.DoesNotExist:
#             return api_response(
#                 message="Invalid subject ID",
#                 message_type="error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         # Response({"error": "Invalid subject ID"}, status=400)

#         try:
#             semester = Semester.objects.get(id=semester_id)
#         except Semester.DoesNotExist:
#             return api_response(
#                 message="Invalid semester ID",
#                 message_type="error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         # Response({"error": "Invalid semester ID"}, status=400)

#         try:
#             chapter = Chapter.objects.get(id=chapter_id)
#         except Chapter.DoesNotExist:
#             return api_response(
#                 message="Invalid chapter ID",
#                 message_type="eror",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#             )
#         # Response({"error": "Invalid chapter ID"}, status=400)
#         # Build S3 path
#         s3_key = f"{student_class.name}/{subject.name}/{semester.semester_name}/{chapter.chapter_name}/{subchapter}{video_name}/{video_file.name}"
 
#         # Upload to S3
#         s3 = boto3.client(
#             "s3",
#             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_S3_REGION_NAME,
#         )
 
#         s3.upload_fileobj(video_file, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
 
#         # Final video URL
#         video_url = f"{settings.MEDIA_URL}{s3_key}"
 
#         # Save in DB
#         data = {
#             "course": student_class.id,
#             "subject": subject.id,
#             "semester": semester.id,
#             "chapter": chapter.id,
#             "subchapter": subchapter,
#             "video_name": video_name,
#             "video_url": video_url,
 
#         }
#         serializer = LearningVideoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(video_url=video_url)

#             return api_response(
#                 message="Video uploaded successfully",
#                 message_type="sucess",
#                 status_code=status.HTTP_201_CREATED,
#                 data=serializer.data
#             )
            
#             # return Response({
#             #     "message": "Video uploaded successfully",
#             #     "data": serializer.data
#             # }, status=status.HTTP_201_CREATED)
#             # Response(serializer.errors, status=400)
#         return api_response(
#             message=serializer.errors,
#             message_type="error",
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )
 

class UploadVideoAPIView(APIView):
    def post(self, request):
        video_file = request.FILES.get("video_file")
        class_id = request.data.get("class_id")
        subject_id = request.data.get("subject_id")
        semester_id = request.data.get("semester")
        chapter_id = request.data.get("chapter")
        subchapter = request.data.get("subchapter")
        video_name = request.data.get("video_name")

        if not video_file:
            return api_response(
                message="No file uploaded",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not all([class_id, subject_id, semester_id, chapter_id, subchapter, video_name]):
            return api_response(
                message="All fields are required.",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            student_class = Class.objects.get(id=class_id)
            subject = Subject.objects.get(id=subject_id)
            semester = Semester.objects.get(id=semester_id)
            chapter = Chapter.objects.get(id=chapter_id)
        except Exception as e:
            return api_response(
                message=str(e),
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # ------------------- Save to temp file -------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        # ---------------------------------------------------------

        # Build S3 path
        s3_key = f"{student_class.name}/{subject.name}/{semester.semester_name}/{chapter.chapter_name}/{subchapter}{video_name}/{video_file.name}"

        # Upload to S3 using temp file
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        s3.upload_file(temp_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

        # Final video URL
        video_url = f"{settings.MEDIA_URL}{s3_key}"

        # ------------------- Get duration -------------------
        try:
            clip = VideoFileClip(temp_path)
            duration_seconds = round(clip.duration, 2)
            clip.close()
        except Exception as e:
            # If any error occurs, set duration to 0 or None
            duration_seconds = 0
            return api_response(
                message= str(e),
                message_type='error',
            )
        finally:
            os.remove(temp_path)  # cleanup temp file
        # ----------------------------------------------------

        # Save in DB
        data = {
            "course": student_class.id,
            "subject": subject.id,
            "semester": semester.id,
            "chapter": chapter.id,
            "subchapter": subchapter,
            "video_name": video_name,
            "video_url": video_url,
        }
        serializer = LearningVideoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(video_url=video_url)

            return api_response(
                message="Video uploaded successfully",
                message_type="success",
                status_code=status.HTTP_201_CREATED,
                data={**serializer.data, "duration_seconds": duration_seconds}
            )

        return api_response(
            message=serializer.errors,
            message_type="error",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

 
class ChapterVideosAPIView(APIView):
    def get(self, request, class_id, subject_id, semester, chapter):
        # Fetch videos that match given filters
        videos = Subchapter.objects.filter(
            class_id=class_id,
            subject_id=subject_id,
            semester=semester,
            chapter=chapter
        )
 
        # Group videos by subchapter
        grouped = {}
        for video in videos:
            if video.subchapter not in grouped:
                grouped[video.subchapter] = {
                    "subchapter": video.subchapter,
                    # "parent_subchapter": video.parent_subchapter,
                    "videos": []
                }
            grouped[video.subchapter]["videos"].append({
                "id": video.id,
                "video_name": video.video_name,
                "video_url": video.video_url
            })
 
        # Convert dict → list
        response_data = {
            "class_id": class_id,
            "subject_id": subject_id,
            "semester": semester,
            "chapter": chapter,
            "subchapters": list(grouped.values())
        }
        return api_response(
            message=response_data,
            message_type="sucess",
            status_code=status.HTTP_201_CREATED
        )
        # Response(response_data)
    


class ClassWIthSubjectsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        classes = Class.objects.all().order_by('id')
        data = []
        for cls in classes:
            subjects = Subject.objects.filter(course=cls.id).order_by('id')
            subject_data = []
            for subject in subjects:
                subject_data.append({
                    'subject_id': subject.id,
                    'subject_name': subject.name,
                    # 'subject_image': subject.image.url if subject.image else None
                })
            # subject_serializer = SubjectSerializer(subjects, many=True)
 
            class_data = {
                'class_id': cls.id,
                'class_name': cls.name,
                'subjects': subject_data
            }
            data.append(class_data)
       
        return api_response(
            message="Classes with subjects fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=data
        )
 
 