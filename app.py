from flask import *
from flask_pymongo import PyMongo
from flask_moment import Moment
import datetime
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['MONGO_URI'] = "mongodb://localhost:27017/full-stack-web-development4"
app.secret_key = \
    b"h\xa2\\xe\xdc\x82*\xffc<<vx\xa0\x84\xfe\xcd\xdd/?,\x8d\x89\xfd.T;\xb0\fdasdfa/sdfa/assdf" \
    b"jwijiwjiejijeijfijifjidjofdijpoijdipjiojdiodijijzx2838 amr33j8j82j8j jj8jxae\x1a\x9f\\x`."
mongo = PyMongo(app)
moment = Moment(app)



@app.route('/', methods=['GET', 'POST'])
def register():
    try:
        if session['logged_in'] != {}:
            flash('You Are Already Logged In')
            return redirect('/home')
    except:
        pass
    if request.method == 'GET':
        return render_template('register.html', year=datetime.date.today().year)
    elif request.method == 'POST':
        if request.form['confirm_password'] == request.form['password']:
            if mongo.db.users.find_one({'email': request.form['email']}) is None:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                email = request.form['email']
                password = request.form['password']
                mongo.db.users.insert_one({
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': password
                })
                session['logged_in'] = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'logged_in_time': datetime.datetime.utcnow()
                }
                flash('Successfully Logged In')
                return redirect('/home')
            else:
                flash('Account with That Email Already Exists')
        else:
            flash('Confirm Password Does Not Match Password')
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['logged_in'] != {}:
            flash('You Are Already Logged In')
            return redirect('/home')
    except:
        pass
    if request.method == 'GET':
        return render_template('login.html', year=datetime.date.today().year)
    elif request.method == 'POST':
        if mongo.db.users.find_one({'email': request.form['email'], 'password': request.form['password']}) is not None:
            found = mongo.db.users.find_one(
                {'email': request.form['email'], 'password': request.form['password']}
            )
            info = {
                'first_name': found['first_name'],
                'last_name': found['last_name'],
                'email': request.form['email'],
                'logged_in_time': datetime.datetime.utcnow()
            }
            session['logged_in']  = info
            flash('Successfully Logged In')
            return redirect('/home')
        else:
            if mongo.db.users.find_one({'email': request.form['email']}) is None:
                flash('An Account with That Email Address Does Not Exist')
                return redirect('/login')
            else:
                flash('Wrong Password')
                return redirect('/login')


@app.route('/home')
def home():
    try:
        if session['logged_in'] == {}:
            flash('You Not Already Logged In')
            return redirect('/')
    except:
        flash('You Are Not Logged In')
        return redirect('/')
    time_diff = (datetime.datetime.utcnow() - session['logged_in']['logged_in_time']).seconds
    return render_template('home.html', logged_in=session['logged_in'], time_diff=time_diff/86400, year=datetime.date.today().year)

@app.route('/logout')
def logout():
    session['logged_in'] = {}
    return redirect('/')


@app.errorhandler(HTTPException)
def page_not_found(e):
    return render_template('page_not_found.html', error=e, year=datetime.date.today().year, title="Page Not Found")


app.add_template_global(datetime.datetime.utcnow, name='utcnow')
app.add_template_global(datetime.timedelta, name='timedelta')


if __name__ == '__main__':
    app.run()