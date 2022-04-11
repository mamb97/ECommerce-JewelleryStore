from flask import render_template, request, Blueprint, redirect, url_for, session
from datetime import datetime
from database import get_db

account_api = Blueprint('account_api', __name__)
account_db = get_db().accounts


@account_api.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        input_body = request.form
        firstname = input_body.get('firstname', '').strip().lower()
        lastname = input_body.get('lastname', '').strip().lower()
        email = input_body.get('email', '').strip().lower()
        address = input_body.get('address', '').strip().lower()
        city = input_body.get('city', '').strip().lower()
        state = input_body.get('state', '').strip().lower()
        country = input_body.get('country', '').strip().lower()
        # zipcode = input_body.get('zipcode', '').strip
        password = input_body.get('password', '').strip()
        confpassword = input_body.get('confpassword', '').strip()
        sq1 = input_body.get('sq1', '').strip().lower()
        sq2 = input_body.get('sq2', '').strip().lower()
        sq3 = input_body.get('sq3', '').strip().lower()

        if not (firstname and lastname and email and address and city and state and country and password and
                confpassword and sq1 and sq2 and sq3):
            return "Mandatory fields are missing"

        if len(password) < 6:
            return "Password should be at least 6 characters"

        if password != confpassword:
            return "Password and Confirm Password doesn't match"

        if not (account_db.find_one({'email': email}) is None):
            return "You cannot register with the provided email"

        # if input_body.get(state, '') == 'state':
        #     return "Please select a state from dopdown"
        # Todo: Add zipcode
        account_db.insert_one(
            {'firstname': firstname, 'lastname': lastname, 'email': email, 'address': address, 'city': city,
             'state': state, 'country': country, 'password': password, 'sq1': sq1, 'sq2': sq2, 'sq3': sq3,
             'orders': []})
        return redirect(url_for('account_api.login'))


@account_api.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'GET':
        return render_template('forgot.html')
    else:
        input_body = request.form
        email = input_body.get('email', '').strip().lower()
        newpassword = input_body.get('newpassword', '').strip()
        confnewpassword = input_body.get('confnewpassword', '').strip()
        sq1 = input_body.get('sq1', '').strip().lower()
        sq2 = input_body.get('sq2', '').strip().lower()
        sq3 = input_body.get('sq3', '').strip().lower()

        if not (input_body.get('email', '') and input_body.get('newpassword', '') and
                input_body.get('confnewpassword', '') and input_body.get('sq1', '') and input_body.get('sq2', '') and
                input_body.get('sq3', '')):
            return "Mandatory fields are missing"

        if len(newpassword) < 6:
            return "Password should be at least 6 characters"

        if newpassword != confnewpassword:
            return "Password and Confirm Password fields doesn't match"

        user_record = account_db.find_one({'email': email})

        if user_record and user_record['sq1'] == sq1 and user_record['sq2'] == sq2 and user_record['sq3'] == sq3:
            account_db.update_one({'email': email}, {"$set": {'password': newpassword}})
            return redirect(url_for('account_api.login'))

    return "Unable to verify the request"


@account_api.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        input_body = request.form
        email = input_body.get('email', '').strip().lower()
        password = input_body.get('password', '').strip()

        if not (email and password):
            return "Mandatory fields are missing"

        user_record = account_db.find_one({'email': email})
        if user_record is None or user_record['password'] != password:
            return "Invalid login details"
        session["username"] = email
        return redirect(url_for("product_api.product_list"))


@account_api.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("product_api.product_list"))


@account_api.route("/orders")
def orders():
    if "username" not in session:
        return []
    user_record = account_db.find_one({'email': session["username"]})
    order_records = user_record.get('orders', [])
    for idx in range(len(order_records)):
        record = order_records[idx]
        record['full_address'] = ",".join([record["address"]["address_line_1"], record["address"]["city"],
                                           record["address"]["state"], record["address"]["country"]]).strip()
        record["current_status"] = record["status"][-1][1].title()
        record["order_placement_date"] = datetime.strptime(record["order_id"],
                                                           "%Y%m%d%H%M%S%f").strftime("%m/%d/%Y %H:%M:%S")
        order_records[idx] = record
    return render_template("order.html", orders=order_records, username=session["username"])


@account_api.route('/account', methods=('GET', 'POST'))
def account():
    if "username" not in session:
        return redirect(url_for('product_api.product_list'))

    user_record = account_db.find_one({'email': session["username"]})

    if request.method == 'GET':
        # user_record = account_db.find_one({'email': session["username"]})
        return render_template('account.html', record=user_record, username=session["username"])

    else:
        input_body = request.form
        firstname = input_body.get('firstname', '').strip().lower()
        lastname = input_body.get('lastname', '').strip().lower()
        email = input_body.get('email', '').strip().lower()
        address = input_body.get('address', '').strip().lower()
        city = input_body.get('city', '').strip().lower()
        state = input_body.get('state', '').strip().lower()
        country = input_body.get('country', '').strip().lower()
        # zipcode = input_body.get('zipcode', '').strip
        #password = input_body.get('password', '').strip()
        #confpassword = input_body.get('confpassword', '').strip()
        sq1 = input_body.get('sq1', '').strip().lower()
        sq2 = input_body.get('sq2', '').strip().lower()
        sq3 = input_body.get('sq3', '').strip().lower()

        if not (firstname and lastname and email and address and city and state and country and sq1 and sq2 and sq3):
            return "Mandatory fields are missing"

        # if input_body.get(state, '') == 'state':
        #     return "Please select a state from dropdown"
        # Todo: Add zipcode

        # account_db.update_one(
        #     {'firstname': firstname, 'lastname': lastname, 'email': email, 'address': address, 'city': city,
        #      'state': state, 'country': country, 'password': password, 'sq1': sq1, 'sq2': sq2, 'sq3': sq3,
        #      'orders': []})

        new_user_record = {}

        if firstname != user_record["firstname"]:
            new_user_record['firstname'] = firstname

        if lastname != user_record["lastname"]:
            new_user_record['lastname'] = lastname

        if address != user_record["address"]:
            new_user_record['address'] = address

        if city != user_record["city"]:
            new_user_record['city'] = city

        if state != user_record["state"]:
            new_user_record['state'] = state

        if sq1 != user_record["sq1"]:
            new_user_record['sq1'] = sq1

        if sq2 != user_record["sq2"]:
            new_user_record['sq2'] = sq2

        if sq3 != user_record["sq3"]:
            new_user_record['sq3'] = sq3


        print (new_user_record)

        account_db.update_one({'email': session["username"]}, {"$set": new_user_record})

        user_record.update(new_user_record)

        return render_template('account.html', record=user_record, username=session["username"])
