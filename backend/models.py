import logging
from datetime import date

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Last modification"
    )
    created_at = models.DateTimeField(auto_now=False, default=timezone.now)
    deleted_at = models.DateTimeField(null=True)

    hard_delete = True

    def delete(self, using=None, keep_parents=False):
        if self.hard_delete:
            super().delete(using, keep_parents)
        else:
            self.deleted_at = timezone.now
            self.save()


class Category(BaseModel):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    class Meta:
        verbose_name_plural = "tags"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PaymentType(BaseModel):
    TYPES = [
        ("credit", "Credit"),
        ("debit", "Debit"),
        ("cash", "Cash"),
        ("crypto", "Crypto"),
    ]

    class Meta:
        verbose_name_plural = "payment types"

    name = models.CharField(max_length=100, unique=True, choices=TYPES)

    def __str__(self):
        return self.name


class Business(BaseModel):
    class Meta:
        verbose_name_plural = "businesses"

    hard_delete = False
    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ]
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=100, unique=True)
    slogan = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=25, choices=STATUS, default=STATUS[0][0]
    )
    accepted_at = models.DateField(null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    payment_types = models.ManyToManyField(PaymentType, blank=True)

    def __str__(self):
        return self.name

    def update_status(self, new_status):
        self.status = new_status

    def clean(self):
        if self.status == "accepted":
            self.accepted_at = date.today()


phone_exemples = [
    "+1-514-111-1111",
    "514-111-1111",
    "+1 514 111 1111",
    "514-111-1111",
    "514 111 1111",
    "111-1111",
    "111 1111",
]


class Phone(BaseModel):
    class Meta:
        verbose_name_plural = "phones"

    PHONE_TYPES = [
        ("tel", "Telephone"),
        ("fax", "Fax"),
    ]
    phone_regex = RegexValidator(
        regex=r"(\+\d{1})?((\-|\s)\d{3})?((\-|\s)\d{3})((\-|\s)\d{4})$",
        message="Format: '{}'".format(",".join(phone_exemples)),
    )  # TODO add Missing extension
    number = models.CharField(max_length=200, validators=[phone_regex],)
    type = models.CharField(choices=PHONE_TYPES, max_length=25)
    extension = models.IntegerField(blank=True, null=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="phones"
    )

    def __str__(self):
        return self.number


class SocialLink(BaseModel):
    class Meta:
        verbose_name_plural = "social links"

    TYPES = [
        "linkedin",
        "facebook",
        "linktr",
        "twitter",
        "instagram",
        "linkedin",
        "tiktok",
        "youtube",
    ]
    link = models.URLField()
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        related_name="social_links",
    )

    @property
    def type(self):
        link = getattr(self, "link")
        for i, name in enumerate(self.TYPES):
            if name.lower() in link.lower():
                return name
        return "unknown"

    def __str__(self):
        return self.link


class OpeningHour(BaseModel):
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
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="opening_hours"
    )
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "opening_time")
        verbose_name_plural = "opening hours"

    def __str__(self):
        if self.closed:
            return f"{self.get_day_display()}: CLOSED"
        return f"{self.get_day_display()} :{self.opening_time}  {self.closing_time}"


class Address(BaseModel):
    class Meta:
        verbose_name_plural = "addresses"

    PROVINCES = [
        ("qc", "Quebec"),
        ("on", "Ontario"),
        ("ns", "Nova Scotia"),
        ("nb", "New Brunswick"),
        ("pe", "Prince Edward Island"),
        ("ab", "Alberta"),
        ("nu", "Nunavut"),
        ("sk", "Saskatchewan"),
        ("bc", "British Columbia"),
        ("nl", "Newfoundland and Labrador"),
        ("mn", "Manitoba"),
    ]
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="addresses"
    )
    app_office_number = models.CharField(
        blank=True, help_text="App/Office number", max_length=10
    )
    street_number = models.SmallIntegerField()
    street_type = models.CharField(max_length=30, blank=True)
    street_name = models.CharField(max_length=200)
    direction = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=200, default="Montreal")
    province = models.CharField(
        max_length=100, choices=PROVINCES, default=PROVINCES[0][0]
    )
    postal_code = models.CharField(max_length=200)
