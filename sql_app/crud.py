from .models import *
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import Optional

def get_user_by_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one()

def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).one()

def get_task_by_id(db: Session, user_id: int):
    return db.query(Task).filter(Task.id == user_id).one()

def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_tasks_by_owner_id(db: Session, owner_id: int):
    return db.query(Task).filter(Task.owner_id == owner_id).all()

def get_tasks_by_receiver_id(db: Session, user_id: int):
    q = db.query(Task, Receive.user_id).join(Task).join(Receive)
    return q.filter(Receive.user_id==user_id).all()

def get_single_tasks_by_task_id(db: Session, task_id: int, unfinished_only: bool):
    q = db.query(Single_task).filter(Single_task.task_id==task_id)
    if not unfinished_only:
        return q.all()
    else:
        finished = db.query(SCR.single_task_id).all()
        # print(finished)
        return q.filter(Single_task.task_id==task_id, ~Single_task.id.in_([fn[0] for fn in finished])).all()



def get_requests_by_task(db: Session, task_id: int):
    return db.query(Request).filter(Request.task_id==task_id).all()

def get_single_results_by_request(db: Session, request_id: int):
    f"""
        select
        scr.*
        from request r
        inner join task t
        on r.task_id = t.id
        inner join single_task st
        on st.task_id = t.id
        inner join single_classification_result scr
        on st.id = scr.single_task_id
        where r.id = {request_id}
    """
    req = db.query(Request).filter(Request.id==request_id).one()
    return db.query(SCR)\
        .join(Single_task, Single_task.id==SCR.single_task_id)\
        .filter(SCR.user_id==req.user_id, Single_task.task_id==req.task_id).all()

def get_single_task_by_id(db: Session, single_task_id: int):
    return db.query(Single_task).filter(Single_task.id==single_task_id).one()


def get_all_users(db: Session):
    return db.query(User).all()

def create_profile(db: Session, user_id: int):
    pf = Profile(user_id=user_id)
    db.add(pf)
    db.commit()

def create_task(db: Session, owner_id: int, name: str, reward: int, typeno: int):
    tsk = Task(owner_id=owner_id, name=name, reward=reward, typeno=typeno)
    db.add(tsk)
    db.commit()
    return tsk.id

def request_task(db: Session, user_id: int, task_id: int):
    req = Request(user_id=user_id, task_id=task_id)
    db.add(req)
    db.commit()
    # return req.id

def allow_request_task(db: Session, request_id: int):
    req = db.query(Request).filter(Request.id==request_id).one()
    user_id, task_id = req.user_id, req.task_id
    # 标记task为received
    tsk = db.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 1})
    # 删除其他request
    reqs = db.query(Request).filter(Request.task_id==task_id)
    reqs.delete()
    # 创建receive
    rec = Receive(user_id=user_id, task_id=task_id)
    db.add(rec)
    db.commit()

def finish_task(db: Session, task_id: int):
    # 标记task为finished
    tsk = db.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 2})
    # 标记receive为finished
    rec = db.query(Receive).filter(Receive.task_id==task_id, Receive.status==0)
    rec.update({Receive.status: 1})
    db.commit()

def accept_task(db: Session, task_id: int):
    # 标记task为accepted
    tsk = db.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 3})
    # 标记receive为accepted
    rec = db.query(Receive).filter(Receive.task_id==task_id, Receive.task_id==1)
    rec.update({Receive.status: 2})
    # 为receiver发放reward
    reward = db.query(Task.reward).filter(Task.id==task_id).scalar()
    q = db.query(Profile.user_id)

    receiver_id = q.join(Receive, Profile.user_id==Receive.user_id).filter(Receive.task_id==task_id, Receive.status==2).scalar()

    receiver = db.query(Profile).filter(Profile.user_id==receiver_id)
    receiver.update({Profile.points: Profile.points + reward})
    db.commit()

def reject_task(db: Session, task_id: int):
    # 重设task为created
    tsk = db.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 0})
    # 标记receive为rejected
    rec = db.query(Receive).filter(Receive.task_id==task_id)
    rec.update({Receive.status: 3})
    db.commit()

def backtrack_task(db: Session, task_id: int):
    # 将与该task有关的所有receive设为异常中断
    recs = db.query(Receive).filter(Receive.task_id==task_id)
    recs.update({Receive.status: 4})
    # 重设task为created
    tsk = db.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 0})
    db.commit()
    
def create_single_task(db: Session, task_id: int, source_url: str):
    st = Single_task(task_id=task_id, source_url=source_url)
    db.add(st)
    db.commit()

def submit_single_classification_result(db: Session, single_task_id: int, choice: int, user_id: int):
    scr = SCR(single_task_id=single_task_id, choice=choice, user_id=user_id)
    db.add(scr)
    db.commit()