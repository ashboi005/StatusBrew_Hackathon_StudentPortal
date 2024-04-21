from flask import Flask,abort, render_template, request, redirect, url_for, session,flash, jsonify
#from flask_login import LoginManager, login_user, logout_user, current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afhuqrfh23r39vq8qydhad919cq9e11euda9qc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hahaok12345@localhost:3306/Hackathon'
#app.config['SQLALCHEMY_ECHO'] = True
#app.config['DEBUG'] = True
db = SQLAlchemy(app)
sheets_scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
sheets_credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets_credentials.json', sheets_scope)
sheets_client = gspread.authorize(sheets_credentials)
drive_scope = ['https://www.googleapis.com/auth/drive']
drive_credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets_credentials.json', drive_scope)
drive_client = gspread.authorize(drive_credentials)

class DashboardDetails(db.Model):
    __tablename__ = 'dashboard_details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    course_name = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    department = db.Column(db.String(100))
    course_code = db.Column(db.String(20))
    parent_name = db.Column(db.String(100))
    relationship = db.Column(db.String(50))
    parent_phone_number = db.Column(db.String(20))
    parent_email = db.Column(db.String(100))
    parent_address = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class ContactForm(db.Model):
    __tablename__ = 'contact_forms'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)

    sent_messages = db.relationship('Message', backref='admin', lazy=True)

    def __repr__(self):
        return f"<Admin(admin_username='{self.admin_username}')>"

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('Admin', backref='messages_sent', foreign_keys=[sender_id])
    recipient = db.relationship('User', backref='received_messages', foreign_keys=[recipient_id])

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_details.id'), nullable=False)
    result_text = db.Column(db.Text, nullable=False)

    user = db.relationship('DashboardDetails', backref='results', lazy=True)

