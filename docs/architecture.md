
# Architecture – MamboHealth Platform

## Overview
MamboHealth is a modular personal health management platform with an emphasis on extensibility, privacy, and AI-assisted insights. The backend uses Django and Wagtail CMS, styled with Tailwind CSS, and deployed on Redcode.cloud with PostgreSQL.

## Core Technologies
- **Wagtail**: CMS for managing health content, snippets, and structured data.
- **Django**: Backend framework handling users, security, models, and APIs.
- **Tailwind CSS**: Utility-first CSS framework for responsive UI.
- **PostgreSQL**: Primary database, hosted on Redcode.cloud.
- **GitHub**: Version control and CI/CD via GitHub Actions.
- **Redcode.cloud**: Hosting and database provider (MVP-ready).

## Modular Architecture
- Each domain (health data, nutrition, goals) is its own Django app.
- All domain apps connect to a central timeline (`TimelineEvent`) for unified health tracking.
- Wagtail Snippets allow editable health ranges, tags, and categories.

## Data Flow
1. User submits input (test result, meal, etc.)
2. Data is saved to its domain model (e.g., `HealthRecord`, `MealLog`)
3. A corresponding `TimelineEvent` is created
4. Timeline view aggregates events chronologically
    