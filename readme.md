# Blog App

This is a blog app, made with Flask.

## Running

- Set up a Python virtual environment

  ```bash
  python -m venv venv
  venv\scripts\activate
  ```

- Install project dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Create your `.env` file

  ```bash
  cp .env-sample .env
  ```

- Run the app

  ```bash
  flask run --debug
  ```

## Developing Your Own Version

To develop your own version of this project, you can `clone` or `fork` this repo.

- `git clone <repo url>` makes a copy of the repo, but still considers the upstream (parent) repo to be this repo. This is fine for development and testing, but the remote repo still belongs to me.
- Forking the repo makes a copy of the repo on _your_ GitHub account, meaning that you have full control of it from that point forward. This is the better approach when you want to make your own version of an existing project, as opposed to contributing to the original one.

## Database Migrations

### Making New Migrations

`flask db migrate -m "commit message"`

### Applying Migrations to Existing DBs

`flask db upgrade`

## Credits

- [Flask](https://flask.palletsprojects.com/en/stable/)
- Architecture inspo from [AshleyAlexJacob](https://github.com/AshleyAlexJacob/Flask-API-Folder-Guide-2023)
