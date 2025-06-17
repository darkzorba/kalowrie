from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    user_type = serializers.CharField(write_only=True)

    def validate(self, attrs):

        data = super().validate(attrs)

        user = self.user

        if user.user_type != attrs.get('user_type'):
            raise AuthenticationFailed('Error trying to authenticate user.')

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['is_first_access'] = user.is_first_access
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['user_id'] = user.id
        token['diet_id'] = user.userdiet_set.filter(status=True).values_list('id',flat=True).first()
        token['user_type'] = user.user_type
        token['team_id'] = user.team_id

        return token
