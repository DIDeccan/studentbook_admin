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
from studentbookadminfrontend.models import Class, Subject, Semester, Chapter, Subchapter
import urllib.parse
from studentbookadminfrontend.models import GeneralContentVideo, MainContent



# Make sure this api_response function is defined somewhere in this file
def api_response(message, message_type, status_code, data=None):
    return Response(
        {
            "message": message,
            "message_type": message_type,
            "status_code": status_code,
            "data": data,
        },
        status=status_code,
    )


class UploadVideoAPIView(APIView):
    def post(self, request):
        video_file = request.FILES.get("video_file")
        class_id = request.data.get("class_id")
        subject_id = request.data.get("subject_id")
        semester_id = request.data.get("semester")  # Changed from "semester_id" to "semester"
        chapter_name = request.data.get("chapter_name")
        chapter_number = request.data.get("chapter_number")
        subchapter_number = request.data.get("subchapter")  # This was already correct
        video_name = request.data.get("video_name")
        tumbnail_image = request.FILES.get("tumbnail_image")
        subchapter_description = request.data.get("subchapter_description")  # 👈 Added


        if not all([video_file, class_id, subject_id, semester_id, chapter_name, subchapter_number, video_name,tumbnail_image]):
            return api_response("All fields are required.", "error", status.HTTP_400_BAD_REQUEST)

        try:
            student_class = Class.objects.get(id=class_id)
            subject = Subject.objects.get(id=subject_id,course=class_id )
            semester = Semester.objects.get(semester_number=semester_id)
        except (Class.DoesNotExist, Subject.DoesNotExist, Semester.DoesNotExist) as e:
            return api_response(f"Object not found: {str(e)}", "error", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return api_response(str(e), "error", status.HTTP_400_BAD_REQUEST)

        # ---------------- Save video temporarily ----------------
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name
        except Exception as e:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return api_response(f"Failed to save temp file: {str(e)}", "error", status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ------------------- Get video duration -------------------
        try:
            clip = VideoFileClip(temp_path)
            duration_seconds = int(clip.duration)
            minutes, seconds = divmod(duration_seconds, 60)
            video_duration = f"{minutes:02}:{seconds:02}"
            clip.close()
        except Exception as e:
            video_duration = None
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return api_response(f"Failed to get video duration: {str(e)}", "error", status.HTTP_400_BAD_REQUEST)

        # ------------------- Upload to S3 -------------------
        s3_key = f"vedios/{student_class.name}/{subject.name}/{semester.semester_name}/{chapter_name}/{subchapter_number}_{video_name}/{video_file.name}"
        encoded_key = urllib.parse.quote(s3_key)
        video_url = None
        print('AWS_ACCESS_KEY_ID',settings.AWS_ACCESS_KEY_ID)
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            s3.upload_file(temp_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
            video_url = f"{settings.MEDIA_URL}{encoded_key}"
        except Exception as e:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return api_response(f"Failed to upload to S3: {str(e)}", "error", status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)  # cleanup temp file

        # ------------------- Get or Create Chapter -------------------
        try:
            chapter, created = Chapter.objects.get_or_create(
                # chapter_name=chapter_name,
               
                chapter_number=chapter_number,
                course=student_class,
                subject=subject,
                semester=semester,
                defaults={"chapter_name":chapter_name}
            )
            if not created and chapter.chapter_name != chapter_name:
                chapter.chapter_name = chapter_name
                chapter.save()
        except Exception as e:
            return api_response(f"Failed to create/get chapter: {str(e)}", "error", status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ------------------- Get or Update Subchapter -------------------
        try:
            
            
            subchapter, created = Subchapter.objects.update_or_create(
                defaults={
                    "video_name": video_name,
                    "video_url": video_url,
                    "vedio_duration": video_duration,
                    "tumbnail_image":tumbnail_image,
                    "description": subchapter_description,  # 👈 Added

                },
                course=student_class,
                subject=subject,
                semester=semester,
                chapter=chapter,
                subchapter=subchapter_number,
            )

            if not created:
                progress_deleted_count, _ = VideoTrackingLog.objects.filter(
                    subchapter=subchapter
                ).delete()
                print(f"INFO: Video replaced. Deleted {progress_deleted_count} student tracking logs.")
            
        except Exception as e:
            return api_response(f"Failed to create/update subchapter: {str(e)}", "error", status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ------------------- Final Response -------------------
        return api_response(
            message="Video uploaded and subchapter updated successfully" if not created else "New subchapter created successfully",
            message_type="success",
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            data={
                "chapter": chapter.chapter_name,
                "chapter_number": chapter.chapter_number,
                "subchapter": subchapter.subchapter,
                "subchapter_id":subchapter.id,
                "video_name": subchapter.video_name,
                "video_url": subchapter.video_url,
                "video_duration": subchapter.vedio_duration,
                "subchapter_description": subchapter.description,  # 👈 Added
                "tumbnail_image":subchapter.tumbnail_image.url if subchapter.tumbnail_image else None
            }
        )

# class UploadVideoAPIView(APIView):
#     def post(self, request):
#         # ------------------- 1. Data Retrieval -------------------
#         video_file = request.FILES.get("video_file")
#         tumbnail_image = request.FILES.get("tumbnail_image")
        
#         class_id = request.data.get("class_id")
#         subject_id = request.data.get("subject_id")
#         semester_id = request.data.get("semester")
#         chapter_name = request.data.get("chapter_name")
#         chapter_number = request.data.get("chapter_number")
#         subchapter_number = request.data.get("subchapter")
#         video_name = request.data.get("video_name")
#         subchapter_description = request.data.get("subchapter_description")

#         # ------------------- 2. Validation and Object Lookup -------------------
#         if not all([video_file, class_id, subject_id, semester_id, chapter_name, subchapter_number, video_name, tumbnail_image]):
#             return api_response(
#                 message="All fields are required.", 
#                 message_type="error", 
#                 status_code=status.HTTP_400_BAD_REQUEST)

#         try:
#             student_class = Class.objects.get(id=class_id)
#             subject = Subject.objects.get(id=subject_id, course=class_id) 
#             semester = Semester.objects.get(semester_number=semester_id)
#         except (Class.DoesNotExist, Subject.DoesNotExist, Semester.DoesNotExist) as e:
#             return api_response(
#                 message=f"Object not found: {str(e)}", 
#                 message_type="error", 
#                 status_code=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return api_response(
#                 message=str(e), 
#                 message_type="error", 
#                 status_code=status.HTTP_400_BAD_REQUEST)

#         # ------------------- 3. Video Processing (Temp, Duration, S3 Upload) -------------------
#         temp_path = None
#         video_url = None
#         video_duration = None
        
#         try:
#             # Save video temporarily
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
#                 for chunk in video_file.chunks():
#                     temp_file.write(chunk)
#                 temp_path = temp_file.name
#         except Exception as e:
#             if temp_path and os.path.exists(temp_path):
#                 os.remove(temp_path)
#             return api_response(
#                 message=f"Failed to save temp file: {str(e)}", 
#                 message_type="error", 
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Get video duration
#             clip = VideoFileClip(temp_path)
#             duration_seconds = round(clip.duration)
#             minutes, seconds = divmod(duration_seconds, 60)
#             video_duration = f"{minutes:02}:{seconds:02}"
#             clip.close()
#         except Exception as e:
#             video_duration = None
#             if temp_path and os.path.exists(temp_path):
#                 os.remove(temp_path)
#             return api_response(
#                 message=f"Failed to get video duration: {str(e)}", 
#                 message_type="error", 
#                 status_code=status.HTTP_400_BAD_REQUEST)

#             # Upload to S3
#             s3_key = f"vedios/{student_class.name}/{subject.name}/{semester.semester_name}/{chapter_name}/{subchapter_number}_{video_name}/{video_file.name}"
#             encoded_key = urllib.parse.quote(s3_key)
#             s3 = boto3.client(
#                 "s3",
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                 region_name=settings.AWS_S3_REGION_NAME,
#             )
#             s3.upload_file(temp_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
#             video_url = f"{settings.MEDIA_URL}{encoded_key}"
            
#         except Exception as e:
#             return api_response(
#                 message=f"File processing/Upload error: {str(e)}", 
#                 message_type="error", 
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         finally:
#             if temp_path and os.path.exists(temp_path):
#                 os.remove(temp_path) # Cleanup temp file

#         # ------------------- 4. Get or Create Chapter -------------------
#         try:
#             chapter, created_ch = Chapter.objects.get_or_create(
#                 chapter_number=chapter_number,
#                 course=student_class,
#                 subject=subject,
#                 semester=semester,
#                 defaults={"chapter_name":chapter_name}
#             )
#             if not created_ch and chapter.chapter_name != chapter_name:
#                 chapter.chapter_name = chapter_name
#                 chapter.save()
#         except Exception as e:
#             return api_response(
#                 message=f"Failed to create/get chapter: {str(e)}", 
#                 message_type="error", 
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # ------------------- 5. Get or Update Subchapter (with Progress Deletion) -------------------
#         try:
#             subchapter_key_fields = {
#                 'course': student_class,
#                 'subject': subject,
#                 'semester': semester,
#                 'chapter': chapter,
#                 'subchapter': subchapter_number,
#             }
            
#             existing_subchapter = Subchapter.objects.filter(**subchapter_key_fields).first()
            
#             # 🔥 Check if Subchapter exists and delete old tracking data
#             if existing_subchapter:
#                 progress_deleted_count, _ = VideoTrackingLog.objects.filter(
#                     subchapter=existing_subchapter
#                 ).delete()
#                 print(f"INFO: Video replaced. Deleted {progress_deleted_count} student tracking logs.")
            
#             # Update or create the Subchapter record with new data
#             subchapter, created_sub = Subchapter.objects.update_or_create(
#                  **subchapter_key_fields,
#                  defaults={
#                      "video_name": video_name,
#                      "video_url": video_url,
#                      "vedio_duration": video_duration,
#                      "tumbnail_image": tumbnail_image, 
#                      "description": subchapter_description,
#                  }
#             )
            
#         except Exception as e:
#             return api_response(
#                 message=f"Failed to create/update subchapter: {str(e)}",
#                 message_type= "error", 
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # ------------------- 6. Final Response -------------------
#         thumbnail_url = subchapter.tumbnail_image.url if subchapter.tumbnail_image else None
        
#         return api_response(
#             message="Video uploaded and subchapter updated successfully" if not created_sub else "New subchapter created successfully",
#             message_type="success",
#             status_code=status.HTTP_201_CREATED if created_sub else status.HTTP_200_OK,
#             data={
#                 "chapter": chapter.chapter_name,
#                 "chapter_number": chapter.chapter_number,
#                 "subchapter": subchapter.subchapter,
#                 "subchapter_id": subchapter.id,
#                 "video_name": subchapter.video_name,
#                 "video_url": subchapter.video_url,
#                 "video_duration": subchapter.vedio_duration,
#                 "subchapter_description": subchapter.description,
#                 "tumbnail_image": thumbnail_url
#             }
#         )






class ChaptersWithSubchaptersAPI(APIView):

    def get(self, request, course_id, subject_id):

        chapters = Chapter.objects.filter(course_id=course_id, subject_id=subject_id).order_by("chapter_number")

        data = []
 
        for chapter in chapters:

            subchapters = Subchapter.objects.filter(chapter=chapter).order_by("subchapter")

            subchapter_data = [

                {

                    "id": sub.id,
                    "subchapter": sub.subchapter,
                    "video_name": sub.video_name,
                    "video_url": sub.video_url,
                    "video_duration": sub.vedio_duration,
                    "created_at":sub.created_at


                }

                for sub in subchapters

            ]
 
            data.append({

                "chapter_id": chapter.id,

                "chapter_name": chapter.chapter_name,

                "chapter_number": chapter.chapter_number,

                "subject": chapter.subject.name,

                "subject_id": chapter.subject.id,

                "class": chapter.course.name,
    
                "subchapters": subchapter_data

            })
 
        return Response(data, status=200)

 
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
    


# class ClassWIthSubjectsView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         classes = Class.objects.all().order_by('id')
#         data = []
#         for cls in classes:
#             subjects = Subject.objects.filter(course=cls.id).order_by('id')
#             subject_data = []
#             for subject in subjects:
#                 subject_data.append({
#                     'subject_id': subject.id,
#                     'subject_name': subject.name,
#                     # 'subject_image': subject.image.url if subject.image else None
#                 })
#             # subject_serializer = SubjectSerializer(subjects, many=True)
 
#             class_data = {
#                 'class_id': cls.id,
#                 'class_name': cls.name,
#                 'subjects': subject_data
#             }
#             data.append(class_data)
       
#         return api_response(
#             message="Classes with subjects fetched successfully",
#             message_type="success",
#             status_code=status.HTTP_200_OK,
#             data=data
#         )
 

class ClassListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    def get(self, request, format=None):
        classes = Class.objects.all().order_by('id')
        serializer = ClassSerializer(classes, many=True)  
        # OutstandingToken.objects.all().delete()
        # BlacklistedToken.objects.all().delete()
        return api_response(
            message="Class List Data.",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )
    
# class GeneralContentVideoAPIView(APIView):
#     # GET: Get a list of all general videos or a single video
#     def get(self, request, pk=None):
#         if pk:
#             try:
#                 video = GeneralContentVideo.objects.get(pk=pk)
#                 data = {
#                     "id": video.id,
#                     "video_name": video.video_name,
#                     "subtitle": video.subtitle,
#                     "main_content_id": video.main_content.id,
#                     "main_content_title": video.main_content.title,
#                     "description": video.discription,
#                     "video_url": video.video_url,
#                 }
#                 return api_response(
#                     message="Video fetched successfully",
#                     message_type="success",
#                     status_code=status.HTTP_200_OK,
#                     data={}
#                 )
#             # ("Video fetched successfully", "success", status.HTTP_200_OK, data)
#             except GeneralContentVideo.DoesNotExist:
#                 return api_response(
#                     message="Video not found",
#                     message_type="error",
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     data={}
#                 )
#             # ("Video not found", "error", status.HTTP_404_NOT_FOUND)
#         else:
#             videos = GeneralContentVideo.objects.all().order_by('video_name')
#             data = [{
#                 "id": v.id,
#                 "video_name": v.video_name,
#                 "main_content_title": v.main_content.title,
#                 "video_url": v.video_url,
#                 "subtitle": v.subtitle,
#             } for v in videos]
#             return api_response(
#                 message="Videos fetched successfully",
#                 message_type="success",
#                 status_code=status.HTTP_200_OK,
#                 data={}
#                 # ("Videos fetched successfully", "success", status.HTTP_200_OK, data)
#             )

#     # POST: Create a new general video
#     def post(self, request):
#         video_name = request.data.get('video_name')
#         subtitle = request.data.get('subtitle')
#         main_content_id = request.data.get('main_content_id')
#         description = request.data.get('discription') # Corrected from 'description' to 'discription'
#         video_file = request.data.get('video_file')

#         if not all([video_name, main_content_id, video_file]):
#             return api_response(
#                 message="Required fields (video_name, main_content_id, video_url) are missing",
#                 message_type="error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 data={}
#         # ("Required fields (video_name, main_content_id, video_url) are missing", "error", status.HTTP_400_BAD_REQUEST)
#             )
        
#         try:
#             main_content = MainContent.objects.get(id=main_content_id)
#         except MainContent.DoesNotExist:
#             return api_response(
#                 message="MainContent with this ID does not exist",
#                 message_type="error",
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 data={}
#                 # "MainContent with this ID does not exist", "error", status.HTTP_404_NOT_FOUND
#             )

#         video = GeneralContentVideo.objects.create(
#             video_name=video_name,
#             subtitle=subtitle,
#             main_content=main_content,
#             discription=description,
#             video_file=video_file,
#         )
#         data = {
#             "id": video.id,
#             "video_name": video.video_name,
#             "video_url": video.video_url,
#         }
#         return api_response(
#             message="Video created successfully",
#             message_type="error",
#             status_code=status.HTTP_404_NOT_FOUND,
#             data={}
#         )
#     # ("Video created successfully", "success", status.HTTP_201_CREATED, data)

class GeneralContentVideoAPIView(APIView):
    # GET: Get a list of all general videos or a single video
    def get(self, request, pk=None):
        if pk:
            try:
                video = GeneralContentVideo.objects.get(pk=pk)
                data = {
                    "id": video.id,
                    "video_name": video.video_name,
                    "subtitle": video.subtitle,
                    "main_content_id": video.main_content.id,
                    "main_content_title": video.main_content.title,
                    "description": video.discription,
                    "video_url": video.video_url,
                }
                return api_response(
                    # "Video fetched successfully", "success", status.HTTP_200_OK, data
                    message="Video uploaded and saved successfully",
                    message_type="success",
                    status_code=status.HTTP_201_CREATED,
                    data=data
                )
            
            except GeneralContentVideo.DoesNotExist:
                return api_response(
                    # "Video not found", "error", status.HTTP_404_NOT_FOUND
                    message="Video not found",
                    message_type="error",
                    status_code=status.HTTP_404_NOT_FOUND,
                    data=data
                )
            
        else:
            videos = GeneralContentVideo.objects.all().order_by('video_name')
            data = [{
                "id": v.id,
                "video_name": v.video_name,
                "main_content_title": v.main_content.title,
                "video_url": v.video_url,
                "subtitle": v.subtitle,
            } for v in videos]
            return api_response(
                # "Videos fetched successfully", "success", status.HTTP_200_OK, data
                    message="Video frtched successfully",
                    message_type="success",
                    status_code=status.HTTP_200_OK,
                    data=data
            )

    # POST: Create a new general video with S3 upload
    def post(self, request):
        video_file = request.FILES.get("video_file")
        video_name = request.data.get('video_name')
        subtitle = request.data.get('subtitle')
        main_content_id = request.data.get('main_content_id')
        description = request.data.get('description')
        tumbnail_image = request.FILES.get("tumbnail_image")

 

        if not all([video_file, video_name, main_content_id]):
            return api_response(
                # "Required fields (video_file, video_name, main_content_id) are missing", "error", status.HTTP_400_BAD_REQUEST
                message="Required fields (video_file, video_name, main_content_id) are missing",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            main_content = MainContent.objects.get(id=main_content_id)
        except MainContent.DoesNotExist:
            return api_response(
                # "MainContent with this ID does not exist", "error", status.HTTP_404_NOT_FOUND
                message="MainContent with this ID does not exist",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        temp_path = None
        video_url = None
        video_duration = None
        
        try:
            # 1. Save video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name

            # 2. Get video duration
            clip = VideoFileClip(temp_path)
            duration_seconds = round(clip.duration)
            minutes, seconds = divmod(duration_seconds, 60)
            video_duration = f"{minutes:02}:{seconds:02}"
            clip.close()

            # 3. Upload to S3
            s3_key = f"vedios/{main_content.title}/{video_name}_{video_file.name}"
            encoded_key = urllib.parse.quote(s3_key)
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            s3.upload_file(temp_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
            video_url = f"{settings.MEDIA_URL}{encoded_key}"

            # 4. Create the database record
            video = GeneralContentVideo.objects.create(
                video_name=video_name,
                subtitle=subtitle,
                main_content=main_content,
                discription=description,
                video_url=video_url,
                vedio_duration = video_duration,
                tumbnail_image = tumbnail_image
                # created_at = 
                # Add a field for duration in the model if you need to save it
            )

            data = {
                "id": video.id,
                "video_name": video.video_name,
                "video_url": video.video_url,
                "video_duration": video_duration,
                "tumbnail_image": video.tumbnail_image.url if video.tumbnail_image and video.tumbnail_image.name else None,
                "description":description,
            }
            return api_response(
                # "Video uploaded and saved successfully", "success", status.HTTP_201_CREATED, data
                message="Video uploaded and saved successfully",
                message_type="success",
                status_code=status.HTTP_201_CREATED,
                data=data
            )
        
        except Exception as e:
            return api_response(
                # f"An error occurred: {str(e)}", "error", status.HTTP_500_INTERNAL_SERVER_ERROR
                message=f"An error occurred: {str(e)}",
                message_type="errror",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path) # Cleanup temp file








