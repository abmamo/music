# import admin creation function
from flask import url_for

def create_user(app, environment, User, db):
    with app.app_context():
        # create user
        try:
            # find user
            user = User.query.filter_by(email=app.config["USER_EMAIL"]).first()
            # check email has been found
            if user != None:
                # check password
                if user.check_password(app.config["USER_PASSWORD"]):
                    pass
                else:
                    # update password
                    user.set_password(app.config["USER_PASSWORD"])
                    # save changes
                    db.session.commit()
            else:
                try:
                    # initialize user
                    user = User(email=app.config["USER_EMAIL"], password=app.config["USER_PASSWORD"])
                    # add to session
                    db.session.add(user)
                    db.session.commit()
                    print("user created: %s" % str(user.id))
                    # assert user properly created
                    assert user.id is not None
                except Exception as e:
                    # log
                    print("user confirm failed: %s" % str(e))
                    # return
                    return None
        except Exception as e:
            # log
            print("init user failed: %s" % str(e))
            # return
            return None
        # send confirmation email
        if user.confirmed == False:
            # import mail send function
            from app import send_mail, ts
            try:
                # prepare email
                subject = "confirm account"
                # generate token
                token = ts.dumps(user.email, salt="email-confirm-key")
                with app.app_context():
                    # build recover url
                    confirm_url = url_for("player_bp.confirm_email", token=token, _external=True)
                # alert user
                print("account confirmation sent or use link below: ")
                print(confirm_url)
                # send the emails
                send_mail(
                    subject, app.config["MAIL_USERNAME"], [user.email], confirm_url
                )
            except Exception as e:
                # log
                print("send confirmation failed: %s" % str(e))
                # return error page
                return None