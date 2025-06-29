
# User Authentication and Roles

## Roles
- **patient**: Default role, sees their data only
- **doctor**: Can view assigned patients' data
- **caregiver**: Read-only access with consent
- **admin**: Full access to system and users

## Custom User Model
```python
class User(AbstractUser):
    role = models.CharField(choices=ROLE_CHOICES, default='patient')
```

## Access Control
Use `@user_passes_test` or role-checking middleware:
```python
@user_passes_test(lambda u: u.role == 'doctor')
```

## Object-Level Permissions
Ensure views like:
```python
HealthRecord.objects.filter(user=request.user)
```

Restrict data access by user ID or linked relationship.
    