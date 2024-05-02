from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *


class SignUpView(GenericAPIView):
    serializer_class  = SignUpSerializer
    def post(self, request):
        user_information = request.data
        serializer = self.get_serializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        code_verivecation = generate_code()
        user_data['id'] = user.id
        if request.data['type_verified'] == 'email':
            print('heloo')
            code = VerificationCode.objects.create(user=user, code=code_verivecation)
            data= {'to_email':user.email, 'email_subject':'code verify for account','username':user.username, 'code': str(code_verivecation)}
            Utlil.send_email(data)
        # tokens = {
        #     'refresh':str(token),
        #     'accsess':str(token.access_token)
        # }
        return Response({'information_user':user_data}, status=status.HTTP_201_CREATED)

class VerifyAccount(GenericAPIView):

    def post(self, request, pk):
        user = CustomUser.objects.filter(pk=pk).first()
        code = request.data['code']
        print(code)
        try:
            user_code = VerificationCode.objects.get(user=user)
            print(user_code)
            if user_code.code == int(code):
                if timezone.now() > user_code.expires_at:
                    return Response("الرجاء اعادة طلب الرمز من جديد نظرا لأن الرمز المدخل انتهت صلاحيته")
                user.is_verified = True
                user.save()
                user_code.delete()
                return Response("تم تأكيد حسابك يمكنك الآن المتابعة وتسجيل الدخول")
        except:
            return Response("الرجاء اعادة طلب الرمز من جديد")
            

class LoginUser(GenericAPIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['image'] = request.build_absolute_uri(user.image.url)
        data['id'] = user.id
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)
    
class LogoutUser(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
######### needs modification to adapt to sms
class SendCodePassword(GenericAPIView):
    def post(self, request):
        try: 
            email = request.data['email']
            user = get_object_or_404(CustomUser, email=email)
            existing_code = VerificationCode.objects.filter(user=user).first()
            if existing_code:
                existing_code.delete()
            code_verivecation = generate_code()
            code = VerificationCode.objects.create(user=user, code=code_verivecation)
            data= {'to_email':user.email, 'email_subject':'code verify for reset password','username':user.username, 'code': str(code_verivecation)}
            Utlil.send_email(data)
            return Response({'message':'تم ارسال رمز التحقق',
                             'user_id' : user.id})
        except:
            raise serializers.ValidationError("الرجاء ادخال الرقم بشكل صحيح")
        
class VerifyCode(GenericAPIView):

    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = VerificationCode.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response("الرجاء اعادة طلب الرمز من جديد نظرا لأن الرمز المدخل انتهت صلاحيته", status=status.HTTP_400_BAD_REQUEST)
                code_ver.is_verified = True
                code_ver.save()
                return Response({"message":"تم التحقق من الرمز", 'user_id':code_ver.user.id},status=status.HTTP_200_OK)
            else:
                return Response('الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح')
        else:
            return Response("الرجاء اعادة طلب الرمز من جديد")

######### needs modification to adapt to sms
class ResetPassword(UpdateAPIView):
    serializer_class = ResetPasswordSerializer

    def put(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        code = VerificationCode.objects.filter(user=user).first()
        if not code:
            return Response("الرجاء اعادة طلب الرمز من جديد")
        if code.is_verified:
            data = request.data
            serializer = self.get_serializer(data=data, context={'user_id':user_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            code.delete()
            messages = {
                'message':'تم تغيير كلمة المرور بنجاح'
            }
            return Response(messages, status=status.HTTP_200_OK)
        
        else:
            return Response({'error':'ليس لديك صلاحية لتغيير كلمة المرور'})
        
class CreateObjectionView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ObjectionSerializer

    def post(self, request):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data, context={'user':user, 'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        objection = user.objection_set.all()
        serializer = self.get_serializer(objection, many=True)
        return Response(serializer.data)
    

class RetUpdDesObjectionView(RetrieveUpdateDestroyAPIView):
    queryset = Objection.objects.all()
    serializer_class = ObjectionSerializer
    permission_classes = [IsAuthenticated,]


class RefuselObjectionView(GenericAPIView):
    serializer_class = RefuselObjectionSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        refusel_obj = RefuselObjection.objects.filter(objection__user=user)
        serializer = self.get_serializer(refusel_obj, many=True)
        return Response(serializer.data)
    
class CreateChoiceSubjectView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShoiceSubjectSerializer

    def post(self, request):
        user = request.user
        data = request.data
        serializer = self.get_serializer(data=data, context={'user':user, 'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        objection = user.shoicesubject_set.all()
        serializer = self.get_serializer(objection, many=True)
        return Response(serializer.data)
    
class RetUpdDesObjectionView(RetrieveUpdateDestroyAPIView):
    queryset = ShoiceSubject.objects.all()
    serializer_class = ShoiceSubjectSerializer
    permission_classes = [IsAuthenticated,]