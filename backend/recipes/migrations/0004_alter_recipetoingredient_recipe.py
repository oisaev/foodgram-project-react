# Generated by Django 3.2.19 on 2023-06-10 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230610_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipetoingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_to_ingredient', to='recipes.recipe', verbose_name='ссылка на рецепт'),
        ),
    ]
