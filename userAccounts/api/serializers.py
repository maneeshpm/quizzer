from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField,
)

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                    username = username,
                    email = email,
                )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=False, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }
    
    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        
        if not username:
            raise ValidationError('Username required')
        
        user = User.objects.filter(Q(username=username)).distinct()
        print(user)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("invalid username")
        
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("incorrect credentials")
        
        utoken = None
        try:
            utoken = Token.objects.get(user=user_obj)
        except Token.DoesNotExist:
            utoken = Token.objects.create(user=user_obj)
        data['token'] = utoken
        return data

