from src import config, app, db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG)
