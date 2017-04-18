from flask import render_template, redirect, url_for, flash, Blueprint
from .forms import ChangePassword
from flask_login import login_required, current_user

user_settings = Blueprint('user_settings', __name__, template_folder='templates')

@user_settings.route('/preferences/your-settings', methods=['GET', 'POST'])
@login_required
def preferences():
    form=ChangePassword()
    if form.validate_on_submit():
        if current_user.check_pass_return(form.passwordold.data) == True:
            if form.passwordnew1.data == form.passwordnew2.data:
                if not form.passwordnew1.data == "":
                    current_user.set_password(form.passwordnew1.data)
                    flash("Successfull changed password", "alert-success")
                    return render_template("virtberryusers-user_preferences.html", form=form)
                else:
                    flash("Password cannot be empty", "alert-danger")
                    return render_template("virtberryusers-user_preferences.html", form=form)
            else:
                flash("Second password did not match the first!!", "alert-danger")
                return render_template("virtberryusers-user_preferences.html", form=form)
        else:
            flash("Old password did not match", "alert-danger")
            return render_template("virtberryusers-user_preferences.html", form=form)
    else:
        return render_template("virtberryusers-user_preferences.html", form=form)
