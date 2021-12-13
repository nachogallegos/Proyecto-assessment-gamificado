from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'


class Question:
    def __init__(self,promt,answer):
        self.promt = promt
        self.answer = answer
