from .database import Base

User = Base.classes.auth_user # django自带

Profile = Base.classes.profile
Profile.__repr__ = lambda self : f"{self.id}, {self.user_id}, {self.create_at}"

Task = Base.classes.task

Single_task = Base.classes.single_task

Request = Base.classes.request

Receive = Base.classes.receive

SCR = Base.classes.single_classification_result

# SCR = Base.classes.single_classification_result


# __all__ = [SessionLocal, Profile, Task, Single_task, Request, Receive]

# print(Task.__dict__)