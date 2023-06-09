# Generated by Django 3.2.19 on 2023-06-10 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipetoingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_to_ingredient', to='recipes.ingredient', verbose_name='ссылка на ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipetoingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='ссылка на рецепт'),
        ),
        migrations.AddConstraint(
            model_name='recipetoingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
    ]
