from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy ORM instance
db = SQLAlchemy()

class Project(db.Model):
    """
    Model representing your portfolio projects (C++, Flask, Web Apps, Systems, etc.)
    """
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)  # e.g., "C++, STL, Flask, SQLite"
    github_url = db.Column(db.String(255), nullable=True)
    live_demo_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), default='C++ / Systems')  # 'C++ / Systems', 'Web App', 'DSA Engine'
    featured = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model object to JSON dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
            'tech_stack': [tag.strip() for tag in self.tech_stack.split(',')] if self.tech_stack else [],
            'github_url': self.github_url,
            'live_demo_url': self.live_demo_url,
            'category': self.category,
            'featured': self.featured
        }

class Achievement(db.Model):
    """
    Model representing your achievements, coding ranks, hackathons, and certifications.
    """
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'Competitive Programming', 'Hackathon', 'Certification', 'Academic'
    issuer = db.Column(db.String(100), nullable=False)    # e.g. "LeetCode", "College Contest", "Coursera"
    date_achieved = db.Column(db.String(50), nullable=False) # e.g. "August 2026"
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), default='trophy')    # Icon identifier: trophy, code, star, medal, certificate
    verification_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'issuer': self.issuer,
            'date_achieved': self.date_achieved,
            'description': self.description,
            'icon': self.icon,
            'verification_url': self.verification_url
        }

class DSAProblem(db.Model):
    """
    Model representing Data Structures & Algorithms problems solved with clean C++ code.
    """
    __tablename__ = 'dsa_problems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # 'Arrays & Hashing', 'Trees & Graphs', 'Dynamic Programming', 'Heaps & Graphs'
    difficulty = db.Column(db.String(20), nullable=False) # 'Easy', 'Medium', 'Hard'
    time_complexity = db.Column(db.String(50), nullable=False) # 'O(N)', 'O(N log N)', 'O(V + E)'
    space_complexity = db.Column(db.String(50), nullable=False) # 'O(1)', 'O(N)'
    problem_statement = db.Column(db.Text, nullable=False)
    cpp_solution = db.Column(db.Text, nullable=False) # Well-formatted C++ code
    explanation = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'difficulty': self.difficulty,
            'time_complexity': self.time_complexity,
            'space_complexity': self.space_complexity,
            'problem_statement': self.problem_statement,
            'cpp_solution': self.cpp_solution,
            'explanation': self.explanation
        }

class ContactMessage(db.Model):
    """
    Model for saving visitor contact form messages in the database.
    """
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
