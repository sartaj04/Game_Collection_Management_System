
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db import models

from django.conf import settings


def string_to_set(s: str) -> set:
    return set(item.strip() for item in s.split(",") if item.strip())


class Club(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class BoardGame(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    year = models.IntegerField()
    designers = models.TextField()
    solo_designers = models.TextField(blank=True)
    artists = models.TextField()
    publishers = models.TextField()
    versions = models.TextField()
    categories = models.TextField()
    mechanisms = models.TextField()
    users_rated = models.IntegerField()
    rating = models.FloatField()
    complexity = models.FloatField()
    game_id = models.IntegerField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    min_play_time = models.IntegerField()
    max_play_time = models.IntegerField()
    image_url = models.URLField()
    components = models.TextField()
    description = models.TextField()
    commerce_links = models.TextField()

    @staticmethod
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0



    def get_similarity(self, other_game):
        category_set1 = string_to_set(self.categories)
        category_set2 = string_to_set(other_game.categories)
        category_similarity = self.jaccard_similarity(category_set1, category_set2)

        mechanism_set1 = string_to_set(self.mechanisms)
        mechanism_set2 = string_to_set(other_game.mechanisms)
        mechanics_similarity = self.jaccard_similarity(mechanism_set1, mechanism_set2)

        rating_similarity = 1 - abs(self.rating - other_game.rating) / 10
        combined_similarity = (category_similarity + mechanics_similarity + rating_similarity) / 3

        return combined_similarity

    def get_recommendations(self, library, wishlist, num_recommendations=10):
        library_pks = [game.pk for game in library]
        wishlist_pks = [game.pk for game in wishlist]
        all_games = BoardGame.objects.exclude(pk__in=library_pks).exclude(pk__in=wishlist_pks)
        similarity_scores = [(game, self.get_similarity(game)) for game in all_games]
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        return [game_score[0] for game_score in similarity_scores[:num_recommendations]]


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    clubs = models.ManyToManyField(Club)
    wishlist = models.ManyToManyField(BoardGame, related_name='wishlisted_by', blank=True)
    library = models.ManyToManyField(BoardGame, related_name='library_users', blank=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

# class Wishlist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     boardgame = models.ForeignKey(BoardGame, on_delete=models.CASCADE)


class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlist_items')
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game',)

class Library(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='library_items')
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game',)


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=3)
    comment = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game',)

class CommunityMember(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game',)






