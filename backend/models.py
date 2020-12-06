import logging
from datetime import date

from autoslug import AutoSlugField
from autoslug.utils import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from users.models import CustomUser

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last modification")
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
    MAX_LEVEL = 3

    class Meta:
        verbose_name_plural = "categories"

    slug = models.SlugField()
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        full_path = self.get_tree()
        return ">".join(full_path[::-1])

    def get_tree(self):
        tree = [self.name]
        k = self.parent
        while k is not None:
            tree.append(k.name)
            k = k.parent
        return tree

    def get_children_ids(self):
        ids = [self.id]
        children = self.children.all()
        for c in children:
            if c.children:
                ids = ids + c.get_children_ids()
            else:
                ids.append(c.id)
        return ids

    def clean(self):
        if len(self.get_tree()) > self.MAX_LEVEL:
            raise ValidationError(
                {
                    "parent": _(
                        f"There can only be {self.MAX_LEVEL} levels of categories"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(BaseModel):
    class Meta:
        verbose_name_plural = "tags"

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PaymentType(BaseModel):
    TYPES = [
        ("credit", _("Credit")),
        ("debit", _("Debit")),
        ("cash", _("Cash")),
        ("crypto", _("Crypto")),
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
        ("pending", _("Pending")),
        ("accepted", _("Accepted")),
        ("refused", _("Refused")),
    ]
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField()
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
    last_updated_by = models.ForeignKey(
        CustomUser, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def update_status(self, new_status):
        self.status = new_status

    def clean(self):
        if self.status == "accepted":
            self.accepted_at = date.today()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Business, self).save(*args, **kwargs)


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
        ("tel", _("Telephone")),
        ("fax", _("Fax")),
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
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
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
        ("qc", _("Quebec")),
        ("on", _("Ontario")),
        ("ns", _("Nova Scotia")),
        ("nb", _("New Brunswick")),
        ("pe", _("Prince Edward Island")),
        ("ab", _("Alberta")),
        ("nu", _("Nunavut")),
        ("sk", _("Saskatchewan")),
        ("bc", _("British Columbia")),
        ("nl", _("Newfoundland and Labrador")),
        ("mn", _("Manitoba")),
    ]
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="addresses"
    )
    app_office_number = models.CharField(
        blank=True, help_text=_("App/Office number"), max_length=10
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
