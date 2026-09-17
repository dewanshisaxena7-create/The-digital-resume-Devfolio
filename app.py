import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from config import Config
from models import db, Project, Achievement, DSAProblem, ContactMessage

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Admin Secret Password (default: 'devanshi2026')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'devanshi2026'

# Initialize SQLAlchemy with app
db.init_app(app)

# -------------------------------------------------------------
# PAGE ROUTES (Template Rendering)
# -------------------------------------------------------------

@app.route('/')
def home():
    """
    Main Portfolio Homepage Route.
    Fetches projects, achievements, and DSA problems from SQLite database.
    """
    projects = Project.query.order_by(Project.id.desc()).all()
    achievements = Achievement.query.order_by(Achievement.id.desc()).all()
    dsa_problems = DSAProblem.query.order_by(DSAProblem.id.asc()).all()

    # Calculate summary metrics for hero badges
    stats = {
        'total_projects': len(projects),
        'total_achievements': len(achievements),
        'total_dsa_problems': 400 + len(dsa_problems)
    }

    return render_template('index.html', 
                           projects=projects, 
                           achievements=achievements, 
                           dsa_problems=dsa_problems, 
                           stats=stats)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Admin Password Authentication Login Route.
    """
    if session.get('admin_logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully authenticated as Admin!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid Admin Password. Access Denied.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """
    Admin Logout Route.
    """
    session.pop('admin_logged_in', None)
    flash('Logged out of Admin Portal.', 'success')
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Protected Admin Dashboard Route.
    Requires session authentication.
    """
    # Protect admin route with session check
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_project':
            new_proj = Project(
                title=request.form.get('title'),
                subtitle=request.form.get('subtitle'),
                description=request.form.get('description'),
                tech_stack=request.form.get('tech_stack'),
                github_url=request.form.get('github_url'),
                live_demo_url=request.form.get('live_demo_url'),
                category=request.form.get('category')
            )
            db.session.add(new_proj)
            db.session.commit()
            flash('Project added successfully to SQL database!', 'success')

        elif action == 'add_achievement':
            new_ach = Achievement(
                title=request.form.get('title'),
                category=request.form.get('category'),
                issuer=request.form.get('issuer'),
                date_achieved=request.form.get('date_achieved'),
                description=request.form.get('description'),
                icon=request.form.get('icon'),
                verification_url=request.form.get('verification_url')
            )
            db.session.add(new_ach)
            db.session.commit()
            flash('Achievement added successfully to SQL database!', 'success')

        elif action == 'add_dsa':
            new_dsa = DSAProblem(
                title=request.form.get('title'),
                category=request.form.get('category'),
                difficulty=request.form.get('difficulty'),
                time_complexity=request.form.get('time_complexity'),
                space_complexity=request.form.get('space_complexity'),
                problem_statement=request.form.get('problem_statement'),
                cpp_solution=request.form.get('cpp_solution'),
                explanation=request.form.get('explanation')
            )
            db.session.add(new_dsa)
            db.session.commit()
            flash('DSA C++ Problem added successfully!', 'success')

        return redirect(url_for('admin'))

    projects = Project.query.all()
    achievements = Achievement.query.all()
    dsa_problems = DSAProblem.query.all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()

    return render_template('admin.html', projects=projects, achievements=achievements, dsa_problems=dsa_problems, messages=messages)

# -------------------------------------------------------------
# REST API ENDPOINTS (JSON Responses)
# -------------------------------------------------------------

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects])

@app.route('/api/projects/<int:id>', methods=['GET'])
def get_project_detail(id):
    proj = Project.query.get_or_404(id)
    return jsonify(proj.to_dict())

@app.route('/api/dsa', methods=['GET'])
def get_dsa_problems():
    problems = DSAProblem.query.all()
    return jsonify([p.to_dict() for p in problems])

@app.route('/api/dsa/<int:id>', methods=['GET'])
def get_dsa_problem_detail(id):
    prob = DSAProblem.query.get_or_404(id)
    return jsonify(prob.to_dict())

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json() or request.form
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'status': 'error', 'message': 'Please fill out all required fields'}), 400

    msg = ContactMessage(name=name, email=email, subject=subject or 'Portfolio Inquiry', message=message)
    db.session.add(msg)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Thank you! Your message has been received.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Flask Portfolio Server on http://127.0.0.1:8000 ...")
    app.run(debug=True, port=8000)
