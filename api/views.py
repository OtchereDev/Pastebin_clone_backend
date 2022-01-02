from api.serializers import UserProfileSerializer, UserSettingsSerializer
from django.core.exceptions import ValidationError
from django.core import serializers
from django.http.response import  HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from api.models import CodeFolder, CodePaste, UserProfile, UserSettings
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

class NewPaste(APIView):
    def post(self,request,*args, **kwargs):
        data=request.data

        # user=request.user
        print(request.user.is_authenticated)

        
        try:
            newPaste=CodePaste.objects.create(title=data['title'],
                                    code=data['code'],
                                    
                                    public=data['public'],
                                    expiration=data['expiration'],
                                    language=data['language'],
                                    syntax_highlighting=data['syntax_highlighting'],
                                    password=data['password'],
                                    )

            if data.get('folder') and request.user.is_authenticated :
                folder=CodeFolder.objects.get_or_create(user=request.user,name=data['folder'])
                print(folder)
                newPaste.folder=folder[0]
                newPaste.save()
            

            if request.user.is_authenticated :
                newPaste.user=request.user
                newPaste.save()

            return JsonResponse({'message':'successfully created','uuid':newPaste.paste_uuid})
                
        except Exception as e: 
            print(e)

            return HttpResponseBadRequest()


class UpdatePaste(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args, **kwargs):
        data=request.data

        uuid=kwargs['uuid']

        # if request.user.is_authenticated :
        #     return HttpResponseForbidden()

        user=request.user
        print('data',data)

        try:
            # print('here')
            data.pop('user',None)
            
            paste = CodePaste.objects.get(paste_uuid=uuid,user=user)
            # print(paste)
            # for i in data.keys():
            #     print(i,data[i],paste.i)
            #     paste.i=data[i]

            if data.get("title"):
                paste.title=data["title"]
            if data.get("code"):
                paste.code=data['code']
                # print(data["code"])
            if data.get("public") != None:
                paste.public=data["public"]
                print("here")
            if data.get("expiration"):
                paste.expiration=data['expiration']
            if data.get("language"):
               
                paste.language=data['language']
            if data.get("syntax_highlighting") != None:
                paste.syntax_highlighting=data['syntax_highlighting']
            if data.get("password"):
                paste.password=data['password']
            if data.get("folder"):
                folder=CodeFolder.objects.get_or_create(data['folder'])
                paste.folder=folder[0]
            
            paste.save()
            # print(paste.code)

            data=serializers.serialize('json',[paste,])

            data=json.loads(data)

            if paste.folder:
                # print(paste.folder.name)

                data[0]['fields']['folder']=paste.folder.name
            

            # print(paste.user,request.user)
            if request.user.is_authenticated and paste.user==request.user:
                
                data[0]['fields']['read_only']=False
    
            else:
                data[0]['fields']['read_only']=True

            return JsonResponse({
                'data':data[0]['fields']
            })


            # return JsonResponse({'message':'successfully updated'})
        
        except CodePaste.DoesNotExist:
            return HttpResponseNotFound()
            
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()


class DeletePaste(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args, **kwargs):
        uuid=kwargs['uuid']

        user=request.user

        try:
            paste = CodePaste.objects.get(paste_uuid=uuid,user=user)

            paste.delete()

            return JsonResponse({'detail':'success'})

        except CodePaste.DoesNotExist:
            print('not_forund')
            return HttpResponseNotFound()

        except:
            return HttpResponseBadRequest()


class RetrievePaste(APIView):
    def get(self,request,*args, **kwargs):
        try:
            uuid=kwargs['uuid']

            object=CodePaste.objects.get(paste_uuid=uuid)


            # if object.password:
            #     raise ValidationError('password required')

            data=serializers.serialize('json',[object,])

            data=json.loads(data)

            if object.folder:
                print(object.folder.name)

                data[0]['fields']['folder']=object.folder.name
            

            print(object.user,request.user)
            if request.user.is_authenticated and object.user==request.user:
                
                data[0]['fields']['read_only']=False
    
            else:
                data[0]['fields']['read_only']=True

            return JsonResponse({
                'data':data[0]['fields']
            })

        except CodePaste.DoesNotExist:
            return HttpResponseNotFound()
        except ValidationError:
            return HttpResponseForbidden('password required')
        except:
            return HttpResponseBadRequest()

    def post(self,request,*args, **kwargs):
        try:
            password=request.data['password']
            uuid=kwargs['uuid']

            object=CodePaste.objects.get(paste_uuid=uuid)

            if object.password != password:
                raise ValidationError('password incorrect')

            data=serializers.serialize('json',[object,])

            return JsonResponse({
                'data':json.loads(data)
            })

        except CodePaste.DoesNotExist:
            return HttpResponseNotFound()
        except ValidationError:
            return HttpResponseForbidden('password incorrect')
        except:
            return HttpResponseBadRequest()    


class Top10Paste(APIView):
    def get(self,request,*args, **kwargs):
        data=CodePaste.objects.filter(Q(public=True,password='') |Q(public=True,password=None)).values()[:10]
        # print(data)
        return JsonResponse({
            'top_paste':list(data)
        })

        
