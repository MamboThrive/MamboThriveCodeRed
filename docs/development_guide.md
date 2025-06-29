
# Development Guide

## Setup
```bash
git clone https://github.com/youruser/mambohealth.git
cd mambohealth
pip install -r requirements.txt
npm install --prefix theme
python manage.py migrate
npm run dev --prefix theme
```

## Common Commands
- `runserver` – Local dev server
- `createsuperuser` – Admin login
- `makemigrations` + `migrate` – DB changes
- `tailwind build` – CSS compile

## Style Guide
- Use `black` for formatting
- Keep views clean, use helpers for logic
- Create templates per app in `templates/<app>/`

## Testing (later)
- Use `pytest-django`
- Seed data fixtures for development
    