
This library works with **HTML-content** and modifies it in some tags to improve sentences tokenizer quality.


# 
## Install NLTK python package
``` pip install nltk```


## Download punkt data

```python
import nltk
nltk.download('punkt')
```

## Download this library
git clone https://github.com/KMiNT21/html2sent.git


## Using
```python
import html2sent
sentences = html2sent.tokenize(html, language='english')
```

Demo: `demo_simple.py` and `demo_folder_multiprocessing.py`


## For russian language

Если для разделения полученного текста на предложения используется библиотека **nltk**,
то для русского языка нужно еще скачать обученный ru_punkt-токенизатор. 

Варианты:

- git clone https://github.com/mhq/train_punkt.git

- git clone https://github.com/Mottl/ru_punkt.git

Скопируйте файл russian.pickle в папку nltk_data (к остальным языковым .pickle файлам)

Альтернативный более точный вариант - библиотека **razdel**

Подробнее об использовании - https://github.com/natasha/razdel
