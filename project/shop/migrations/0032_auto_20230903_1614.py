# Generated by Django 2.2 on 2023-09-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20230902_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtered',
            name='display_size',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filtered',
            name='generation',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='filtered',
            name='ram',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filtered',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='filtereditti',
            name='display_size',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='filtereditti',
            name='generation',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='filtereditti',
            name='ram',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filtereditti',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='display',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='display_size',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='graphics_info',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='graphics_type',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='ram',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='sstorage',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='filteredneo',
            name='storage_type',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='display',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='generation',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='maximum_display_resulation',
            field=models.CharField(blank=True, default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productitti',
            name='display',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productitti',
            name='generation',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productitti',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productneo',
            name='display',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productneo',
            name='generation',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productneo',
            name='storage',
            field=models.CharField(default='-', max_length=200),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='battery',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='camera_features',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='charger',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='color',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='cpu',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='date',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='density',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='dimensions',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='display',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='expandablememory',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='extra_sensor',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='front_camera',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='front_camera_extra',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='gpu',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='memorycardslot',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='model',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='nfc',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='operatingsystem',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='processor',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='protection',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='ram',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='rear_camera',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='rear_camera_extra',
            field=models.CharField(default=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='resolution',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='sensors',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='sim_type',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='sound',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='storage',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='technology',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='touchscreen',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='type',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='usb',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='video',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='warranty',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='weight',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphonedeal',
            name='wlan',
            field=models.CharField(default=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='battery_power',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='brand',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='chipset',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='display_size',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='insurance',
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='operating_system',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='primary_camera',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='ram',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='secondary_camera',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='sim_type',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productphoneneo',
            name='warranty',
            field=models.CharField(max_length=200),
        ),
    ]
