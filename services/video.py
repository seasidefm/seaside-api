TEMP_MOVIE_DETAILS = """
Title: Maison Ikkoku |
Synopsis: Maison Ikkoku is a bitter-sweet romantic comedy involving a group of
madcap people who live in a boarding house in 1980s Tokyo. The story focuses
primarily on the gradually developing relationships between Yusaku Godai, a poor
student down on his luck, and Kyoko Otonashi, a young, recently widowed boarding
house manager.
"""


class VideoInfoService:
    def __init__(self):
        self.movie_details = TEMP_MOVIE_DETAILS

    def get_movie_details(self) -> str:
        return self.movie_details