class Fee(db.Model):
    __tablename__ = 'fees'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dashboard_details.id'), nullable=False)
    fee_amount = db.Column(db.Float, nullable=False)
    fee_description = db.Column(db.Text)

    user = db.relationship('DashboardDetails', backref='fees', lazy=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        new_contact = ContactForm(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )

        db.session.add(new_contact)

        db.session.commit()

        return redirect(url_for('index'))

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return 'Username is already taken!'

        new_user = User(username=username, password=password)

        db.session.add(new_user)

        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user_details = None

    if user_id:
        user_details = DashboardDetails.query.filter_by(id=user_id).first()

    return render_template('dashboard.html', user_details=user_details)

@app.route('/submit_details', methods=['POST'])
def submit_details():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        dob = request.form['date_of_birth']
        gender = request.form['gender']
        phone = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        course_name = request.form['course_name']
        semester = request.form['semester']
        department = request.form['department']
        course_code = request.form['course_code']
        parent_name = request.form['parent_name']
        relationship = request.form['relationship']
        parent_phone = request.form['parent_phone_number']  # Corrected column name
        parent_email = request.form['parent_email']
        parent_address = request.form['parent_address']

        new_details = DashboardDetails(
            name=name,
            student_id=student_id,
            date_of_birth=dob,
            gender=gender,
            phone_number=phone,
            email=email,
            address=address,
            course_name=course_name,
            semester=semester,
            department=department,
            course_code=course_code,
            parent_name=parent_name,
            relationship=relationship,
            parent_phone_number=parent_phone,
            parent_email=parent_email,
            parent_address=parent_address
        )

        db.session.add(new_details)
        db.session.commit()

        flash('Data submitted successfully.', 'success')
        return redirect(url_for('dashboard'))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['admin_username']
        password = request.form['admin_password']

        admin = Admin.query.filter_by(admin_username=username, admin_password=password).first()

        if admin:
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    users = DashboardDetails.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/edit_dashboard/<int:user_id>')
def edit_dashboard(user_id):
    user = DashboardDetails.query.get_or_404(user_id)
    return render_template('editable_dashboard.html', user=user)

@app.route('/update_details/<int:user_id>', methods=['POST'])
def update_details(user_id):
    user = DashboardDetails.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.student_id = request.form['student_id']
        user.date_of_birth = request.form['date_of_birth']
        user.gender = request.form['gender']
        user.phone_number = request.form['phone_number']
        user.email = request.form['email']
        user.address = request.form['address']
        user.course_name = request.form['course_name']
        user.semester = request.form['semester']
        user.department = request.form['department']
        user.course_code = request.form['course_code']
        user.parent_name = request.form['parent_name']
        user.relationship = request.form['relationship']
        user.parent_phone_number = request.form['parent_phone_number']
        user.parent_email = request.form['parent_email']
        user.parent_address = request.form['parent_address']

        db.session.commit()
        flash('User details updated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/send_message/<int:user_id>', methods=['POST'])
def send_message(user_id):
    if request.method == 'POST':
        message_content = request.form['message']
        if 'admin_id' in session:
            sender_id = session['admin_id']
            admin = Admin.query.get(sender_id)
            if not admin:
                abort(401)
        else:
                abort(401)

        new_message = Message(sender_id=sender_id, recipient_id=user_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()

        return 'Message sent successfully.'

@app.route('/messages')
def messages():
    user_id = session.get('user_id')
    if not user_id:
        abort(401, description="Unauthorized")

    messages = Message.query.filter_by(recipient_id=user_id).all()

    return render_template('messages.html', messages=messages)

@app.route('/message_system/<int:user_id>')
def message_system(user_id):
    user = DashboardDetails.query.get_or_404(user_id)
    return render_template('message_system.html', user=user)

@app.route('/result_system/<int:user_id>')
def result_system(user_id):
    user = DashboardDetails.query.get_or_404(user_id)
    return render_template('result_system.html', user=user)

@app.route('/add_result/<int:user_id>', methods=['POST'])
def add_result(user_id):
    if request.method == 'POST':
        result_text = request.form['result_text']

        new_result = Result(user_id=user_id, result_text=result_text)
        db.session.add(new_result)
        db.session.commit()

        flash('Result added successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/result')
def result():
    user_id = session.get('user_id')
    user_details = None

    if user_id:
        user_details = DashboardDetails.query.filter_by(id=user_id).first()

    return render_template('result.html', user_details=user_details)

@app.route('/fees_system/<int:user_id>')
def fees_system(user_id):
    user = DashboardDetails.query.get_or_404(user_id)
    return render_template('fees_system.html', user=user)

@app.route('/add_fee/<int:user_id>', methods=['POST'])
def add_fee(user_id):
    if request.method == 'POST':
        fee_amount = request.form['fee_amount']
        fee_description = request.form['fee_description']

        new_fee = Fee(user_id=user_id, fee_amount=fee_amount, fee_description=fee_description)
        db.session.add(new_fee)
        db.session.commit()

        flash('Fee added successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/fee')
def fee():
    user_id = session.get('user_id')
    user_details = None

    if user_id:
        user_details = DashboardDetails.query.filter_by(id=user_id).first()

    return render_template('fee.html', user_details=user_details)

@app.route('/attendance')
def attendance():
    sheet = sheets_client.open('Iot attendance').sheet1
    data = sheet.get_all_records()
    return render_template('attendance.html', data=data)

@app.route('/student_attendance')
def student_attendance():
    user_id = session.get('user_id')
    if user_id:
        student_details = DashboardDetails.query.filter_by(id=user_id).first()
        if student_details:
            student_name = student_details.name
            sheet = sheets_client.open('Iot attendance').sheet1
            all_records = sheet.get_all_records()
            student_attendance_records = [record for record in all_records if record['Student Name'] == student_name]
            return render_template('student_attendance.html', student_name=student_name, attendance_records=student_attendance_records)

    flash('You must be logged in as a student to view attendance records.', 'error')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        if 'login' not in metadata.tables:
            User.__table__.create(bind=db.engine)
        if 'dashboard_details' not in metadata.tables:
            DashboardDetails.__table__.create(bind=db.engine)
        if 'admin' not in metadata.tables:
            Admin.__table__.create(bind=db.engine)
        if 'messages' not in metadata.tables:
            Message.__table__.create(bind=db.engine)
        if 'results' not in metadata.tables:
            Result.__table__.create(bind=db.engine)
        if 'fees' not in metadata.tables:
            Fee.__table__.create(bind=db.engine)
        if 'contact_forms' not in metadata.tables:
            ContactForm.__table__.create(bind=db.engine)
    app.run(debug=True)

