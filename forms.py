from django.forms import Form
from django import forms


class AnalyserForm(Form):
    """
    TODO: Берем текст из файла или вставляем в поле
    FIXME: Не отправлять форму с пустыми частями речи
    """
    source_file_path = forms.FileField(label="путь к файлу с текстом:")
    destination_file_path = forms.FileField(label="путь к готовой картинке:")
    parts_of_speech = [
        ("NOUN", "существительные"),
        ("ADJF", "прилагательные (полные)"),
        ("ADJS", "прилагательные (краткие)"),
        ("VERB", "глаголы (личная форма)"),
        ("INFN", "глаголы (инфинитив)")
    ]
    part_of_speech = forms.MultipleChoiceField(
        label="части речи:",
        choices=parts_of_speech,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    words_number = forms.IntegerField(label="Количество слов", max_value=100, min_value=1)
    wordcloud_width = forms.IntegerField(label="Ширина картинки", max_value=1920, min_value=1)
    wordcloud_height = forms.IntegerField(label="Высота картинки", max_value=1080, min_value=1)
