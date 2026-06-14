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