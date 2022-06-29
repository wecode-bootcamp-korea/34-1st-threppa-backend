import json
import bcrypt
import jwt

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.conf            import settings

from users.models           import User
from users.validator        import validate_email, validate_password

class SighUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            username     = data['username']
            first_name   = data['first_name']
            last_name    = data['last_name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
    
            # TODO : validate logic -> OOP refactoring

            validate_email(email)
            validate_password(password)
                
            if User.objects.filter(email = email).exists():
                return  JsonResponse( {"message" : "Email Already Exists"}, status = 400)

            if User.objects.filter(username = username).exists():
                return  JsonResponse( {"message" : "USERNAME Already Exists"}, status = 400)

            if User.objects.filter(phone_number = phone_number).exists():
                return  JsonResponse( {"message" : "PHONE_NUMBER Already Exists"}, status = 400)

            hashed_password_decoded  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                username     = username,
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                password     = hashed_password_decoded,                    
                phone_number = phone_number
            )

            return JsonResponse({"message": "SIGHUP SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

        except ValidationError as error:
            return JsonResponse({"message" : error.message}, status = 400)

class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            validate_email(email)

            user = User.objects.get(email = email)

            if not bcrypt.checkpw(user.password.encode('utf-8'), password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({"access_token" : access_token}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 404)
