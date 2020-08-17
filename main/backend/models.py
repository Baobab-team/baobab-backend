from django.core.validators import RegexValidator
from django.db import models


class BaseModel(models.Model):
    id = models.AutoField()


class Category(BaseModel):
    name = models.CharField(max_length=100)


class Tag(BaseModel):
    name = models.CharField(max_length=100)


class Business(BaseModel):
    STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    website = models.URLField()
    email = models.EmailField()
    notes = models.CharField(max_length=300)
    status = models.CharField(max_length=150, choices=STATUS)
    accepted_at = models.DateField()
    tags = models.ManyToManyField(Tag)


class Phone(BaseModel):
    PHONE_TYPES = [
        ('tel', 'Telephone'),
        ('fax', 'Fax'),
    ]
    phone_regex = RegexValidator(regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-](\d{3})[\s.-](\d{4})$',
                                 message="Format: '222 333 5555','222-333-5555','+1 222-333-5555'")  # TODO add Missing extension
    telephone = models.CharField(max_length=200, validators=[phone_regex], blank=True)
    type = models.CharField(choices=PHONE_TYPES)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, )


class SocialLink(BaseModel):
    TYPES = [
        "linkedin",
        "facebook",
    ]
    link = models.URLField()

    @property
    def type(self):
        link = getattr(self, "link")
        if link.lower() in (name.lower() for name in self.TYPES):
            return link.lower()
        return "unknown"


class OpeningHours(BaseModel):
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    day = models.IntegerField(choices=WEEKDAYS)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    business = models.ForeignKey(Business, on_delete=models.CASCADE, )

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return f"{getattr(self, 'day')} :{self.opening_time}  {self.closing_time}"
