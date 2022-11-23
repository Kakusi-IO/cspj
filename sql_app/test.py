import requests
import os

BASE_URL = 'http://localhost:8000/api/'

def main():
    # users:
    # 2: root
    # 19: carol
    
    # 2创建task
    res = requests.post(os.path.join(BASE_URL, 'user/create'))

print(os.path.join(BASE_URL, 'post/sdf'))