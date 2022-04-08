from django.db import models

from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='shopping_carts',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe =  models.ManyToManyField(
        "Recipe",
        related_name='shopping_carts',
        verbose_name='id рецепта',
    )

    # def get_list(self):
    #     return ", ".join(str(l) for l in self.recipe.all())
    # get_list.__name__ = 'Рецепты'

    # def __str__(self):
    #     return str(self.get_list())

    class Meta:
        ordering = ['id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='favorites',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe =  models.ManyToManyField(
        "Recipe",
        related_name='favorites',
        verbose_name='id рецепта',
    )

    # def __str__(self):
    #     return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followings'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        "Tag",
        related_name='recipes',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        CustomUser,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    # is_favorited =
    # is_in_shopping_cart =
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
    )

    image = models.ImageField(
        upload_to='posts/',
        verbose_name = 'Картинка',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        max_length=2000,
    )
    cooking_time = models.IntegerField(
        verbose_name='Время готовки'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7,
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Слаг тега',
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'