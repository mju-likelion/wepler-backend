from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets, status 
from wepler.models import *
from wepler.serializers import *
import jwt                             # 토큰 발행에 사용
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_exempt

def tokenCheck(request):
    SECRET_KEY = '아무튼비밀임'
    if request.method == 'GET' or request.method == 'POST':
        token = request.headers.get('Authorization', None)
        print(token)
        user_token_info = jwt.decode(token, SECRET_KEY, algorithm = "HS256")
        if Plus.objects.filter(plus_id=user_token_info['user_id']).exists() :
            user_id = user_token_info['user_id']
            return user_id
        elif Plz.objects.filter(plz_id=user_token_info['user_id']).exists() :
            user_id = user_token_info['user_id']
            return user_id 
        return HttpResponse(status=403)
    else:
        HttpResponse(status=400)

def getMypage(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id = user_id).exists():
            user_info = Plus.objects.filter(plus_id = user_id)[0]
            user_name = user_info.plus_name
            user_phone = user_info.plus_phonenumber
            user_address_big = user_info.plus_address_big
            user_address_small = user_info.plus_address_small
            user_month = user_info.plus_continu_month
            user_start = user_info.plus_start_time
            user_end = user_info.plus_end_time
            user_talent = user_info.plus_talentshare
            user_class = user_info.plus_class
            user_day = user_info.plus_date
            return JsonResponse({"user_name" : user_name, "user_phone" : user_phone, "user_class" : user_class, "user_email" : user_id, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_continu_month" : user_month, "user_start_time" : user_start, "user_end_time" : user_end, "user_talentshare" : user_talent, "user_start_day" : user_day}, status=200)
        elif Plz.objects.filter(plz_id = user_id).exists():
            user_info = Plz.objects.filter(plz_id = user_id)[0]
            user_name = user_info.plz_name
            user_phone = user_info.plz_phonenumber
            user_address_big = user_info.plz_address_big
            user_address_small = user_info.plz_address_small
            user_group = user_info.plz_group
            user_when_learn = user_info.plz_when_learn
            user_class = user_info.plz_class
            return JsonResponse({"user_name" : user_name, "user_phone" : user_phone, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_group" : user_group, "user_when_learn" : user_when_learn, "user_class" : user_class, "user_email" : user_id}, status=200)
        else:
            return HttpResponse(staus = 403)
    else:
        return HttpResponse(staus = 400)

@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = tokenCheck(request)
        if Plus.objects.filter(plus_id=user_id).exists() :
            user_info = Plus.objects.filter(plus_id=user_id)[0]
            user_info.plus_talentshare = data['plus_talentshare']
            user_info.plus_continu_month = data['plus_continu_month']
            user_info.plus_start_time = data['plus_start_time']
            user_info.plus_end_time = data['plus_end_time']
            user_class = data['plus_fields']
            user_day = data['plus_start_day']
            u_class = ''
            u_day = ''
            for i in range(len(user_class)):
                if user_class[i] == 'education':
                    h_class = '교육'
                elif user_class[i] == 'council':
                    h_class = '상담'
                elif user_class[i] == 'making':
                    h_class = '메이킹'
                elif user_class[i] == 'activity':
                    h_class = '야외활동'
                elif user_class[i] == 'culture':
                    h_class = '문화'
                elif user_class[i] == 'trip':
                    h_class = '여행'
                else:
                    h_class = '기타'
                u_class = u_class + h_class + ' '
            
            for j in range(len(user_day)):
                if user_day[j] == 'monday':
                    h_day = '월요일'
                elif user_day[j] == 'tuesday':
                    h_day = '화요일'
                elif user_day[j] == 'wednesday':
                    h_day = '수요일'
                elif user_day[j] == 'thursday':
                    h_day = '목요일'
                elif user_day[j] == 'friday':
                    h_day = '금요일'
                elif user_day[j] == 'saturday':
                    h_day = '토요일'
                else:
                    h_day = '일요일'
                u_day = u_day + h_day + ' '
            user_info.plus_class = u_class
            user_info.plus_date = u_day
            user_info.save()
            return HttpResponse(status=200)
        elif Plz.objects.filter(plz_id=user_id).exists() :
            user_info = Plz.objects.filter(plz_id=user_id)[0]
            #plz 어떤 정보 수정인지 알아보기
            user_class = data['plz_fields']
            u_class = ''
            for i in range(len(user_class)):
                if user_class[i].class_name == 'education':
                    h_class = '교육'
                elif user_class[i].class_name == 'council':
                    h_class = '상담'
                elif user_class[i].class_name == 'making':
                    h_class = '메이킹'
                elif user_class[i].class_name == 'activity':
                    h_class = '야외활동'
                elif user_class[i].class_name == 'culture':
                    h_class = '문화'
                elif user_class[i].class_name == 'trip':
                    h_class = '여행'
                else:
                    h_class = '기타'
                u_class = u_class + h_class + ' '
            user_info.plz_class = u_class
            user_info.save()
            return HttpResponse(status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=403)

def applied_list(request):
    if request.method == 'GET':
        print("작동")
        token = request.headers.get('Authorization', None)
        print(token)
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id=user_id).exists() :
            qs = Plus_apply.objects.filter(plz_user=user_id)
            serializer = Plus_ApplySerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            qs = Plz_apply.objects.filter(plz_user=user_id)
            serializer = Plz_ApplySerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    else: return HttpResponse(status=400)

def apply_list(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id=user_id).exists() :
            qs = Plz_apply.objects.filter(plz_user=user_id)
            serializer = Plus_ApplySerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            qs = Plus_apply.objects.filter(plz_user=user_id)
            serializer = Plz_ApplySerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    else: return HttpResponse(status=400)

#Plus가 신청한걸 Plz가 거절하는 경우
@csrf_exempt
def apply_delete(request, apply_id):
    if request.method == 'DELETE':
        if Plz.objects.filter(plz_id = user_id).exists():
            pa = Plus_apply.objects.filter(id=apply_id)[0]
            pa.delete()
            return HttpResponse(status = 200)
        else:
            pa = Plz_apply.objects.filter(id=apply_id)[0]
            pa.delete()
            return HttpResponse(status = 200)
    else: return HttpResponse(status=400)

#수락한 경우
@csrf_exempt
def user_match(request, apply_id): #아직 어떤 정보를 띄우는게 좋은지 모른다.
    print("작동-")
    if request.method == 'POST':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            h_id = Plus_apply.objects.filter(id=apply_id)[0].hire_id_id
            p_id = Plus_apply.objects.filter(id=apply_id)[0].plus_user_id
            plz = Plz.objects.filter(plz_id = user_id)[0]
            plus = Plus.objects.filter(plus_id = p_id)[0]
            if(Match.objects.filter(plus_user=p_id).filter(plz_user=user_id).exists()):
                return JsonResponse({"isoverap" : True}, status=200)
            else:
                Match.objects.create(
                    plz_user = plz,
                    plus_user = plus,
                    plz_name = plz.plz_name,
                    plus_name = plus.plus_name,
                    plz_address_big = plz.plz_address_big,
                    plus_address_big = plus.plus_address_big,
                    plz_class = Hire_board.objects.filter(id=h_id)[0].plz_class,
                    plus_class = Plus_apply.objects.filter(id=apply_id)[0].plus_class,
                    match_subject = Hire_board.objects.filter(id=h_id)[0].title,
                    complete = False,
                    h_id = h_id,
                )
                apply = Plus_apply.objects.filter(id=apply_id)
                apply.delete()
                return JsonResponse({"isoverap" : False}, status=200)
        elif Plus.objects.filter(plus_id=user_id).exists() :
            h_id = Plz_apply.objects.filter(id=apply_id)[0].hire_id_id
            p_id = Plz_apply.objects.filter(id=apply_id)[0].plz_user_id
            plz = Plz.objects.filter(plz_id = p_id)[0]
            plus = Plus.objects.filter(plus_id = user_id)[0]
            if(Match.objects.filter(plus_user=user_id).filter(plz_user=p_id).exists()):
                return JsonResponse({"isoverap" : True}, status=200)
            else:
                Match.objects.create(
                    plz_user = plz,
                    plus_user = plus,
                    plz_name = plz.plz_name,
                    plus_name = plus.plus_name,
                    plz_address_big = plz.plz_address_big,
                    plus_address_big = plus.plus_address_big,
                    plz_class = Hire_board.objects.filter(id=h_id)[0].plz_class,
                    plus_class = Plz_apply.objects.filter(id=apply_id)[0].plus_class,
                    match_subject = Hire_board.objects.filter(id=h_id)[0].title,
                    complete = False,
                    h_id = h_id,
                )
                apply = Plz_apply.objects.filter(id=apply_id)
                apply.delete()
                return JsonResponse({"isoverap" : False}, status=200)
        else: return HttpResponse(status=400)
    else: return HttpResponse(status=403)

def applied_detail(request, apply_id):        #이부분은 소현이가 원하는 데이터 넘겨주면 됨
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            apply = Plus_apply.objects.filter(id = apply_id)[0]
            user_id = apply.plus_user_id
            p_user = Plus.objects.filter(plus_id = user_id)[0]
            
            user_id = apply.plus_user_id
            user_name = apply.plus_user_name
            user_class = apply.plus_class
            user_day = apply.plus_date
            user_phone = p_user.plus_phonenumber
            user_address_big = p_user.plus_address_big
            user_address_small = p_user.plus_address_small
            user_month = p_user.plus_continu_month
            user_start = p_user.plus_start_time
            user_end = p_user.plus_end_time
            user_talent = p_user.plus_talentshare
            user_point = p_user.plus_point
            return JsonResponse({"user_name" : user_name, "user_day" : user_day, "user_start" : user_start, "user_end" : user_end, "user_phone" : user_phone, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_class" : user_class, "user_email" : user_id, "user_point" : user_point}, status=200)
        else:
            apply = Plz_apply.objects.filter(id = apply_id)[0]
            user_id = apply.plz_user_id
            p_user = Plz.objects.filter(plz_id = user_id)[0]
            
            user_id = apply.plz_user_id
            user_name = apply.plz_user_name
            user_class = apply.plz_class
            user_day = apply.plz_date
            user_phone = p_user.plz_phonenumber
            user_address_big = p_user.plz_address_big
            user_address_small = p_user.plz_address_small
            #게시글 내용을 좀 채워주면 될듯. 시간이나 제목 같은 거
            return JsonResponse({"user_name" : user_name, "user_day" : user_day, "user_start" : user_start, "user_end" : user_end, "user_phone" : user_phone, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_class" : user_class, "user_email" : user_id, "user_point" : user_point}, status=200)
    else: return HttpResponse(status=400)

def match_detail(request, match_id):
    if request.method == 'GET':
        match = Match.objects.filter(id=match_id)[0]
        user_id = match.plus_user_id
        p_user = Plus.objects.filter(plus_id=user_id)[0]
        user_name = match.plus_name
        user_class = match.plus_class
        user_address_big = match.plus_address_big
        user_address_small = p_user.plus_address_small
        user_point = p_user.plus_point
        user_start = p_user.plus_start_time
        user_end = p_user.plus_end_time
        return JsonResponse({"user_email" : user_id, "user_name" : user_name, "user_class" : user_class, "user_address_big" : user_address_big, "user_address_small" : user_address_small, "user_point" : user_point, "user_start" : user_start, "user_end" : user_end}, status=200)
    else: return HttpResponse(status=400)
        
#진행중인 숫자
def match_list_count(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            match = Match.objects.filter(plz_user=user_id).filter(complete=False).count()
            return JsonResponse({"match_count" : match}, status=200)
        else:
            match = Match.objects.filter(plus_user=user_id).filter(complete=False).count()
            return JsonResponse({"match_count" : match}, status=200)
    else: return HttpResponse(status=400)

#완료한거 숫자
def complete_list_count(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            match = Match.objects.filter(plz_user=user_id).filter(complete=True).count()
            return JsonResponse({"match_count" : match}, status=200)
        else:
            match = Match.objects.filter(plus_user=user_id).filter(complete=True).count()
            return JsonResponse({"match_count" : match}, status=200)
    else: return HttpResponse(status=400)

#신청받은거 숫자
def applied_list_count(request):
    if request.method == 'GET':
        print("작동")
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            apply = Plus_apply.objects.filter(plz_user=user_id).count()
            return JsonResponse({"match_count" : apply}, status=200)
        else:
            apply = Plz_apply.objects.filter(plus_user=user_id).count()
            return JsonResponse({"match_count" : apply}, status=200)
    else: return HttpResponse(status=400)

def match_list(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists(): 
            qs = Match.objects.filter(plz_user=user_id).filter(complete=False)
            serializer = MatchSerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            qs = Match.objects.filter(plus_user=user_id).filter(complete=False)
            serializer = MatchSerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    else: return HttpResponse(status=400)

#완료된 활동
def complete_list(request):
    if request.method == 'GET':
        user_id = tokenCheck(request)
        if Plz.objects.filter(plz_id = user_id).exists():
            user_id = tokenCheck(request)
            qs = Match.objects.filter(plz_user=user_id).filter(complete=True)
            serializer = MatchSerializer(qs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            user_id = tokenCheck(request)
            qs = Match.objects.filter(plz_user=user_id).filter(complete=True)
            serializer = MatchSerializer(qs, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    else: return HttpResponse(status=400)

@csrf_exempt
def match_complete(request, match_id):
    if request.method == 'POST':
        ma = Match.objects.filter(id = match_id)[0]
        ma.complete = True
        ma.save()
        return HttpResponse(status=200)
    else: return HttpResponse(status=400)
