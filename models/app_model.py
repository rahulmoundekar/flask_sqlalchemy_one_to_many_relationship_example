from db.db import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    addresses = db.relationship('Address', backref=db.backref('employee', uselist=True),
                                cascade='all, delete-orphan', lazy=True, uselist=True)
    # delete parent record in one to many relationship in flask cascade='all, delete-orphan'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(255), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), unique=True, nullable=False)

    def __init__(self, addr):
        self.addr = addr
