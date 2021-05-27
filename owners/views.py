import json
from django.views import View
from django.http import JsonResponse
from .models import Owner, Dog


class OwnerListView(View):
    
    def get(self, request):
        owners = Owner.objects.all()
        # Queryset은 Json으로 변경이 불가능하니까! for문이 필요함
       #.dog_set -> 바라보는 class를 소문자로 바꾸고 _set을 붙이면 됨 (역참조)
       # -> 역참조말고 filter로 가져올수도 있음
       # 
        result = []
        for owner in owners:
            dogs = owner.dog_set.all()
            dogs_list = []

            for dog in dogs:
                dog_info = {
                    'name': dog.name,
                    'age' : dog.age
                }
                dogs_list.append(dog_info)

        # 빨리 하고싶을때, 조건문도 for문 뒤에 쓸수 있음, 너무 길어지면 가독성 떨어짐= dogs_list = [{
        #     'name': dog.name,
        #     'age' : dog.age
        #  } for dog in dogs]

            owner_info = {   
                'name' : owner.name,
                'age'  : owner.age,
                'email': owner.email,
                'dogs' : dogs_list
                        
                    } 
            result.append(owner_info)
            return JsonResponse({'result': result }, status=200)


    def post(self, request):
        try: 
        
            data = json.loads(request.body) 

            Owner.objects.create(
                name = data['name'],
                email = data['email'],
                age = data['age']
                )
        
            return JsonResponse({'result': 'OK' }, status=201)

        except KeyError:
            return JsonResponse ({'message':'INVALID_ KEY'}, status=400)

class DogListView(View):
    def get(self, request):
        dogs = Dog.objects.all()
        # Queryset은 Json으로 변경이 불가능하니까! for문이 필요함
        
        result = []
        for dog in dogs:
                dog_info = {   
                    'name' : dog.name,
                    'age'  : dog.age,
                    'owner': dog.owner.name

                } 
                result.append(dog_info)
        return JsonResponse({'result': result}, status=200)





    #get 하고 create함 
    def post(self, request):
        try: 
            data = json.loads(request.body) 

            owner= Owner.objects.get(email=data['owner_data'])
            # email -> 컬럼명 / data['email] -> front에서 보내주는 값
            Dog.objects.create(name=data['name'], age=data['age'], owner=owner)
            # get에서 exception2개 발생 -> email없을떄, email 같은 값일때

            return JsonResponse({'result': 'OK' }, status=201)

        except KeyError:

            return JsonResponse ({'message':'INVALID_ KEY'}, status=400)
        except Owner.DoesNotExist:
            return JsonResponse ({'message':'USER_DOSE_NOT_EXIST'}, status=404)
            # error 알기