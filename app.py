from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.secret_key = 'your secret key'  

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/apnastore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#  Databse Table
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)



# Search bar
category = {
    'men': 'mens.html',
    'women': 'girl.html',
    'kids': 'kids.html',
    'shoes': 'shooes.html',
    'toys': 'toys.html',
    'traditionalmen': 'traditional men.html',
    'traditionalwomen': 'traditional women.html',
    'watch': 'watch.html',
    'sunglasses': 'watch.html',
}

# Routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/mens')
def mens():
    return render_template("mens.html")

@app.route('/girl')
def girl():
    return render_template("girl.html")

@app.route('/kids')
def kids():
    return render_template("kids.html")

@app.route('/wedding')
def wedding():
    return render_template("traditional women.html")

@app.route('/traditional')
def traditional():
    return render_template("traditional men.html")

@app.route('/order')
def order():
    return render_template("order.html")

@app.route('/shooes')
def shooes():
    return render_template("shooes.html")

@app.route('/watch')
def watch():
    return render_template("watch.html")

@app.route('/winterwear')
def winterwear():
    return render_template("winterwear.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/home')
def homepage():
    return render_template("home.html")

 # user sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        mobile = request.form.get('mobile')

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_password, mobile=mobile)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template("signup.html")


#  User Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_mobile'] = user.mobile
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")

# User Dashboard 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("userdashboard.html", 
                           name=session['user_name'], 
                           email=session['user_email'],
                           mobile=session['user_mobile'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Contact
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        entry = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html")

#Search  bar
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '').lower().strip()
    words = query.split()  

    for cat, filename in category.items():
        
        cat_words = cat.lower().split()
        if all(word in words for word in cat_words):
            return render_template(filename)
    
    return "Sorry! No item found..."


# Run File 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
