import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()
from boardgames.models import BoardGame
import os
import pandas as pd
from django.core.exceptions import ValidationError


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swd.settings')
import django
django.setup()

def import_csv_data(csv_file_path):
    data = pd.read_csv(csv_file_path)

    for index, row in data.iterrows():
        instance = BoardGame(
            rank=row['rank'],
            title=row['title'],
            short_description=row['short_description'],
            year=row['year'],
            designers=row['designers'],
            solo_designers=row['solo_designers'],
            artists=row['artists'],
            publishers=row['publishers'],
            versions=row['versions'],
            categories=row['categories'],
            mechanisms=row['mechanisms'],
            users_rated=row['users_rated'],
            rating=row['rating'],
            complexity=row['complexity'],
            game_id=row['game_id'],
            min_players=row['min_players'],
            max_players=row['max_players'],
            min_play_time=row['min_play_time'],
            max_play_time=row['max_play_time'],
            image_url=row['image_url'],
            components=row['components'],
            description=row['description'],
            commerce_links=row['commerce_links'],
        )

        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            print(f"Row {index} has errors: {e}")

if __name__ == '__main__':
    csv_file_path = 'game_details.csv'
    import_csv_data(csv_file_path)