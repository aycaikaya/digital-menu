from flask import Blueprint
from flask import render_template
main = Blueprint('main',__name__)




@main.route('/')
@main.route('/home',methods=['GET','POST'])
def home():
    return render_template("index.html",title="Home")






