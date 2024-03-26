from user_admin import app
from flask import render_template, redirect, session, url_for, flash,request,make_response,jsonify
from user_admin.models import Employee,Admin,Role,load_user
from user_admin.forms import RegisterForm,LoginForm,AdminForm,EditForm
from user_admin import db
from sqlalchemy.exc import IntegrityError,DataError
from flask_login import login_user,logout_user,login_required
from flask_jwt_extended import create_access_token, jwt_required,unset_jwt_cookies,get_jwt_identity


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/employee")
# @login_required
@jwt_required()
def employee_page():
    access_token_cookie = request.cookies.get('access_token_cookie')
    if access_token_cookie:
        current_user_email = get_jwt_identity()
        current_user = Employee.query.filter_by(email_address=current_user_email).first()
        return render_template("employee_page.html", current_user=current_user)

@app.route("/employee/register",methods=['GET','POST'])
def employee_register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            employee_role = Role.query.filter_by(name='employee').first()
            employee_to_create = Employee(first_name = register_form.first_name.data,
                                        last_name = register_form.last_name.data,
                                        email_address = register_form.email_address.data,
                                        address = register_form.address.data,
                                        DOB = register_form.DOB.data,
                                        password = register_form.password.data,
                                        phone_number = register_form.phone_number.data,
                                        role = employee_role)
            db.session.add(employee_to_create)
            db.session.commit()
            flash(f'Account created successfully!! ',category='success')
            
            return redirect(url_for('employee_login'))
        except IntegrityError as e:
            db.session.rollback()
            email_address_error = 'email_address' in str(e.orig)
            phone_number_error = 'phone_number' in str(e.orig)
            print(email_address_error,phone_number_error)
            if (email_address_error):
                flash('Email address is already in use.', category='danger')
            elif (phone_number_error):
                flash('Phone number is already in use.', category='danger')
            else:
                print(e)
                flash('Error occurred while creating employee.', category='danger')
                
        except DataError as e:
            db.session.rollback()
            phone_number_error = 'phone_number' in str(e.orig)
            if(phone_number_error):
                flash('Phone number should be 10 charcters.', category='danger')
    if register_form.errors != {}:
        for field,error_message in register_form.errors.items():
            flash(f'there is a error with creating a employee for {field}: {error_message}',category='danger')
            
    return render_template('employee_register.html',form=register_form)


@app.route("/employee/login",methods=['GET','POST'])
def employee_login():
    login_form =  LoginForm()
    if (login_form.validate_on_submit()):
        email = login_form.email_address.data
        attempted_employee = Employee.query.filter_by(email_address=email).first()
        if(attempted_employee and attempted_employee.check_password_correction(attempted_password = login_form.password.data)):
            session['user_id'] = attempted_employee.id
            session['role'] = 'employee'
            login_user(attempted_employee)
            access_token_cookie = create_access_token(identity=email)          
            response = make_response(redirect(url_for('employee_page')))
            response.set_cookie('access_token_cookie', access_token_cookie) 
            flash(f"Success! You are logged in as: {attempted_employee.first_name}{attempted_employee.last_name}", category="success")
            
            return response
            # return redirect(url_for('employee_page',access_token = access_token))
        else:
            flash(f"Email and password are not match ! Please try again",category="danger")
    return render_template("employee_login.html",form = login_form)

@app.route("/logout")
def employee_logout_page():
    logout_user()
    session.clear()
    flash("You have been logged out!",category='info')
    response = make_response(redirect(url_for("home_page")))
    unset_jwt_cookies(response)
    return response

@app.route("/admin_page")
#@login_required
@jwt_required()
def admin_page():
    access_token_cookie = request.cookies.get('access_token_cookie')
    if access_token_cookie:
        employess = Employee.query.all()
        return render_template("admin_view.html",employees = employess)

@app.route("/admin/login",methods=["GET","POST"])
def admin_login():
    admin_form = AdminForm()
    if(admin_form.validate_on_submit()):
        email = admin_form.email_address.data
        attempted_admin = Admin.query.filter_by(email_address=email).first()
        if(attempted_admin and attempted_admin.check_password_correction(attempted_password = admin_form.password.data)):
            session['user_id'] = attempted_admin.id
            session['role']='admin'
            login_user(attempted_admin)
            access_token_cookie = create_access_token(identity=email)          
            response = make_response(redirect(url_for('admin_page')))
            response.set_cookie('access_token_cookie', access_token_cookie) 

            flash(f"Success! You are logged in as: {attempted_admin.first_name}{attempted_admin.last_name}", category="success")
            return response
        else:
            flash(f"Email and password are not match ! Please try again",category="danger")
    return render_template("admin_login.html",form = admin_form)

@app.route("/admin/employee/<int:id>",methods=['GET'])
@login_required
def admin_employee_info(id):
    employee = Employee.query.get(id)
    if not employee:
        return flash(f"There is error while fetching the employee",category="danger")
    return render_template('admin_employee_info.html',employee=employee)

@app.route("/admin/edit_employee/<int:id>", methods = ['GET','POST'] )
@login_required
def admin_employee_edit(id):
    employee =  Employee.query.get(id)
    editform = EditForm(obj = employee)
    print("CSRF Token:", request.form.get("csrf_token"))
    if request.method == "POST":
        if editform.validate_on_submit():
            editform.populate_obj(employee)
            db.session.commit()
            flash(f"Successfully edited the employee details: {employee.first_name} {employee.last_name}",category="success")
            return redirect(url_for('admin_page'))
        else:
            flash(f"Error for the edited the employee details:",category="danger")
            
    return render_template('admin_employee_edit.html',form = editform,employee = employee)

@app.route("/admin/delete_employee/<int:id>",methods = ['GET','POST'] )
@login_required
def admin_employee_delete(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash(f"Successfully deleted the employee: {employee.first_name} {employee.last_name}", category="success")
    else:
        flash(f"Employee with ID {id} does not exist.", category="danger")
    return redirect(url_for('admin_page'))

@app.route("/admin/register",methods=['GET','POST'])
def admin_register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        try:
            admin_role = Role.query.filter_by(name='admin').first()
            admin_to_create = Admin(first_name = register_form.first_name.data,
                                        last_name = register_form.last_name.data,
                                        email_address = register_form.email_address.data,
                                        address = register_form.address.data,
                                        DOB = register_form.DOB.data,
                                        password = register_form.password.data,
                                        phone_number = register_form.phone_number.data,
                                        role = admin_role)
            db.session.add(admin_to_create)
            db.session.commit()
            
            flash(f'Account created successfully!! ',category='success')
            
            return redirect(url_for('admin_login'))
        except IntegrityError as e:
            db.session.rollback()
            email_address_error = 'email_address' in str(e.orig)
            phone_number_error = 'phone_number' in str(e.orig)
            if (email_address_error):
                flash('Email address is already in use.', category='danger')
            elif (phone_number_error):
                flash('Phone number is already in use.', category='danger')
            else:
                print(e)
                flash('Error occurred while creating employee.', category='danger')

    if register_form.errors != {}:
        for field,error_message in register_form.errors.items():
            flash(f'there is a error with creating a employee for {field}: {error_message}',category='danger')
            
    return render_template('admin_register.html',form=register_form)