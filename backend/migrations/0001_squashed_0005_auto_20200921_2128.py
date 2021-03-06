# Generated by Django 3.1.1 on 2020-09-22 01:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [
        ("backend", "0001_initial"),
        ("backend", "0002_auto_20200920_0111"),
        ("backend", "0003_auto_20200920_2334"),
        ("backend", "0004_auto_20200921_2114"),
        ("backend", "0005_auto_20200921_2128"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Business",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slogan", models.CharField(blank=True, max_length=150)),
                ("description", models.CharField(blank=True, max_length=300)),
                ("website", models.URLField(blank=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("notes", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("refused", "Refused"),
                        ],
                        default="pending",
                        max_length=25,
                    ),
                ),
                ("accepted_at", models.DateField(null=True)),
            ],
            options={"verbose_name_plural": "businesses"},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={"verbose_name_plural": "categories"},
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={"verbose_name_plural": "tags"},
        ),
        migrations.CreateModel(
            name="SocialLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                ("link", models.URLField()),
                (
                    "business",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_links",
                        to="backend.business",
                    ),
                ),
            ],
            options={"verbose_name_plural": "social links"},
        ),
        migrations.CreateModel(
            name="Phone",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "number",
                    models.CharField(
                        max_length=200,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Format: '+1-514-111-1111,514-111-1111,+1 514 111 1111,514-111-1111,514 111 1111,111-1111,111 1111'",
                                regex="(\\+\\d{1})?((\\-|\\s)\\d{3})?((\\-|\\s)\\d{3})((\\-|\\s)\\d{4})$",
                            )
                        ],
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("tel", "Telephone"), ("fax", "Fax")],
                        max_length=25,
                    ),
                ),
                ("extension", models.IntegerField(blank=True, null=True)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phones",
                        to="backend.business",
                    ),
                ),
            ],
            options={"verbose_name_plural": "phones"},
        ),
        migrations.AddField(
            model_name="business",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="backend.category",
            ),
        ),
        migrations.AddField(
            model_name="business",
            name="tags",
            field=models.ManyToManyField(blank=True, to="backend.Tag"),
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "app_office_number",
                    models.CharField(
                        blank=True,
                        help_text="App/Office number",
                        max_length=10,
                    ),
                ),
                ("street_number", models.SmallIntegerField()),
                ("street_type", models.CharField(blank=True, max_length=30)),
                ("street_name", models.CharField(max_length=200)),
                ("direction", models.CharField(blank=True, max_length=10)),
                ("city", models.CharField(default="Montreal", max_length=200)),
                (
                    "province",
                    models.CharField(
                        choices=[
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
                        ],
                        default="qc",
                        max_length=100,
                    ),
                ),
                ("postal_code", models.CharField(max_length=200)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to="backend.business",
                    ),
                ),
            ],
            options={"verbose_name_plural": "addresses"},
        ),
        migrations.CreateModel(
            name="PaymentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("credit", "Credit"),
                            ("debit", "Debit"),
                            ("cash", "Cash"),
                            ("crypto", "Crypto"),
                        ],
                        max_length=100,
                        unique=True,
                    ),
                ),
            ],
            options={"verbose_name_plural": "payment types"},
        ),
        migrations.AddField(
            model_name="business",
            name="payment_types",
            field=models.ManyToManyField(blank=True, to="backend.PaymentType"),
        ),
        migrations.AlterField(
            model_name="business",
            name="description",
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.CreateModel(
            name="OpeningHour",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last modification"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "day",
                    models.IntegerField(
                        choices=[
                            (1, "Monday"),
                            (2, "Tuesday"),
                            (3, "Wednesday"),
                            (4, "Thursday"),
                            (5, "Friday"),
                            (6, "Saturday"),
                            (7, "Sunday"),
                        ]
                    ),
                ),
                ("opening_time", models.TimeField(max_length=100)),
                ("closing_time", models.TimeField()),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opening_hours",
                        to="backend.business",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "opening hours",
                "ordering": ("day", "opening_time"),
                "unique_together": set(),
            },
        ),
    ]
