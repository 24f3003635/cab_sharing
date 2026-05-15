from flask import jsonify, Blueprint, request
from app.models import User
from datetime import datetime, date,timedelta
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy import or_, distinct
from app.database import db

api_bp=Blueprint("api",__name__)


@api_bp.route("/test")          
def test():
    return jsonify({"message":"api working"})