from rest_framework.serializers import ModelSerializer
from .models import CodePaste, UserProfile,UserSettings

class UserProfileSerializer(ModelSerializer):

    class Meta:
        model=UserProfile
        fields=[
            'website_url',
            'location',
            'avatar'
        ]


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model=UserSettings
        fields=[
            'defaultSyntax',
            'defaultExpiration',
            'nightMode',
            'defaultExposure'
        ]


class PasteSerializer(ModelSerializer):
    class Meta:
        models=CodePaste
        fields=[
            'paste_uuid',
            'title',
            'code',
           
            'created',
            'public',
            'expiration',
            'language',
            'syntax_highlighting',
            'password',
        ]     