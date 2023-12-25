import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=self.load_api_key())
        self.youtube_channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    @staticmethod
    def load_api_key() -> str:
        """
        Загрузка API ключей из .env
        """
        dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        return os.getenv('API_KEY_YOUTUBE')

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube_channel, indent=2, ensure_ascii=False))
