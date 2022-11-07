from flask import Blueprint
from flask import render_template,redirect,url_for,flash,abort
from dmenu.menus.forms import UploadForm

from dmenu.models import Menu
from flask_login import current_user,login_required
from dmenu import db
from dmenu.menus.utils import save_picture


menus = Blueprint('menus',__name__)

@menus.route('/upload',methods=['GET','POST'])
@login_required
def upload_menu():
    form = UploadForm()
    if form.validate_on_submit():
        picture_file=save_picture(form.menu_photo.data)
        menu = Menu(title=form.title.data,content=picture_file,user_id=current_user.id)
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for('users.admin_page'))
    return render_template("upload_menu.html",title='Upload Menu',form=form)


@menus.route("/admin/<int:menu_id>/delete")
@login_required
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if menu.author != current_user:
        abort(403)
    db.session.delete(menu)
    db.session.commit()
    flash('Selected menu has been deleted!','success')
    return redirect(url_for("users.admin_page"))


@menus.route('/menus/<int:user_id>')
def rest_menu(user_id):
    user_menus=Menu.query.order_by(Menu.date_posted.desc()).filter_by(user_id=user_id)
    return render_template("menu1.html",menus=user_menus)