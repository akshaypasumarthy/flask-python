from flask import Blueprint, request, render_template,make_response
from user_admin.models import Employee
from flask_restful import Resource, Api


employee_search_bp = Blueprint('employee_search', __name__)
api = Api(employee_search_bp)

class EmployeeSearchResource(Resource):
    def get(self):
        search_query = request.args.get('search_query')
        first_name_checked = request.args.get('first_name') == 'on'
        last_name_checked = request.args.get('last_name') == 'on'
        address_checked = request.args.get('address') == 'on'
        email_address_checked = request.args.get('email_address') == 'on'
        
        employees = []

        if first_name_checked:
            employees.extend(Employee.query.filter(Employee.first_name.ilike(f"%{search_query}%")).all())

        if last_name_checked:
            employees.extend(Employee.query.filter(Employee.last_name.ilike(f"%{search_query}%")).all())

        if address_checked:
            employees.extend(Employee.query.filter(Employee.address.ilike(f"%{search_query}%")).all())
        
        if email_address_checked:
            employees.extend(Employee.query.filter(Employee.email_address.ilike(f"%{search_query}%")).all())

        response = make_response(render_template('admin_view.html', search_employee=employees), 200)
        return response

api.add_resource(EmployeeSearchResource, '/admin/employee/search')