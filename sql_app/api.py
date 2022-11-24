from ninja import NinjaAPI, Schema
from ninja.files import UploadedFile
from . import crud, schema
from .database import DBManager
from typing import Optional, List
from django.contrib.auth.models import User
from ninja.responses import codes_2xx, codes_4xx
import json

api = NinjaAPI()

@api.get('/user', response=schema.User)
def get_user(request, user_id: int):
    with DBManager() as db:
        return crud.get_user_by_user_id(db, user_id)

@api.get('/user/profile', response=schema.Profile)
def get_profile(request, user_id: int):
    # print(request.user)
    with DBManager() as db:
        return crud.get_profile_by_user_id(db, user_id)

@api.get('/task', response=schema.Task)
def get_task(request, task_id: int):
    with DBManager() as db:
        return crud.get_task_by_id(db, task_id)

@api.get('/task/all', response=List[schema.Task])
def get_all_tasks(request):
    with DBManager() as db:
        return crud.get_all_tasks(db)

@api.get('/user/tasks', response=List[schema.Task])
def get_tasks(request, owner_id: Optional[int] = None, receiver_id: Optional[int] = None):
    with DBManager() as db:
        if owner_id is not None:
            return crud.get_tasks_by_owner_id(db, owner_id)
        elif receiver_id is not None:
            return crud.get_tasks_by_receiver_id(db, receiver_id)
        else:
            raise Exception('至少需要owner_id或receiver_id中的一个')

@api.get('/user/request', response=List[schema.Request])
def get_requests(request, task_id: int):
    with DBManager() as db:
        return crud.get_requests_by_task(db, task_id)

# 测试用
@api.get('/user/all', response=List[schema.User])
def get_all_users(request):
    with DBManager() as db:
        return crud.get_all_users(db)

@api.post('/user/create')
def create_user(request, data: schema.UserIn):
    print(data)
    print(type(data))
    try:
        with DBManager() as db:
            user = User.objects.create_user(username=data.username, password=data.password)
            crud.create_profile(db, user.id)
        return {'message': 'created'}
    except Exception as e:
        print(e)
        return {'message': e.__str__()}
        
@api.post('/task/create')
def create_task(request, data: schema.TaskIn):
    try:
        with DBManager() as db:
            task_id = crud.create_task(db, data.owner_id, data.name, data.reward, data.typeno)
        return {'task_id': task_id}
    except Exception as e:
        return {'message': e.__str__()}

@api.get('/task/single', response=List[schema.SingleTask])
def get_single_tasks_by_task_id(request, task_id: int, not_finished: bool = False):
    with DBManager() as db:
        return crud.get_single_tasks_by_task_id(db, task_id, not_finished)

@api.post('/task/single/create')
def create_single_tasks(request, data: List[schema.SingleTaskIn]):
    try:
        with DBManager() as db:
            for sti in data: 
                crud.create_single_task(db, sti.task_id, sti.source_url)
        return {'message': 'created'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/task/single/upload')
def upload_single_tasks(request, f: UploadedFile, task_id: int):
    try:
        data_ = f.read().decode('utf-8') # str
        data = json.loads(data_) # dict
        # print(data)
        with DBManager() as db:
            for sti in data: 
                crud.create_single_task(db, task_id, sti['source_url'])
        return {'message': 'created'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/task/single/submit')
def submit_single_task_results(request, data: List[schema.SCRIn]):
    try:
        with DBManager() as db:
            # TODO: 
            # 类型判断
            for dt in data:
                crud.submit_single_classification_result(db, dt.single_task_id, dt.choice, dt.user_id)
        return {'message': 'submitd'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/request/create')
def request_task(request, data: schema.RequestIn):
    try:
        with DBManager() as db:
            crud.request_task(db, data.user_id, data.task_id)
        return {'message': 'created'}
    except Exception as e:
        return {'message': e.__str__()}

@api.get('/request/result', response=List[schema.SCR])
def get_single_results_by_request(request, request_id: int):
    with DBManager() as db:
        return crud.get_single_results_by_request(db, request_id)

@api.post('/request/allow')
def allow_request_task(request, data: schema.IDIn):
    try:
        with DBManager() as db:
            crud.allow_request_task(db, data.id)
        return {'message': 'allowed'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/task/finish')
def finish_task(request, data: schema.IDIn):
    try:
        with DBManager() as db:
            crud.finish_task(db, data.id)
        return {'message': 'allowed'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/task/accept')
def accept_task(request, data: schema.IDIn):
    try:
        with DBManager() as db:
            crud.accept_task(db, data.id)
        return {'message': 'accepted'}
    except Exception as e:
        return {'message': e.__str__()}

@api.post('/task/reject')
def reject_task(request, data: schema.IDIn):
    try:
        with DBManager() as db:
            crud.reject_task(db, data.id)
        return {'message': 'rejected'}
    except Exception as e:
        return {'message': e.__str__()}
    
@api.post('/task/backtrack')
def backtrack_task(request, data: schema.IDIn):
    try:
        with DBManager() as db:
            crud.backtrack_task(db, data.id)
        return {'message': 'backtracked'}
    except Exception as e:
        return {'message': e.__str__()}