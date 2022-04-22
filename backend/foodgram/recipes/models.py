from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'cписок покупок'
        verbose_name_plural = 'cписки покупок'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_cart')
        ]

    def __str__(self):
        return f'пользователь {self.user} | рецепт {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite')
        ]

    def __str__(self):
        return f'пользователь {self.user} | рецепт {self.recipe}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        "Tag",
        related_name='recipes',
        verbose_name='тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    name = models.CharField(
        verbose_name='название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='картинка рецепта',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        verbose_name='текст рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),
            MaxValueValidator(
                (60 * 24), 'Слишком долго'
            )
        ),
        verbose_name='время приготовления'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'], name='unique_recipe'),
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='единца измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


class AmountIngredientForRecipe(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='amountingredientforrecipe',
        verbose_name='рецепта'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='amountingredientforrecipe',
        verbose_name='ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),
            MaxValueValidator(
                1000, 'Слишком много!'
            ),
        ),
        verbose_name='количество ингредиента'
    )

    class Meta:
        verbose_name = 'количество ингредиента для рецепта'
        verbose_name_plural = 'количество ингредиента для рецепта'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='цветовой HEX-код',
        max_length=7,
        unique=True
    )
    slug = models.CharField(
        verbose_name='уникальный слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['id']

    def __str__(self):
        return self.name
