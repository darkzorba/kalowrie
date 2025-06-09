from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['is_first_access'] = user.is_first_access
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['user_id'] = user.id
        token['diet_id'] = user.userdiet_set.filter(status=True).values_list('id',flat=True).first()

        return token
