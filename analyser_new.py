import re  # разбирем строку на отдельные слова
from collections import Counter  # считаем самые частые слова
from docx import Document  # pip install python-docx
from bs4 import BeautifulSoup  # прасинг xml
import pymorphy2  # нормализация частей речи
from wordcloud import WordCloud  # pip install wordcloud
from charset_normalizer import from_path  # нормализуем кодировку


class Analyser:
    """
    Делает из текстового файла картинку - облако слов
    """
    def __init__(
        self,
        source_file_path=None,
        dest_file_path=None,
        parts_of_speech=None,
        words_number=None,
        wordcloud_width=None,
        wordcloud_height=None,
        wordcloud_background_color=None
    ):
        self.source_file_path = source_file_path
        if not self.source_file_path:
            raise ValueError(
                "Невозможно найти файл источника! Проверьте путь к файлу с текстом!"
            )

        self.dest_file_path = dest_file_path
        if not self.dest_file_path:
            raise ValueError(
                "Невозможно найти файл назначения! Проверьте путь к файлу с картинкой!"
            )

        self.parts_of_speech = parts_of_speech 
        if not self.parts_of_speech:
            raise ValueError(
                "Не выбраны части речи! Анализ текста невозможен!"
            )

        self.words_number = words_number
        if not self.words_number:
            raise ValueError(
                "Не указано количество слов на изображении облака слов!"
            )

        self.wordcloud_width = wordcloud_width
        if not self.wordcloud_width:
            raise ValueError(
                "Не указана ширина изображении облака слов!"
            )

        self.wordcloud_height = wordcloud_height
        if not self.wordcloud_height:
            raise ValueError(
                "Не указана высота изображении облака слов!"
            )

        self.wordcloud_background_color = wordcloud_background_color
        if not self.wordcloud_background_color:
            raise ValueError(
                "Не указан цвет фона изображении облака слов!"
            )

        self.content = self.make_text_from_file()
        self.words = self.make_words_from_text()
        self.normalized_words = self.make_normalized_words()
        self.most_frequent_words = self.make_most_frequent_words()
        self.wordcloud = self.make_wordcloud()
        self.save_wordcloud_to_file()

    def make_text_from_file(self) -> str:
        """
        Определяет расширение текстового файла источника
        Вызывает соответствуйющий метод для типов TXT, DOCX, FB2
        Возвращает контент файла строкой
        """
        content = ""
        if self.source_file_path.endswith(".txt"):
            content = self.make_text_from_txt()
        elif self.source_file_path.endswith(".docx"):
            content = self.make_text_from_docx()
        elif self.source_file_path.endswith(".fb2"):
            content = self.make_text_from_fb2()
        else:
            raise ValueError("Неверный тип файла! Только TXT, DOCX и FB2!")

        if not content:
            raise ValueError(
                "Не удалось получить текст из файла! Возможно, файл пустой."
            )
        return content

    def make_text_from_txt(self) -> str:
        """
        Возвращает текст из TXT файла
        """
        text = str(from_path(self.source_file_path).best())
        if not text:
            raise ValueError(
                "Не удалось прочитать содержимое файла TXT как текст!"
            )
        return text

    def make_text_from_docx(self) -> str:
        """
        Возвращает текст из DOCX файла
        """
        file = Document(self.source_file_path)
        text = " ".join([p.text for p in file.paragraphs])
        if not text:
            raise ValueError(
                "Не удалось прочитать содержимое файла DOCX как текст!"
            )
        return text

    def make_text_from_fb2(self) -> str:
        """
        Возвращает текст из FB2 файла
        """
        with open(self.source_file_path, 'rb') as file:
            data = file.read()
        bs_data = BeautifulSoup(data, "xml")
        sections = bs_data.find_all('section')
        text = " ".join([s.text for s in sections])
        if not text:
            raise ValueError(
                "Не удалось прочитать содержимое файла FB2 как текст!"
            )
        return text

    def make_words_from_text(self) -> list:
        """
        Возвращает список русских слов со строчной буквы без знаков препинания
        """
        words = re.findall("[а-яё]+", self.content.lower())
        if not words:
            raise ValueError(
                "Не удалось распознать отдельные русские слова в тексте!"
            )
        return words
        
    def make_normalized_words(self) -> list:
        """
        Возвращает список нормальных форм слов
        для определенных в part_of_speech частей речи.
        https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html#grammeme-docs
        """
        morph = pymorphy2.MorphAnalyzer()
        normalized_words = []
        for word in self.words:
            parse = morph.parse(word)[0]
            for part in self.parts_of_speech:
                if part in parse.tag:
                    normalized_words.append(parse.normal_form)

        if not normalized_words:
            raise ValueError(
                "Не удалось получить нормальныю форму слов в тексте!"
            )
        return normalized_words

    def make_most_frequent_words(self) -> dict:
        """
        Возвращает словарь длинной num из самых частых слов по убыванию частоты
        слово: частота
        """
        most_frequent_words = dict(Counter(
            self.normalized_words).most_common(self.words_number))
        if not most_frequent_words:
            raise ValueError(
                "Не удалось посчитать частоту слов в нормальной форме в тексте!"
            )
        return most_frequent_words

    def make_wordcloud(self) -> WordCloud:
        """
        Возвращает объект Wordcloud
        width - ширина в пикселях
        height  - высота в пикселях
        background_color - цвет фона словом
        TODO: Какая модель цвета, можно ли hex?
        """
        wordcloud = WordCloud(
            width=self.wordcloud_width,
            height=self.wordcloud_height,
            background_color=self.wordcloud_background_color
        )
        
        if not wordcloud:
            raise ValueError(
                "Не удалось сгенерировать изображение облака слов!"
            )
        return wordcloud.generate_from_frequencies(
            self.most_frequent_words
        )

    def save_wordcloud_to_file(self):
        """
        сохраняет Wordcloud в файл filename
        """
        try:
            self.wordcloud.to_file(self.dest_file_path)
        except:
            raise ValueError(
                "Не удалось сохранить изображение облака слов в файл!"
            )
