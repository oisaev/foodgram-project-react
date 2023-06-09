# Generated by Django 3.2.19 on 2023-06-07 14:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранный рецепт',
                'verbose_name_plural': 'избранные рецепты',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название ингредиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='единица измерения ингредиента')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='название рецепта')),
                ('image', models.ImageField(upload_to='images/', verbose_name='фотография блюда')),
                ('text', models.TextField(verbose_name='описание рецепта')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления должно быть не менее 1 минуты')], verbose_name='время приготовления (в минутах)')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='дата и время публикации')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='RecipeToIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1')], verbose_name='количество ингредиента в рецепте')),
            ],
            options={
                'verbose_name': 'связь рецепта и ингредиентов',
                'verbose_name_plural': 'связи рецепта и ингредиентов',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='название тега')),
                ('color', models.CharField(max_length=7, unique=True, verbose_name='цвет тега')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug тега')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.recipe', verbose_name='рецепт для покупки')),
            ],
            options={
                'verbose_name': 'рецепт для покупок',
                'verbose_name_plural': 'рецепты для покупок',
            },
        ),
    ]
