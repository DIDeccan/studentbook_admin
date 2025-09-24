from django.contrib import admin
from .models import *
# Register your models here.
 
#user models register
 
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','email','phone_number', 'user_type',
                 'is_superuser', 'is_active']
    list_filter = ('user_type',)
 
 
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','email','phone_number', 'user_type','student_class']
 
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['id','name']
 
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id','name']
 
class StudentPackageAdmin(admin.ModelAdmin):
    list_display = ['id','student','course','price','subscription_taken_from','subscription_valid_till']
 
admin.site.register(User,UserAdmin)
admin.site.register(StudentPackage,StudentPackageAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Class,ClassAdmin)
 
#user models register end
 
 
#Subscription model registration
class SubscriptionOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course','price','payment_status']
 
admin.site.register(SubscriptionOrder,SubscriptionOrderAdmin)
 
 
#course models registrations
 
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course' ]
    list_filter = ['course',]
 
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'semester_name']
    # list_filter = ['course','subject']
 
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id','chapter_name' ,'semester' ,'course' ,'subject']
    list_filter = ['course','subject','semester']
 
class SubChapterAdmin(admin.ModelAdmin):
    list_display = ['id','subchapter' ,'parent_subchapter','chapter' ,'semester','course' ,'subject']
    list_filter = ['course','subject','semester','chapter']
 
 
 
class SubTopicAdmin(admin.ModelAdmin):
    list_display = ['id','subtopic_name','topic_name','chapter_name' ,'unit','subject','course']
    list_filter = ['course','subject','unit','chapter_name','topic_name']
   
class GeneralContentAdmin(admin.ModelAdmin):
    list_display = ['id','title',]
 
 
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Semester,SemesterAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(Subchapter,SubChapterAdmin)
admin.site.register(MainContent,GeneralContentAdmin)
 
 
#student dashboard models registration
# class VideoTrackingLogAdmin(admin.ModelAdmin):
#     list_display = ['id','student','subchapter','watched_duration','completed','created_at']
#     list_filter = ['student','subchapter','completed']  
 
 
# admin.site.register(VideoTrackingLog,VideoTrackingLogAdmin)
 
class GeneralContentVideoAdmin(admin.ModelAdmin):
 
    list_display = ['id','video_name','subtitle','main_content']
 
    list_filter = ['main_content']
 
 