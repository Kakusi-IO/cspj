from models import *

session = SessionLocal()

def get_profile_by_user_id(user_id):
    return session.query(Profile).filter(Profile.user_id == user_id).one()

def get_task_by_id(user_id):
    return session.query(Task).filter(Task.id == user_id).one()

def get_tasks_by_owner_id(owner_id):
    return session.query(Task).filter(Task.owner_id == owner_id).all()

def get_tasks_by_receiver_id(user_id):
    q = session.query(Task, Receive.user_id).join(Task).join(Receive)
    return q.filter(Receive.user_id==user_id).all()

def get_requests_by_task(task_id):
    return session.query(Request).filter(Request.task_id==task_id).all()

def create_profile(user_id):
    pf = Profile(user_id=user_id)
    session.add(pf)
    session.commit()

def create_task(owner_id, name, reward):
    tsk = Task(owner_id=owner_id, name=name, reward=reward)
    session.add(tsk)
    session.commit()
    return tsk.id

def request_task(user_id, task_id):
    # 创建request
    req = Request(user_id=user_id, task_id=task_id)
    session.add(req)
    session.commit()
    return req.id

def allow_request_task(request_id):
    req = session.query(Request).filter(Request.id==request_id).one()
    user_id, task_id = req.user_id, req.task_id
    # 标记task为received
    tsk = session.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 1})
    # 删除其他request
    reqs = session.query(Request).filter(Request.task_id==task_id)
    reqs.delete()
    # 创建receive
    rec = Receive(user_id=user_id, task_id=task_id)
    session.add(rec)
    session.commit()

def finish_task(task_id):
    # 标记task为finished
    tsk = session.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 2})
    # 标记receive为finished
    rec = session.query(Receive).filter(Receive.task_id==task_id, Receive.status==0)
    rec.update({Receive.status: 1})
    session.commit()

def accept_task(task_id):
    # 标记task为accepted
    tsk = session.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 3})
    # 标记receive为accepted
    rec = session.query(Receive).filter(Receive.task_id==task_id, Receive.task_id==1)
    rec.update({Receive.status: 2})
    # 为receiver发放reward
    reward = session.query(Task.reward).filter(Task.id==task_id).scalar()
    q = session.query(Profile.user_id)

    receiver_id = q.join(Receive, Profile.user_id==Receive.user_id).filter(Receive.task_id==task_id, Receive.status==2).scalar()

    receiver = session.query(Profile).filter(Profile.user_id==receiver_id)
    receiver.update({Profile.points: Profile.points + reward})
    session.commit()

def reject_task(task_id):
    # 重设task为created
    tsk = session.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 0})
    # 标记receive为rejected
    rec = session.query(Receive).filter(Receive.task_id==task_id)
    rec.update({Receive.status: 3})
    session.commit()

def backtrack_task(task_id):
    # 将与该task有关的所有receive设为异常中断
    recs = session.query(Receive).filter(Receive.task_id==task_id)
    recs.update({Receive.status: 4})
    # 重设task为created
    tsk = session.query(Task).filter(Task.id==task_id)
    tsk.update({Task.status: 0})
    session.commit()
    
