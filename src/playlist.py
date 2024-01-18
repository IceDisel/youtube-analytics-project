from datetime import timedelta
import isodate

from src.video import Video


class PlayList(Video):
    """
    Класс Плейлист ютуб канала.
    """
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        youtube = self.get_service()

        playlist_response = youtube.playlists().list(part="snippet", id=self.__playlist_id).execute()
        playlist_videos = youtube.playlistItems().list(part='contentDetails', playlistId=self.__playlist_id,
                                                       maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.__video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)
                                                      ).execute()

        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        """
        total_duration = timedelta()
        for video in self.__video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration = total_duration + duration

        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        like, id_video = 0, ""
        for video in self.__video_response['items']:
            likes_int = int(video['statistics']['likeCount'])
            if like < likes_int:
                like = likes_int
                id_video = video['id']

        return f"https://youtu.be/{id_video}"
