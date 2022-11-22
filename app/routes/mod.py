from flask import Blueprint
from flask_login import login_required

from app.utils.utils import Permission
from app.utils.decorator import permission_required

bp_mod = Blueprint("mod", __name__)


@bp_mod.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "Para moderadores!"