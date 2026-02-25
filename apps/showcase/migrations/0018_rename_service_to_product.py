from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0017_aboutmetric_is_deleted_aboutsection_is_deleted_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServiceSection',
            new_name='ProductSection',
        ),
        migrations.RenameModel(
            old_name='Service',
            new_name='Product',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='ur',
            new_name='url',
        ),
    ]
