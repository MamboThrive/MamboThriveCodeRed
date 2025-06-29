
# Model Design

## User
Custom user model using `AbstractUser` with a `role` field:
- `patient`, `doctor`, `caregiver`, `admin`

## TimelineEvent
A central model for the unified health timeline:
```python
class TimelineEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    event_type = models.CharField(choices=EVENT_TYPE_CHOICES)
    summary = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    related_object = GenericForeignKey("content_type", "object_id")
```

## Snippets
- `HealthRangeSnippet`: Stores health value reference ranges
- `ConditionTagSnippet`: Tags like metabolic, cardiac, renal, etc.

## Future Models
- `HealthRecord`, `MealLog`, `SleepLog`, `Goal`, etc., will integrate with `TimelineEvent`
    