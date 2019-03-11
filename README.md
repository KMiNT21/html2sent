This library works with HTML-content and modifies it in some tags to improve sentences tokenizer quality.
It is better to combine with library that remove or unwrap abbreviations with period at the end (not a part of this lib).

Instalation:

## Install NLTK python package:
```
pip install nltk
```

## Download punkt data:

import nltk
nltk.download('punkt')

For Russian language also download ru_punkt:

git clone https://github.com/mhq/train_punkt.git
(fork: https://github.com/KMiNT21/train_punkt.git )

Copy russian.pickle into nltk_data folder (ensure the appropriate location for your OS).

## Download this library:
git clone https://github.com/KMiNT21/html2sent.git


## Use it as simple:
```python
import html2sent
sentences = html2sent.tokenize(html, language='english')
```

Demo: `demo_simple.py` and `demo_folder_multiprocessing.py`