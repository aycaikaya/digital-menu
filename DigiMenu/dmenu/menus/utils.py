import secrets
import os
from flask import current_app
from PIL import Image



def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _ ,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path=os.path.join(current_app.root_path,'static/menu_uploads',picture_fn)
    output=(2400,1600)
    i = Image.open(form_picture)
    i.thumbnail(output)
    i.save(picture_path)
    return picture_fn