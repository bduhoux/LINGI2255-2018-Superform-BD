from flask import Blueprint, url_for, redirect, session, render_template, request

from superform.utils import login_required
from superform.models import db, Post, Publishing, User

from superform.plugins.facebook import delete

delete_page = Blueprint('delete', __name__)


@delete_page.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required()
def delete_post(id):
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None

    if user is not None:
        post = db.session.query(Post).filter_by(id=id).first()
        if post is not None:
            post_user_id = post.user_id
            if post_user_id == user.id:
                publishings = db.session.query(Publishing).filter(Publishing.post_id == id).all()
                post_del_cond = True
                for pub in publishings:
                    # If the publishing is not yet validated
                    if is_not_validated(pub):
                        db.session.delete(pub)
                        db.session.commit()
                    # If the publishing has been posted already (not archived)
                    elif pub.state == 1:
                        # If the checkbox for Facebook is checked
                        if request.form.get('Facebook'):
                            # Delete post on Facebook
                            #fb_post_id = pub.extra
                            # delete(fb_post_id)
                            pass
                    else:
                        post_del_cond = False

                # post = db.session.query(Post).filter(Post.id == id).first()
                # If every publishing linked to the post has been deleted (otherwise violation of constraint in db)
                if post_del_cond:
                    db.session.delete(post)
                    db.session.commit()
            else:
                # The user trying to delete the post is not the one who created it
                return render_template('403.html'), 403
        else:
            # The post does not exist
            return render_template('404.html'), 404
    else:
        # User is not connected
        return render_template('403.html'), 403

    return redirect(url_for('index'))


def is_not_validated(pub):
    if pub.state != -1 and pub.state != 0:
        return False

    return True
