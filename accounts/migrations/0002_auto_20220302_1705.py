from django.db import migrations, models


class Migration(migrations.Migration):

    # Define dependencies for this migration, ensuring it's applied after the initial UserProfile migration.
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    # Operations to be carried out in this migration.
    operations = [
        # Add a new field 'mobile' to the UserProfile model.
        migrations.AddField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(
                max_length=100,  # Maximum length for the mobile number
                blank=True,      # Allow the field to be blank
                null=True,       # Allow the field to be null in the database
                default='0',     # Default value is '0'
                verbose_name='手机'  # Human-readable name for the field in the admin interface
            ),
        ),
        # Alter the existing 'email' field in the UserProfile model.
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(
                max_length=100,  # Maximum length for the email address
                blank=True,      # Allow the field to be blank
                null=True,       # Allow the field to be null in the database
                default='0',     # Default value is '0'
                verbose_name='邮箱'  # Human-readable name for the field in the admin interface
            ),
        ),
    ]
