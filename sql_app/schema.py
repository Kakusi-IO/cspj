from ninja import Schema
from typing import Optional
from . import crud
from .database import DBManager

class User(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

class Profile(Schema):
    id: int
    user_id: int
    points: int
    user: User

    @staticmethod
    def resolve_user(obj):
        with DBManager() as db:
            return crud.get_user_by_user_id(db, obj.user_id)


class Task(Schema):
    id: int
    owner_id: int
    owner_name: str
    name: str
    reward: int
    status: int
    typeno: int
    status_name: str
    type_name: str
    owner_name: str

    @staticmethod
    def resolve_owner_name(obj):
        with DBManager() as db:
            return crud.get_user_by_user_id(db, obj.owner_id).username

    @staticmethod
    def resolve_status_name(obj):
        match obj.status:
            case 0:
                return '已创建'
            case 1:
                return '已认领'
            case 2:
                return '已完成'
            case 3:
                return '已交付'
            case _:
                return '???'

    @staticmethod
    def resolve_type_name(obj):
        match obj.typeno:
            case 0:
                return '文本分类'
            case 1:
                return '音频分类'
            case 2:
                return '图像分类'
            case 3:
                return '框图'
            case _:
                return '???'


class Request(Schema):
    id: int
    task_id: int
    user_id: int

class RequestIn(Schema):
    task_id: int
    user_id: int

class UserIn(Schema):
    username: str
    password: str

class TaskIn(Schema):
    owner_id: int
    name: str
    reward: int = 500



class SingleTaskIn(Schema):
    task_id: int
    source_url: str = 'https://raw.githubusercontent.com/Kakusi-IO/images/main/Mr.Love.txt'

class SingleTask(SingleTaskIn):
    id: int
    # finished: Optional[bool]

class Message(Schema):
    message: str

class IDIn(Schema):
    id: int

class SCRIn(Schema):
    single_task_id: int 
    choice: int
    user_id: int

class SCR(Schema):
    id: int
    single_task_id: int 
    choice: int
    user_id: int
    single_task: SingleTask

    @staticmethod
    def resolve_single_task(obj):
        with DBManager() as db:
            return crud.get_single_task_by_id(db, obj.single_task_id)