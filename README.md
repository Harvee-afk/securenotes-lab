# SecureNotes API — Weeks 14–15: Secure It, Then Prove It

This is the SecureNotes student lab project with its five security tasks and nine TODO tests completed. The source files keep the original `TASK` marker boundaries in `app/main.py`.

## Features
- Passwords are salted and hashed with bcrypt; login verifies stored hashes.
- Login issues a signed, expiring JWT, and protected routes verify the token.
- Requests without valid credentials return HTTP 401.
- Note ownership is enforced (HTTP 403 for someone else's note).
- Only admins can view `/admin/users`, which excludes passwords and password hashes.

## Install and run

Run these commands inside this project directory:

```bash
python -m venv venv
source venv/bin/activate         # macOS/Linux
# venv\Scripts\activate         # Windows (use this instead)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs.

Development accounts (lab exercises only):
- `admin` / `admin123` (admin)
- `alice` / `alicepass` (owns note 1)
- `bob` / `bobpass` (owns note 2)

## Tests

```bash
pytest -q
pytest --cov=app
```

There are 11 tests (2 examples and 9 completed tests). The `client` fixture in `tests/conftest.py` resets the in-memory database for each test.

Keep the professor-specified `bcrypt==4.0.1` requirement and exclude `venv/` from Git. For any deployment beyond this classroom demonstration, replace the `SECRET_KEY` development default with a long random environment secret and use a real persistent database.

## GitHub peer review

1. Commit the **original starter** files on `main` as the initial commit.
2. Create a `secure-and-test` branch and add the completed files from this project.
3. Commit and push the feature branch, then open a pull request into `main`.
4. Review another pair's PR, leave code comments and approve/request changes.
5. Submit the repo link, your PR link, the reviewed PR link and your completed `TASKS.md`.
