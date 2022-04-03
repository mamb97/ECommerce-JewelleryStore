
from flask import render_template, request, Blueprint, redirect, url_for

from database import get_db

account_api = Blueprint('account_api', __name__)
account_db = get_db().accounts


@account_api.route('/signup/', methods=('GET', 'POST'))
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        input_body = request.form
        firstname = input_body.get('firstname', '').strip().lower()
        lastname = input_body.get('lastname', '').strip().lower()
        email = input_body.get('email', '').strip().lower()
        address = input_body.get('address', '').strip().lower()
        city = input_body.get('city', '').strip().lower()
        state = input_body.get('state', '').strip().lower()
        country = input_body.get('country', '').strip().lower()
        password = input_body.get('password', '').strip()
        confpassword = input_body.get('confpassword', '').strip()
        sq1 = input_body.get('sq1', '').strip().lower()
        sq2 = input_body.get('sq2', '').strip().lower()
        sq3 = input_body.get('sq3', '').strip().lower()

        if not (input_body.get('firstname', '') and input_body.get('lastname', '') and input_body.get('email',
                                                                                                      '') and input_body.get(
            'address', '') and input_body.get('city', '') and input_body.get('state', '') and input_body.get('country',
                                                                                                             '') and input_body.get(
            'password', '') and input_body.get('confpassword',
                                               '') and input_body.get('sq1',
                                                                      '') and input_body.get(
            'sq2', '') and input_body.get('sq3', '')):
            return "Mandatory fields are missing"

        if password != confpassword:
            return "Password and Confirm Password doesn't match"

        if not (len(password) > 5):
            return "Password should be at least 6 characters"

        if not (account_db.find_one({'email': email}) is None):
            return "You cannot register with the provided email"

        # if input_body.get(state, '') == 'state':
        #     return "Please select a state from dopdown"
        # Todo: Add state country and city
        account_db.insert_one({'firstname': firstname, 'lastname': lastname, 'email': email, 'address': address,
                               'password': password, 'sq1': sq1, 'sq2': sq2, 'sq3': sq3})

        return 'Executed insert account details to db - signup fields'

    else:
        return '<h1> Executed account method else statement </h1>'


@account_api.route('/forgot/', methods=('GET', 'POST'))
def forgot():
    if request.method == 'GET':
        return render_template('forgot.html')

    if request.method == 'POST':
        input_body = request.form
        email = input_body.get('email', '').strip().lower()
        newpassword = input_body.get('newpassword', '').strip()
        confnewpassword = input_body.get('confnewpassword', '').strip()
        sq1 = input_body.get('sq1', '').strip().lower()
        sq2 = input_body.get('sq2', '').strip().lower()
        sq3 = input_body.get('sq3', '').strip().lower()

        if not (input_body.get('email', '') and input_body.get('newpassword', '') and input_body.get('confnewpassword',
                                                                                                     '') and input_body.get(
            'sq1', '') and input_body.get('sq2', '') and input_body.get('sq3', '')):
            return "Mandatory fields are missing"

        if (account_db.find_one({'email': email}) is None):
            return "Invalid Email"

        if newpassword != confnewpassword:
            return "Password and Confirm Password fields doesn't match"

        if not (len(newpassword) > 5):
            return "Password should be atleast 6 characters"

        sq = account_db.find_one({'email': email})

        if sq['sq1'] == sq1 and sq['sq2'] == sq2 and sq['sq3'] == sq3:
            account_db.update_one({'email': email}, {"$set": {'password': newpassword}})
            return "Password updated succesfully"

    return "Unable to verify the request"


@account_api.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        input_body = request.form
        email = input_body.get('email', '').strip().lower()
        password = input_body.get('password', '').strip()

        if not (email and password):
            return "Mandatory fields are missing"

        if (account_db.find_one({'email': email}) is None):
            return "Invalid Email"

        # Todo - session creation is pending

        auth =  account_db.find_one({'email': email})
        if auth['email'] == email and auth['password'] == password:
            return redirect(url_for("product_api.product_list"))

        else:
            return "Incorrect login details"

    else:
        return 'Reset password else statement executed'
