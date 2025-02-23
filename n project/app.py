from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

# Initialize Flask App
app = Flask(__name__)

# 🔹 Configure App Settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_random_secret_key'  # Change this in production!

# 🔹 Initialize Extensions
from models import db  # Import `db` AFTER defining `app`
db.init_app(app)  # Bind `db` to `app`
csrf = CSRFProtect(app)

# 🔹 Ensure tables are created
with app.app_context():
    db.create_all()

# Import Models & Forms AFTER `db.init_app(app)`
from models import Lead
from forms import LeadForm

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# View Leads
@app.route('/leads')
def view_leads():
    leads = Lead.query.all()
    return render_template('leads.html', leads=leads)

# Add Lead
@app.route('/add-lead', methods=['GET', 'POST'])
def add_lead():
    form = LeadForm()
    if form.validate_on_submit():
        existing_lead = Lead.query.filter_by(email=form.email.data).first()
        if existing_lead:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_lead'))

        lead = Lead(
            name=form.name.data,
            email=form.email.data,
            company=form.company.data
        )
        db.session.add(lead)
        db.session.commit()
        flash('Lead added successfully!', 'success')
        return redirect(url_for('view_leads'))
    
    return render_template('add_lead.html', form=form)

# Run App
if __name__ == '__main__':
    app.run(debug=True)
