
# 🩺 MamboHealth – Personal Health Management Platform

MamboHealth is a modular, AI-augmented personal health management platform built using Django, Wagtail, and Tailwind CSS. It is designed to help individuals track, understand, and optimize their health through structured data, visual timelines, and AI-assisted insights.

This README describes the project as of **Phase 0**, focused on setting up the core platform architecture and documentation.

---

## 🚀 Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Web Backend | Django + Wagtail   |
| UI Framework| Tailwind CSS       |
| Database    | PostgreSQL         |
| Hosting     | Redcode.cloud      |
| CI/CD       | GitHub + Actions   |

---

## 🧱 Phase 0 Scope

Phase 0 lays the foundation for the platform. Deliverables include:

- Project scaffold with modular app structure
- Custom user model with roles (patient, doctor, caregiver, admin)
- Central timeline model (`TimelineEvent`)
- Wagtail Snippets for health data configuration
- Tailwind-based responsive UI framework
- Initial CI/CD setup with GitHub Actions
- Internal documentation

---

## 🗂 Project Structure

```
mambohealth/
├── core/            # Timeline, user model, shared utilities
├── health_data/     # Lab results app (Phase 1+)
├── nutrition/       # Food log and nutrition tracking
├── coaching/        # Goal tracking, AI advice (future)
├── docs/            # Internal markdown documentation
├── templates/       # Jinja2/HTML templates
├── theme/           # Tailwind CSS with npm
├── static/          # Static assets
├── media/           # Uploaded files
├── manage.py        # Django CLI entry point
```

---

## 🧑‍⚕️ Roles & Permissions

- `patient`: Default user, sees own data
- `doctor`: Can view assigned patient data
- `caregiver`: Read-only viewer with consent
- `admin`: Full system access

Role enforcement is implemented via Django decorators and object-level queryset filtering.

---

## 🛠 Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Node.js + npm

### Install

```bash
git clone https://github.com/youruser/mambohealth.git
cd mambohealth
pip install -r requirements.txt
npm install --prefix theme
python manage.py migrate
npm run dev --prefix theme
```

---

## 🧪 Core Models

### `User`

Custom Django user model with role-based access control.

### `TimelineEvent`

Generic model linking any health event (test, meal, goal) to a unified timeline.

### Wagtail Snippets

- `HealthRangeSnippet`: Reference ranges by metric, gender, age
- `ConditionTagSnippet`: Labels for clustering health data

---

## 🚚 Deployment

The platform is hosted on [Redcode.cloud](https://redcode.cloud) using:

- PostgreSQL database
- Static/media file handling (local for now)
- GitHub Actions for CI/CD deployment

---

## 📑 Documentation

See the `/docs/` folder for detailed internal documentation:

- `architecture.md`
- `project_structure.md`
- `model_design.md`
- `auth_roles.md`
- `deployment.md`
- `development_guide.md`
- `future_modules.md`

---

## 🧭 Next Steps

- Phase 1: Implement Health Exam Logging + Timeline UI
- Phase 2: Introduce AI Insights + Nutrition Logging
- Phase 3+: Add Sleep, Mental Health, Medication, etc.

---

## 👨‍🔬 License

This project is currently closed source (pre-release phase). Licensing terms will be defined in a future phase.

---
