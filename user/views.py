from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers.LoginSerializer import LoginSerializer
from user.serializers.UserSerializer import UserSerializer
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from user.models import User
# http://127.0.0.1:8000/api/login
class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            if not User.objects.filter(username=data['username'],role=data['role']).exists():
                error_response = {
                    'status': 400,
                    'error': 'invalid_role',
                    'message': 'Invalid role provided',
                }
                return Response(error_response, status=400)
            
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                username = data['username']
                password = data['password']
                user = authenticate(username=username, password=password)
                if user is None:
                    error_response = {
                        'status': 400,
                        'error': 'invalid_password',
                        'message': 'Invalid password',
                        'data': {}
                    }
                    return Response(error_response, status=400)
                if Token.objects.filter(user=user).exists():
                    Token.objects.get(user=user).delete()
                token=Token.objects.create(user=user)
                # refresh = RefreshToken.for_user(user)

                success_response = {
                    'user': UserSerializer(user, many=False).data,
                    'Token': token.key,
                }
                return Response(success_response)


            else:
                error_response = {
                    'status': 400,
                    'error': 'invalid_data',
                    'message': 'Invalid data',
                    'data': {}
                }
                return Response(error_response, status=400)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)