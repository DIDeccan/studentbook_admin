from studentbookadminfrontend.models import *
from rest_framework import serializers



class LearningVideoSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(read_only=True)
    # class_id = 
    class Meta:
        model = Subchapter
        fields = ["course", "subject", "semester", "chapter", "subchapter", "video_name", "video_url", "created_at"]
 
 
 