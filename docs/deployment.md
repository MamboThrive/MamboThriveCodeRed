
# Deployment – Redcode.cloud

## PostgreSQL Setup
- Get connection URL from Redcode dashboard
- Configure `DATABASES` in `settings.py`

## Static & Media
- `collectstatic` for static files
- `media/` is local; future S3 integration optional

## GitHub Actions
```yaml
# .github/workflows/deploy.yml
on: push
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: ssh user@redcode 'cd app && git pull && ./deploy.sh'
```

## Environment Variables
Use `.env` locally and `os.environ` for Redcode deployment.
    