from flask import Blueprint
from flask_login import login_required

from app.utils.decorator import admin_required

bp_admin = Blueprint("admin", __name__)


@bp_admin.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "Solo para admins!"
