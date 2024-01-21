import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """
    Класс Видео ютуб канала.
    """

    def __init__(self, video_id):
        self.__video_id = video_id
        try:
            youtube = self.get_service()
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.__video_id
                                                   ).execute()
            self.title: str = video_response['items'][0]['snippet']['title']
            self.video_url = "https://www.youtube.com/watch?v=" + self.__video_id
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title, self.video_url, self.view_count, self.like_count = (None,) * 4

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
        return os.getenv('API_KEY_YOUTUBE')

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс Плейлист ютуб канала.
    """

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id
        youtube = self.get_service()
        self.playlist_response = youtube.playlists().list(part="snippet", id=self.__playlist_id).execute()