class NewFolder(APIView):
    def post(self,request,*args, **kwargs):
        try:
            
            name=request.data['name']

            if not request.user.is_authenticated:
                return HttpResponseForbidden()

            user=request.user

            folder=CodeFolder.objects.create(name=name,user=user)

            return JsonResponse({'message':'successfully created'}) 

        except KeyError:
            return HttpResponseBadRequest('folder name is required')
        except:
            return HttpResponseBadRequest()


class RetrieveUserCodeFolder(APIView):
    def get(self,request,*args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        user=request.user
        folders=CodeFolder.objects.filter(user=user).values()
        
        return JsonResponse({
            'folders':list(folders)
        })

class UpdateCodeFolder(APIView):
    def post(self,request,*args, **kwargs):
        data=request.data

        uuid=kwargs['uuid']

        if request.user.is_authenticated :
            return HttpResponseForbidden()

        user=request.user

        try:
            data.pop('user',None)
            paste = CodeFolder.objects.get(folder_uuid=uuid,user=user)
           
            for i in data.keys():
                paste[i]=data[i]
            
            paste.save()

            return JsonResponse({'message':'successfully updated'})
        
        except CodeFolder.DoesNotExist:
            return HttpResponseNotFound()
            
        except:
            return HttpResponseBadRequest()


class DeleteCodeFolder(APIView):
    def post(self,request,*args, **kwargs):
        uuid=kwargs['uuid']

        if request.user.is_authenticated :
            return HttpResponseForbidden()

        user=request.user

        try:
            folder = CodeFolder.objects.get(folder_uuid=uuid,user=user)

            folder.delete()

        except CodeFolder.DoesNotExist:
            return HttpResponseNotFound()

        except:
            return HttpResponseBadRequest()


class RetrieveUserCodeFolderContent(APIView):
    def get(self,request,*args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return HttpResponseForbidden()

            uuid=kwargs['uuid']

            user=request.user
            folder=CodeFolder.objects.get(user=user,folder_uuid=uuid)

            code_pastes=folder.codepaste_set.all().values()
            
            return JsonResponse({
                'folder_paste':list(code_pastes)
            })

        except KeyError:
            return HttpResponseForbidden()
        except CodeFolder.DoesNotExist:
            return HttpResponseNotFound()
        except:
            return HttpResponseBadRequest()


class GetUser(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args, **kwargs):
        try:
            user= request.user
            
            if user.email:
                return JsonResponse({'username':user.username,'email':user.email})
            else:
                return JsonResponse({'username':user.username})

            

        except :
            return HttpResponseForbidden()

def fieldReset(request,uid,token,type):
    
    if type in ['password','username']:
        redirect_url=f'{settings.FRONTEND_HOST}/reset/{type}/{uid}/{token}'
        return render(request,'field_reset.html',{
            'redirect_url':redirect_url
        })

    else:
        return HttpResponseBadRequest()


class UpdateUserProfile(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,*args, **kwargs):
       
        user=request.user
        user_profile=UserProfile.objects.get_or_create(user=user)
        serializer=UserProfileSerializer(user_profile[0],data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'detail':'success'})
            
        else:
            print("pp:",serializer.errors)
            return JsonResponse(serializer.errors,status=400)


class UpdateUserSettings(APIView):

    permission_classes=[IsAuthenticated]
    def post(self,request,*args, **kwargs):
        
        user=request.user
        user_settings=UserSettings.objects.get_or_create(user=user)
        serializer=UserSettingsSerializer(user_settings[0],data=request.data or request.FILES)

        if serializer.is_valid():
            
            serializer.save()
            return JsonResponse({'detail':'success'})
            
        else:
            print(serializer.errors)
            return JsonResponse(serializer.errors,status=400)


class GetUserProfile(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user=request.user 
        total_number_of_paste=len(CodePaste.objects.filter(user=user))
        number_of_public_paste=len(CodePaste.objects.filter(user=user,public=True))
        number_of_private_paste=len(CodePaste.objects.filter(user=user,public=False))
        total_paste_view=0
        query=CodePaste.objects.filter(user=user)
        all_paste=[]

        for paste in query:
            total_paste_view+=paste.views 
            new_paste={
                'title':paste.title,
                'paste_uuid':paste.paste_uuid
            }

            all_paste.append(new_paste)

        today=timezone.now()
        user_reg_date=user.date_joined

        delta=today-user_reg_date

        return JsonResponse({
            'total_number_of_paste':total_number_of_paste,
            'number_of_public_paste':number_of_public_paste,
            'number_of_private_paste':number_of_private_paste,
            'total_paste_view':total_paste_view,
            'all_paste':all_paste,
            'date_joined':delta.days
        }) 


class GetUserSettings(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args, **kwargs):

        user=request.user

        object = UserSettings.objects.get(user=user)

        user_setting=serializers.serialize('json',[object,])

        user_setting=json.loads(user_setting)

        return JsonResponse({
            'data':user_setting[0]['fields']
        })


class GetProfileData(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user

        obj = UserProfile.objects.get(user=user)

        serializer = UserProfileSerializer(obj)

        return JsonResponse(serializer.data)
