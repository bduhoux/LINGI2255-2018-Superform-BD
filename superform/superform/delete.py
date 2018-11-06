from flask import Blueprint, url_for, redirect, request, abort

from superform.utils import login_required
from superform.models import db, Post, Publishing

delete_page = Blueprint('delete', __name__)


@delete_page.route('/delete/<int:id>')
@login_required()
def delete_post(id):

    publishings = db.session.query(Publishing).filter(Publishing.post_id == id).all()
    for elem in publishings:
        db.session.delete(elem)
        db.session.commit()

    post = db.session.query(Post).filter(Post.id == id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))
