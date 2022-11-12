from django.shortcuts import render
from .analyser import Analyser
from . import forms


def index(request):
    """
    FIXME: поля AnalyserForm source_file_path, dest_file_path, не проходят валидацию
    FIXME: поле AnalyserForm wordcloud_background_color не джанговое, не проходит валидацию тоже
    """
    if request.method == "POST":
        form = forms.AnalyserForm(request.POST)
        if form.is_valid():
            analyser = Analyser(
                source_file_path=r"C:\Users\Me\Desktop\django_develop\my_project\text_analyser\static\text_analyser\text\text.fb2",
                dest_file_path=r"C:\Users\Me\Desktop\django_develop\my_project\text_analyser\static\text_analyser\img\wordcloud.jpg",
                parts_of_speech=form.cleaned_data["part_of_speech"],
                words_number=form.cleaned_data["words_number"],
                wordcloud_width=form.cleaned_data["wordcloud_width"],
                wordcloud_height=form.cleaned_data["wordcloud_height"],
                wordcloud_background_color="black",
            )
            return render(request, "text_analyser/result.html", {"path_to_image": analyser.dest_file_path})
        else:
            return render(request, "text_analyser/index.html", {"form": form})
    else:
        form = forms.AnalyserForm()
        return render(request, "text_analyser/index.html", {"form": form})
