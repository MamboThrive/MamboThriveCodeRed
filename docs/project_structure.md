
# Project Structure

## Top-Level Layout
```
/mambohealth/
├── manage.py
├── mambohealth/           # Django project config and settings
├── core/                  # Shared models (users, timeline)
├── health_data/           # Health test result logging
├── nutrition/             # Meal and food log
├── coaching/              # Goal setting and AI advice (future)
├── templates/             # Shared HTML templates
├── theme/                 # Tailwind CSS setup and assets
├── static/                # Compiled CSS/JS
├── media/                 # User-uploaded files
├── docs/                  # Documentation folder
```

## Development Tools
- `theme/` uses Tailwind with npm (`npm run dev`)
- `templates/` organized by app
- Wagtail admin handles snippet and structured content
    