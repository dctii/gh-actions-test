import os
from dotenv import load_dotenv

from locust.env import Environment
from locust.user.users import HttpUser
from locust.user.task import task, TaskSet
from locust.user.wait_time import between

load_dotenv()

class BaseTaskSet(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.headers = self.user.client.headers


class MyTest(BaseTaskSet):
    def on_start(self):
        pass

    @task
    def load_test(self):
        endpoint = '/'

        with self.client.get(
                endpoint,
                timeout=10,
                headers=self.headers,
                catch_response=True) as response:
            if response.status_code == 200:
                print(f"{response.status_code} GOOD REQUEST")
                response.success()
            else:
                response.failure(f"{response.status_code}: BAD REQUEST")

    def on_stop(self):
        pass


class DesktopUser(HttpUser):
    wait_time = between(1, 12)
    host = os.getenv("HOST")
    tasks = [MyTest]


class MyEnvironment(Environment):
    user_classes = [DesktopUser]


environment = MyEnvironment()
