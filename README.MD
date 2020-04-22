# Flask CURD SqlAlchemy one to many relationship example :

#### Project Setup

  - Making the project as :
     ```
    mkdir flask_sqlalchemy_one_to_many_relationship_example
    cd flask_sqlalchemy_one_to_many_relationship_example
    ```
  - Install flask:
    ```
     pip install flask
    ```
 - Integrating SqlAlchemy
    ```
    pip install sqlalchemy
    ```
 - Create EmployeeManagementSystem.py for development 
 - create folder structure like this :
    ![N|Solid](structure.PNG)
    
 - create db.py
    ```
     from flask_sqlalchemy import SQLAlchemy
     db = SQLAlchemy()
    ```  
       
  - Declaring Models: [models/app_model.py]
     ```
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
    

    ```
 - create settings.py for configuration
     ```
     # configuration
    class Config:
        DEBUG = True
        # db
        SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/djangoapp'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```
    
 - Make a runserver configuration
     ``` 
    from flask import Flask, render_template, request, redirect, flash
    from sqlalchemy.exc import IntegrityError
    
    from db.db import db
    from models.app_model import Employee, Address
    
    app = Flask(__name__)
    app.secret_key = 'asrtarstaursdlarsn'
    app.config.from_object('settings.Config')
    
    # initialization
    db.init_app(app)
    
    
    @app.route("/", methods=['GET', 'POST'])
    @app.route("/<int:employee_id>", methods=['GET'])
    def employeeHome(employee_id=None):
        if request.method == 'POST':
            # person data
            pid = request.form.get('id')
            name = request.form.get('name')
            contact = request.form.get('contact')
            email = request.form.get('email')
            # license data
            address_list = []
    
            for addressValue in zip(request.form.getlist('address')):
                address_list.append(Address(addressValue[0]))
    
            print(address_list)
            if pid:  # if id present update records
                employee = Employee.query.filter_by(id=pid).first()
                employee.name = name
                employee.email = email
                employee.contact = contact
                employee.addresses = address_list
                db.session.commit()
                flash('Looks like you have changed your Details!', "success")
            else:
                # id not None save record
                try:
                    employee_entry = Employee(name=name, email=email, contact=contact)
                    employee_entry.addresses = address_list
                    db.session.add(employee_entry)
                    db.session.commit()
                    flash('Employee Successfully saved!', "success")
                except IntegrityError as e:
                    flash(e, 'Something went wrong please try again later', "danger")
        employee = None
        addresses = [None, None]
    
        if employee_id:  # load record form edit form data
            employee = Employee.query.filter_by(id=employee_id).first()
            addresses = Address.query.filter_by(employee_id=employee_id)
        employees = Employee.query.all()
        return render_template('index.html', employees=employees, employee=employee, addresses=addresses)
    
    
    @app.route("/delete/<int:employee_id>", methods=['GET'])
    def deleteEmployee(employee_id):
        try:
            employee = Employee.query.filter_by(id=employee_id).first()
            print(employee)
            if employee:
                db.session.delete(employee)
                db.session.commit()
                flash('Looks like you have changed your Details!', "success")
            else:
                flash('Could not find any Employee to delete', "danger")
        except IntegrityError as e:
            flash('Something went wrong please try again later', "danger")
        return redirect("/")
    
    
    # run always put in last statement or put after all @app.route
    if __name__ == '__main__':
        app.run(host='localhost')
    
    # manager.run()

    ```
 - create html file inside templates folder
    * check project directory for index.html file
    
 
 - In order to run app:
    ```
	  python app.py
    ```

 - run on your browser
    * Your should run at: http://127.0.0.1:5000/
