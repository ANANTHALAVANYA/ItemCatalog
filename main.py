from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base,PenDrivesCompanyName,PenDriveName,PenDriveUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///pendrives.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "PenDrives Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
pendrives = session.query(PenDrivesCompanyName).all()


# login
@app.route('/login')
def showLogin():
    
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    pendrives = session.query(PenDrivesCompanyName).all()
    pdcm = session.query(PenDriveName).all()
    return render_template('login.html',
                           STATE=state, pendrives=pendrives, pdcm=pdcm)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = PenDriveUser(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
    session.commit()
    user = session.query(PenDriveUser).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(PenDriveUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(PenDriveUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

#####
# Home
@app.route('/')
@app.route('/home')
def home():
    pendrives = session.query(PenDrivesCompanyName).all()
    return render_template('myhome.html', pendrives=pendrives)

#####
# PenDrive Category for admins
@app.route('/PenDriveStore')
def PenDriveStore():
    try:
        if login_session['username']:
            name = login_session['username']
            pendrives = session.query(PenDrivesCompanyName).all()
            pdpdcc = session.query(PenDrivesCompanyName).all()
            pdcm = session.query(PenDriveName).all()
            return render_template('myhome.html', pendrives=pendrives,
                                   pdpdcc=pdpdcc, pdcm=pdcm, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing pendrives based on PenDrive category
@app.route('/PenDriveStore/<int:pdccid>/AllCompanys')
def showPenDrives(pdccid):
    pendrives = session.query(PenDrivesCompanyName).all()
    pdpdcc = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pdcm = session.query(PenDriveName).filter_by(pendrivecompanyid=pdccid).all()
    try:
        if login_session['username']:
            return render_template('showPenDrives.html', pendrives=pendrives,
                                   pdpdcc=pdpdcc, pdcm=pdcm,
                                   uname=login_session['username'])
    except:
        return render_template('showPenDrives.html',
                               pendrives=pendrives, pdpdcc=pdpdcc, pdcm=pdcm)

#####
# Add New pendrives
@app.route('/PenDriveStore/addPenDriveCompany', methods=['POST', 'GET'])
def addPenDriveCompany():
    if request.method == 'POST':
        company = PenDrivesCompanyName(name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('PenDriveStore'))
    else:
        return render_template('addPenDriveCompany.html', pendrives=pendrives)

########
# Edit Pendrive Category
@app.route('/PenDriveStore/<int:pdccid>/edit', methods=['POST', 'GET'])
def editPenDriveCategory(pdccid):
    editedpds = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    creator = getUserInfo(editedpds.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this PenDrive Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('PenDriveStore'))
    if request.method == "POST":
        if request.form['name']:
            editedpds.name = request.form['name']
        session.add(editedpds)
        session.commit()
        flash("Byke Category Edited Successfully")
        return redirect(url_for('PenDriveStore'))
    else:
        # pendrives is global variable we can them in entire application
        return render_template('editPenDriveCategory.html',
                               tb=editedpds, pendrives=pendrives)

######
# Delete pendrive Category
@app.route('/PenDriveStore/<int:pdccid>/delete', methods=['POST', 'GET'])
def deletePenDriveCategory(pdccid):
    tb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Pendrive Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('PenDriveStore'))
    if request.method == "POST":
        session.delete(tb)
        session.commit()
        flash("PenDrive Category Deleted Successfully")
        return redirect(url_for('PenDriveStore'))
    else:
        return render_template('deletePenDriveCategory.html', tb=tb, pendrives=pendrives)

######
# Add New pendrive Name Details
@app.route('/PenDriveStore/addCompany/addpendrivedetails/<string:cppname>/add',
           methods=['GET', 'POST'])
def addPenDriveDetails(cppname):
    pdpdcc = session.query(PenDrivesCompanyName).filter_by(name=cppname).one()
    # See if the logged in user is not the owner of pendrive
    creator = getUserInfo(pdpdcc.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new Pendrive edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showPenDrives', pdccid=pdpdcc.id))
    if request.method == 'POST':
        name = request.form['name']
        drives_number = request.form['drives_number']
        item_capacity = request.form['item_capacity']
        drive_name= request.form['drive_name']
        item_color = request.form['item_color']
        transferspeed = request.form['transferspeed']
        item_cost = request.form['item_cost']
        warranty = request.form['warranty']
        pendrivedetails = PenDriveName(name=name, drives_number=drives_number,
                              item_capacity=item_capacity, drive_name=drive_name,
                              item_color=item_color,
                              transferspeed=transferspeed,
                              item_cost=item_cost,
                              warranty=warranty,             
                              date=datetime.datetime.now(),
                              PenDrivesCompanyNameid=pdpdcc.id,
                              user_id=login_session['user_id'])
        session.add(pendrivedetails)
        session.commit()
        return redirect(url_for('showPenDrives', pdccid=pdpdcc.id))
    else:
        return render_template('addPenDriveDetails.html',
                               cppname=pdpdcc.name, pendrives=pendrives)

######
# Edit Pendrive details
@app.route('/PenDriveStore/<int:pdccid>/<string:pdpdname>/edit',
           methods=['GET', 'POST'])
def editPenDrive(pdccid, pdpdname):
    tb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pendrivedetails= session.query(PenDriveName).filter_by(name=pdpdname).one()
    # See if the logged in user is not the owner of pendrive
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this PENDRIVE edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showPenDrives', pdccid=tb.id))
    # POST methods
    if request.method == 'POST':
        pendrivedetails.name = request.form['name']
        pendrivedetails.drives_number = request.form['drives_number']
        pendrivedetails.item_capacity = request.form['item_capacity']
        pendrivedetails.drive_name = request.form['drive_name']
        pendrivedetails.item_color = request.form['item_color']
        pendrivedetails.transferspeed = request.form['transferspeed']
        pendrivedetails.item_cost = request.form['item_cost']
        pendrivedetails.warranty= request.form['warranty']
        pendrivedetails.date = datetime.datetime.now()
        session.add(pendrivedetails)
        session.commit()
        flash("pendrive Edited Successfully")
        return redirect(url_for('showPenDrives', pdccid=pdccid))
    else:
        return render_template('editPenDrive.html',
                               pdccid=pdccid, pendrivedetails=pendrivedetails, pendrives=pendrives)

#####
# Delte pendrive Edit
@app.route('/PenDriveStore/<int:pdccid>/<string:pdpdname>/delete',
           methods=['GET', 'POST'])
def deletePenDrive(pdccid, pdpdname):
    tb = session.query(PenDrivesCompanyName).filter_by(id=pdccid).one()
    pendrivedetails = session.query(PenDriveName).filter_by(name=pdpdname).one()
    # See if the logged in user is not the owner of pendrive
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this Pendrive edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showPenDrives', pdccid=tb.id))
    if request.method == "POST":
        session.delete(pendrivedetails)
        session.commit()
        flash("Deleted Pendrive Successfully")
        return redirect(url_for('showPenDrives', pdccid=pdccid))
    else:
        return render_template('deletePenDrive.html',
                               pdccid=pdccid, pendrivedetails=pendrivedetails, pendrives=pendrives)

####
# Logout from current user
@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json
@app.route('/PenDriveStore/JSON')
def allPenDrivesJSON():
    pendrivecategories = session.query(PenDrivesCompanyName).all()
    category_dict = [c.serialize for c in pendrivecategories]
    for c in range(len(category_dict)):
        pendrives = [i.serialize for i in session.query(
                 PenDriveName).filter_by(pendrivecompanyid=category_dict[c]["id"]).all()]
        if pendrives:
            category_dict[c]["byke"] = pendrives
    return jsonify(PenDrivesCompanyName=category_dict)

####
@app.route('/PenDriveStore/pendriveCategories/JSON')
def categoriesJSON():
    pendrives = session.query(PenDrivesCompanyName).all()
    return jsonify(pendriveCategories=[c.serialize for c in pendrives])

####
@app.route('/PenDriveStore/pendrives/JSON')
def itemsJSON():
    items = session.query(PenDriveName).all()
    return jsonify(pendrives=[i.serialize for i in items])

#####
@app.route('/PenDriveStore/<path:pendrive_name>/pendrives/JSON')
def categoryItemsJSON(pendrive_name):
    pendriveCategory = session.query(PenDrivesCompanyName).filter_by(name=pendrive_name).one()
    pendrives = session.query(PenDriveName).filter_by(PenDriveName=pendriveCategory).all()
    return jsonify(pendriveEdtion=[i.serialize for i in pendrives])

#####
@app.route('/PenDriveStore/<path:pendrive_name>/<path:edition_name>/JSON')
def ItemJSON(pendrive_name, edition_name):
    pendriveCategory = session.query(PenDrivesCompanyName).filter_by(name=pendrive_name).one()
    pendriveEdition = session.query(PenDriveName).filter_by(
           name=edition_name, PenDriveName=pendriveCategory).one()
    return jsonify(pendriveEdition=[pendriveEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
