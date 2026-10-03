from flask import Blueprint, render_template
from flask_login import current_user
from models import Opportunity

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    total_opportunities = Opportunity.query.count()
    if current_user.is_authenticated and current_user.role == 'admin':
        return render_template('index.html', total_opportunities=total_opportunities)
    return render_template('index.html', total_opportunities=total_opportunities)
