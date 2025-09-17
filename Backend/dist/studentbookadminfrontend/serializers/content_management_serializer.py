from studentbookadminfrontend.models import *
from rest_framework import serializers



# class LearningVideoSerializer(serializers.ModelSerializer):
#     video_url = serializers.URLField(read_only=True)
#     # class_id = 
#     class Meta:
#         model = Subchapter
#         fields = ["course", "subject", "semester", "chapter", "subchapter", "video_name", "video_url", "created_at"]
 
 
  
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ["chapter_name", "chapter_number", "description", "course", "subject", "semester"]
 
class SubchapterSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(read_only=True)
    class Meta:
        model = Subchapter
        fields = ["subchapter", "video_name", "video_url", "vedio_duration"]
 
class ChapterWithSubchaptersSerializer(serializers.ModelSerializer):
    subchapters = SubchapterSerializer(many=True)
    
 
    class Meta:
        model = Chapter
        fields = ["chapter_name", "chapter_number", "description", "course", "subject", "semester", "subchapters"]
 
    def create(self, validated_data):
        subchapters_data = validated_data.pop("subchapters")
        chapter = Chapter.objects.create(**validated_data)
 
        for sub in subchapters_data:
            Subchapter.objects.create(chapter=chapter, **sub)
 
        return chapter

 
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']


 


 