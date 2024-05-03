from rest_framework import serializers
from django.contrib.auth import  authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    confpassword = serializers.CharField(write_only = True)
    type_verified = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'univercity_id', 'type_verified', 'password', 'confpassword']
        extra_kwargs = {
            'password':{'write_only':True,},
            'confpassword': {'write_only':True}
        }
    def validate(self, validated_data):
        validate_password(validated_data['password'])
        validate_password(validated_data['confpassword'])
        if validated_data['password'] != validated_data['confpassword'] :
            raise serializers.ValidationError("password and confpassword didn't match")
        return validated_data

    def create(self, validated_data):
        validated_data.pop('confpassword', None)
        validated_data.pop('type_verified')
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect Credentials")
            if not user.is_active:
                raise serializers.ValidationError({'message_error':'this account is not active'})
            if not user.is_verified:
                raise serializers.ValidationError({'message_error':'this account is not verified'})
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data
    
    
class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ResetPasswordSerializer(serializers.Serializer):
    newpassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password', '')
        newpassword = attrs.get('newpassword', '')
        validate_password(password)
        validate_password(newpassword)
        if password != newpassword:
            raise serializers.ValidationError('كلمات المرور غير متطابقة')
        
        return attrs

    def save(self, **kwargs):
        user_id = self.context.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        password = self.validated_data['newpassword']
        user.set_password(password)
        user.save()
        return user
    

class ObjectionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    univercity_id = serializers.IntegerField(source='user.univercity_id', read_only=True)

    class Meta:
        model = Objection
        fields = '__all__'

    def create(self, validated_data):
        chapter_id = validated_data.pop('chapter').id
        chapter = Chapter.objects.get(id=chapter_id)
        if chapter.end_at >= timezone.datetime.now().date():
            user = self.context.get('user')
            validated_data['user'] = user
            validated_data['chapter'] = chapter
            instance = Objection.objects.create(**validated_data)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("الوقت المخصص لتقديم طلبات الإعتراض انتهى")
    
    def update(self, instance, validated_data):
        chapter_id = validated_data.pop('chapter').id
        chapter = Chapter.objects.get(id=chapter_id)
        if chapter.end_at >= timezone.datetime.now().date():
            validated_data['chapter'] = chapter
            for attrs, value in validated_data.items():
                setattr(instance, attrs, value)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("الوقت المخصص لتقديم طلبات الإعتراض انتهى")

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['chapter'] = instance.chapter.chapter
        return repr
    
class RefuselObjectionSerializer(serializers.ModelSerializer):
    objection = ObjectionSerializer(read_only=True)
    
    class Meta:
        model = RefuselObjection
        fields = '__all__'

class ShoiceSubjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    univercity_id = serializers.IntegerField(source='user.univercity_id', read_only=True)

    class Meta:
        model = ShoiceSubject
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['user'] = user
        instance = ShoiceSubject.objects.create(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)
        instance.save()
        return instance
    
class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def to_representation(self, instance):
        username = self.context.get('user', '')
        repr = super().to_representation(instance)
        repr['user'] = [user.username for user in instance.user.filter(username=username)]
        return repr