from flask import Blueprint, url_for, redirect, session

from superform.utils import login_required
from superform.models import db, Post, Publishing, User

delete_page = Blueprint('delete', __name__)


@delete_page.route('/delete/<int:id>')
@login_required()
def delete_post(id):
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    post = db.session.query(Post).filter_by(id=id).first()
    post_user_id = post.user_id
    if user is not None:
        if post_user_id == user.id:
            publishings = db.session.query(Publishing).filter(Publishing.post_id == id).all()
            for elem in publishings:
                db.session.delete(elem)
                db.session.commit()

            post = db.session.query(Post).filter(Post.id == id).first()
            db.session.delete(post)
            db.session.commit()

    return redirect(url_for('index'))
