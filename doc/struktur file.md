├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── password.py
│   │   └── security.py
│   ├── models/
│   │   ├── admin.py
│   │   ├── product.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── product.py
│   │   └── user.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       ├── auth.py
│       └── products.py
├── doc/
│   └── ...
├── static/
│   └── ...
├── templates/
│   ├── admin.html
│   ├── admin_user_detail.html
│   ├── change_password.html
│   ├── index.html
│   ├── login.html
│   ├── praregister.html
│   ├── profile.html
│   └── register.html
├── .env
├── .gitignore
├── alembic.ini
├── create_admin.py
└── README.md

├── /admin
│   ├── .get("/dashboard")
│   ├── .get("/members/list")
│   ├── .get("/members{member_id}")
│   ├── .get("/members/{member_id}/photo")
│   ├── .post("/members/{member_id}/approve")
│   ├── .post("/members/{member_id}/reset-password")
│   ├── .get("/member{member_id}/preview")
│   ├── .get("/members/{member_id}/edit-profile")
│   ├── .post("/members/{member_id}/edit-profile")
│
├── /auth
│   ├── def verify_admin
│   ├── def verify_user
│   ├── .get("/login")
│   ├── .post("/login")
│   ├── .get("/logout")
│
├── /dashboard
│   ├── .get("/me")
│   ├── .get("/profile")
│   ├── def get_current_member
│   ├── .get("/change-profile")
│   ├── .post("edit-profile")
│   ├── .post("/profile/photo")
│
├── /users
│   ├── .get("/praregister")
│   ├── .get("/register")
│   ├── .post("/register")
│   ├── .get("/change-password")
│   ├── .post("/change-password")