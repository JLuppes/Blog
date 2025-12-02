from src import config, app, db
from flask_security import hash_password
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    # one time setup
    with app.app_context():
        # init_db()
        # Create a user and role to test with
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}, title="user"
        )
        db.session.commit()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com",
            password=hash_password("password"), roles=["user"])
        db.session.commit()

    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
