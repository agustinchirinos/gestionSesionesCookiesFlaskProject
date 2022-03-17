from flask import render_template, abort
from flask_login import login_required, current_user

from . import admin
from ..auth.decorator import admin_required


@admin.route('/adminindex/')
@login_required
@admin_required
def adminindex():  # put application's code here
    # if not current_user.is_admin:
    #     abort(401)
    return render_template('adminindex.html')
