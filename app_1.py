from datetime import datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for

from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meeting.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Room {self.id}>'
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

class ReserveInfo(db.Model):
    # __tablename__ = 'reservations'  # 自定义表名
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), nullable=False)
    person = db.Column(db.String(128), nullable=False)
    date = db.Column(db.String(128), nullable=False)
    start_time = db.Column(db.String(128), nullable=False)
    end_time = db.Column(db.String(128), nullable=False)
    landline = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(128), nullable=False)
    item = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Room {self.id}>'
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()  # 在应用上下文中创建所有数据库表

#
# class RegistrationForm(FlaskForm):
#     username = StringField('username', validators=[DataRequired(), Length(min=4, max=25)])
#     password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=16)])
#     confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/register', methods=['GET', 'POST'])    #装饰器，用于定义路由，这里整段code可以称为一个路由
# def register():#视图函数
#     print("aaaaaaa")
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None:
#             hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
#             new_user = User(username=form.username.data, password_hash=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful! Please login.')
#             return redirect(url_for('login'))  # Assuming you have a login route
#         else:
#             flash('Username already exists.')
#     return render_template('register.html', form=form)

@app.route('/register', methods=['GET', 'POST'])     #装饰器，用于定义路由，这里整段code可以称为一个路由
def register():#视图函数
    print("aaaaaaa")
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if username != None and password != None and password == confirm_password:
        user = User.query.get(username)
        if user:
            _ = "此账号已存在"
            flash('此账号已存在')
            return 'I此账号已存在'
        else:
            # user = User.query.filter_by(username=form.username.data).first()
            # if user is None:
            new_user = User(username=username, password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            print("qqqqqq:", username, password, confirm_password)
            flash('Registration successful! Please login.')
            # return render_template('login.html')
            return redirect(url_for('login'))  # Assuming you have a login route

    else:
        return render_template('register.html')


# Login form submission route
# 后面改为使用Flask-Login扩展
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.get(username)
        if user:
            get_password = user.password_hash
            if password == get_password:
                session['current_user_name'] = username
                # print("current_user_name: ",current_user_name)
                return redirect(url_for('home'))
            else:
                flash('密码错误.')
                return 'Invalid username or password'
        else:
            flash('.')
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

# Login route
@app.route('/')
def index():
    return redirect(url_for('billboard'))


@app.route('/billboard')
def billboard():
    return render_template('billboard.html')

# Logout route
@app.route('/logout')
def logout():
    return render_template('logout.html')


# register route
# @app.route('/register')
# def register():
#     return render_template('register.html')



@app.route('/linshi')
def linshi():
    return render_template('linshi.html')

# register route
@app.route('/forget')
def forget():
    return render_template('forget.html')

# reserve route
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    date = request.form.get('date')
    room_name = request.form.get('room_name')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    landline = request.form.get('landline')
    number = request.form.get('number')
    item = request.form.get('item')

    if 'current_user_name' in session and session['current_user_name'] is not None:
        current_user_name = session['current_user_name']

    if current_user_name != None and date != None and room_name != None and start_time != None \
            and end_time != None and landline != None and number != None and item != None :
        # user = User.query.get(username)

        # reserve_info = ReserveInfo.query.filter(or_(ReserveInfo.date == date, ReserveInfo.room_name == room_name)).all()

        # if user:
        #     _ = "此账号已存在"
        #     flash('此账号已存在')
        #     return 'I此账号已存在'
        # else:
            # user = User.query.filter_by(username=form.username.data).first()
            # if user is None:

        new_reserveInfo = ReserveInfo(room_name=room_name, person=current_user_name, date=date, start_time=start_time,
                                      end_time=end_time, landline=landline, number=number, item=item)
        db.session.add(new_reserveInfo)
        db.session.commit()
        print("预定成功:",room_name,current_user_name,date,start_time,end_time,landline,number,item)
        # flash('Registration successful! Please login.')
        return render_template('reserve.html')
            # return redirect(url_for('login'))  # Assuming you have a login route
            # else:
            #     flash('Username already exists.')
    # return render_template('register.html', form=form)
    else:
        print("预定失败:",room_name,current_user_name,date,start_time,end_time,landline,number,item)
        return render_template('reserve.html')

# reserve route
@app.route('/reserve_info', methods=['GET', 'POST'])
def reserve_info():
    return render_template('reserve_info.html')


reserve_data = {
        "columns": ["#", "First name", "Progress", "Amount", "Deadline"],
        "data": [
            {
                "user_id": 1,
                "first_name": "Herman Beck",
                "progress": 25,
                "amount": 77.99,
                "deadline": "May 15, 2015"
            },
            {
                "user_id": 3,
                "first_name": "Messsy Adam",
                "progress": 75,
                "amount": 245.30,
                "deadline": "July 1, 2015"
            }
        ]
    }

@app.route('/api/reserve', methods=['GET'])
def get_reservations():
    return jsonify(reserve_data)


# 更新数据
@app.route('/api/reserve/<int:user_id>', methods=['PUT'])
def update_reserve_data(user_id):
    data = request.get_json()

    print(user_id,data)
    # 操作数据更新

    if user_id==1:
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


# 删除数据
@app.route('/api/reserve/<int:item_id>', methods=['DELETE'])
def delete_reserve(item_id):
    # 这里添加删除逻辑
    # 从数据库中删除指定的记录
    print("+++++++++",item_id)
    return '', 204  # 返回204 No Content

@app.route('/user')
def user():
    return render_template("user_info.html")



# Booking page route
@app.route('/booking')
def booking():
    # Here you can add authentication logic to check if the user is logged in
    # If not logged in, redirect to the login page
    return render_template('index.html')

@app.route('/test1')
def test1():
    return render_template("test1.html")

@app.route('/test2')
def test2():
    return render_template("test2.html")


if __name__ == '__main__':
    # db.create_all()  # Create all database tables
    app.run(debug=True)
