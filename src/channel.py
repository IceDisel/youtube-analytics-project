import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        youtube = Channel.get_service()
        self.youtube_channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.youtube_channel['items'][0]['snippet']['title']
        self.description = self.youtube_channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.youtube_channel['items'][0]['id']}"
        self.subscriber_count = self.youtube_channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.youtube_channel['items'][0]['statistics']['videoCount']
        self.view_count = self.youtube_channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Создаем объект youtube с использованием учетных данных API
        """
        youtube = build('youtube', 'v3', developerKey=cls.load_api_key())
        return youtube

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

    def to_json(self, filename: str):
        """
        Запись в файл информации о канале
        """
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.youtube_channel, file, indent=2, ensure_ascii=False)
