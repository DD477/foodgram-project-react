from dataclasses import field
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт'
    )

    class Meta:
        db_table = 'shopping_carts'
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
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        db_table = 'favorites'
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite')
        ]

    def __str__(self):
        return f'пользователь {self.user} | рецепт {self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Автор'
    )

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='user_not_author')
        ]

    def __str__(self):
        return f'Подписчик {self.user.username} | Автор {self.author.username}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        "Tag",
        related_name='recipes',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Текст рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),
            MaxValueValidator(
                (60 * 24), 'Слишком долго'
            )
        ),
        verbose_name='Время приготовления'
    )

    class Meta:
        db_table = 'recipes'
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
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единца измерения',
        max_length=200
    )

    class Meta:
        db_table = 'ingredients'
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
        verbose_name='Рецепта'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='amountingredientforrecipe',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),
            MaxValueValidator(
                1000, 'Слишком много!'
            ),
        ),
        verbose_name='Количество ингредиента'
    )

    class Meta:
        db_table = 'amount_ingredient_for_recipe'
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
        verbose_name='Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        unique=True
    )
    slug = models.CharField(
        verbose_name='Уникальный слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        db_table = 'tags'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['id']

    def __str__(self):
        return self.name
