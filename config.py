from dataclasses import dataclass

@dataclass
class ParserConfig:
    start_url: str = 'https://mangabuff.ru/manga/pererozhdenie-bessmertnogo-gorodskogo-praktika/1/35'
    scroll_time: int = 35
    after_found_time: int = 200
    comment_text: str = 'Вери биг сенкс'
    comments_ready: int = 10
    comments_need: int = 13
    mine_needed: bool = True
    comment_on: bool = True
    scroll_mode: int = 1