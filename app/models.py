from app import db
from sqlalchemy import Enum, CheckConstraint

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estimate = db.Column(db.Integer)
    title = db.Column(db.String)
    # Define the Enum type for the 'status' field
    status = db.Column(db.String(50), nullable=False, default='Open')
    notes = db.Column(db.String)

    # CheckConstraint to enforce valid values
    __table_args__ = (
        CheckConstraint("status IN ('Open', 'Started', 'Done')", name='valid_status'),
    )
    
    
