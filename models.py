from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json

db = SQLAlchemy()

class SEMM(db.Model):
    __tablename__ = 'System'

    id = db.Column(db.Integer, primary_key=True)
    Activity = db.Column(db.String())
    Explanation = db.Column(db.String())
    Artifacts = db.Column(db.String())
    Method1 = db.Column(db.String())
    Method2 = db.Column(db.String())
    Method3 = db.Column(db.String())

    def __init__(self, Activity, Explanation, Artifacts, Method1, Method2, Method3):
        self.Activity = Activity
        self.Explanation = Explanation # Corrected typo here
        self.Artifacts = Artifacts
        self.Method1 = Method1
        self.Method2 = Method2
        self.Method3 = Method3

    def __repr__(self):
        return f'{self.Activity}:{self.Explanation}:{self.Artifacts}:{self.Method1}:{self.Method2}:{self.Method3}'













# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
# import json
#
# db = SQLAlchemy()
#
# class SEMM(db.Model):
#     __tablename__ = 'System'
#
#     id = db.Column(db.Integer, primary_key=True)
#     Activity = db.Column(db.String())
#     Explanation = db.Column(db.String())  # Corrected typo here
#     Artifacts = db.Column(db.String())
#     Methods = db.Column(db.String())
#
#     def __init__(self, Activity, Explanation, Artifacts, Methods):
#         self.Activity = Activity
#         self.Explanation = Explanation  # Corrected typo here
#         self.Artifacts = Artifacts
#         self.Methods = Methods
#
#     def __repr__(self):
#         return f'{self.Activity}:{self.Explanation}:{self.Artifacts}:{self.Methods}'
#
#