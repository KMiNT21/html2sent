""" KMiNT21 """
import re
from typing import List

import bs4
import nltk


# HTML processing settings

PARAGRAPH_LAST_CHAR_MUST_BE_IN = '.!?'
FINALYZE_PARAGRAPH_WITH_PERIOD_IF_NOT = True
SKIP_FINALYZING_IF_ENDS_WITH_COLON = True  # i.e. speach quote (Somebody: Text)
REMOVE_TIME_TAG = True
REMOVE_LISTS_OF_LINKS = True
REMOVE_TABLES = False
REMOVE_LISTS = False

# TEXT processing settings

# if we find "Sentence1 (.|?|!) Sentence2."
REMOVE_QUOTATION_MARKS_IF_MULT_SENT_INSIDE = True

HANDLE_LOTS_OF_SPACES_AS_SENTENCES_SEPARATOR_BY_PATTERN = False

# Previous sent. 1. Text1 -> Previous sent. 1) Text1
REPLACE_PERIOD_WITH_BRACKET_IN_LIST_ELEMENTS = True

# Sentence1.Sentence2 -> Sentence1. Sentence2
FIX_MISSING_SPACE_BETWEEN_SENTENCES = True


def html2text(html: str) -> str:
    """ Change HTML to help torenizer and return text """

    # Replace <br/> with PERIOD+NEW_LINE
    html = re.sub(r'(\s*<br\s?\/\s*>)+', '. \n', html)
    html = re.sub(r'<br\s?\/?>', '. \n', html)

    html = re.sub(r'\s*(</?em>)\s*', r' \1 ', html)
    html = re.sub(r'\s*(</?strong>)\s*', r' \1 ', html)
    html = re.sub(r'\s*(</?b>)\s*', r' \1 ', html)
    html = re.sub(r'\s*(</?i>)\s*', r' \1 ', html)

    soup = bs4.BeautifulSoup(html, 'html5lib')

    if REMOVE_TABLES:
        for tag in soup('table'):
            tag.extract()

    if REMOVE_LISTS:
        for tag in soup('ul'):
            tag.extract()

    divs_to_remove = '^(script|noscript|form|style|head|nav)$'
    for tag in soup.find_all(re.compile(divs_to_remove)):
        tag.extract()

    if REMOVE_TIME_TAG:
        for tag in soup('time'):
            tag.extract()

    if REMOVE_LISTS_OF_LINKS:
        for ul in soup('ul'):
            ul_can_be_removed_flags = []
            for li in ul.find_all('li'):
                can_be_removed = False
                li_is_link = False
                a_tags_in_li = li.find_all('a')
                if len(a_tags_in_li) == 1:
                    li_is_link = True
                if li_is_link and li.get_text().strip() == \
                        a_tags_in_li[0].get_text().strip():
                    can_be_removed = True
                ul_can_be_removed_flags.append(li_is_link)
                ul_can_be_removed_flags.append(can_be_removed)
            if all(ul_can_be_removed_flags):
                ul.extract()

    # List of html-tags that we consider as BLOCK,
    # so there are no sentences that begins in one and ends in another
    pattern = re.compile('^(div|p|h1|h2|h3|h4|h5|code|blockquote)$')

    for tag in soup.find_all(pattern):

        if tag.name == 'div' and tag.find_all(pattern):  # skip if has child
            continue

        tag_text = tag.get_text().strip()
        if not tag_text:
            continue

        if tag_text[-1] == ':' and SKIP_FINALYZING_IF_ENDS_WITH_COLON:
            continue

        # Adding PERIOD in the end of text tag
        if not tag_text[-1] in PARAGRAPH_LAST_CHAR_MUST_BE_IN:
            # remove COLON in the end
            new_tag = soup.new_tag('p')
            if tag_text[-1] == ':':
                tag_text = tag_text.rstrip(':')
            new_tag.string = '. \n' + tag_text + '. '
            tag.replace_with(new_tag)

    text = soup.get_text()

    # Remove possible period (side-effect) at the start
    text = re.sub(r'^\s*\.', r'', text)
    # Text..SPACE -> Text.SPACE
    text = re.sub(r'([^\.])\.\. ', r'\1. ', text)
    # Remove redundant punkt . \n . -> .  TODO: optimize here
    text = re.sub(r'\.(\s*\n\s*\.)+', r'. \n', text)
    text = re.sub(r'\.\s*\n\.', r'. \n', text)
    text = re.sub(r'\n\.', r'. ', text)
    text = re.sub(r'\.\s\n\s*\.', r'. \n', text)
    text = re.sub(r'\.\s*\.\s\n', r'. \n', text)
    text = re.sub(r'\s+\.\s\n', r'. \n', text)
    text = re.sub(r'\n\.\s*\n', r'\n', text)

    return text


def preprocess_text(text: str) -> str:
    """ Improve text before tokenize """

    # REMOVE_HORIZONTAL_ELLIPSIS_BEFORE_PERIOD
    text = text.replace('….', '.')

    # qmarks = '[“”〝〞«»]' https://stackoverflow.com
    # /questions/13535172/list-of-all-unicodes-open-close-brackets
    if REMOVE_QUOTATION_MARKS_IF_MULT_SENT_INSIDE:
        text = re.sub(
            r'[“〝«]([^“〝«”〞»]*?[А-ЯZ-Z][\.\!\?][^“〝«”〞»]*?)[”〞»]',
            r'\1', text)
        # Do not try with general quote marks " - impossible to guess begin/end
        # More strict pattern:
        text = re.sub(
            r'\s*[\"\']([А-ЯZ-Z][а-яa-z][^\"\']*?[\.\!\?][^\"\']*?)[\"\']',
            r'.\n\1', text)

    if HANDLE_LOTS_OF_SPACES_AS_SENTENCES_SEPARATOR_BY_PATTERN:
        text = re.sub(r'([А-яA-z0-9])\s{4,}([А-ЯA-Z0-9])', r'\1. \2', text)

    if REPLACE_PERIOD_WITH_BRACKET_IN_LIST_ELEMENTS:
        text = re.sub(r'^\s*(\d+)\.\s?([“”〝〞«»\'\"]?[А-ЯA-Z])', r'\1) \2',
                      text)
        text = re.sub(r'([\.\!\?:])\s+(\d+)\.\s?([“”〝〞«»\'\"]?[А-ЯA-Z])',
                      r'\1 \2) \3', text)
        # special case for 1)
        text = re.sub(r'([\.\!\?:])\s+1\)\s([А-ЯA-Z])', r'. 1) \2', text)

    if FIX_MISSING_SPACE_BETWEEN_SENTENCES:
        text = re.sub(r'([а-яa-z])\.([А-ЯA-Z])', r'\1. \2', text)
        text = re.sub(r'([а-яa-z])\?([А-ЯA-Z])', r'\1. \2', text)
        text = re.sub(r'([а-яa-z])\!([А-ЯA-Z])', r'\1. \2', text)

    # Replace HORIZONTAL_ELLIPSIS to PERIOD in the end of sentence
    # --text = re.sub(r'([А-яA-z0-9])…\s?([А-ЯA-Z0-9])', r'\1. \2', text)
    text = re.sub(r'…\s?([А-ЯA-Z0-9])', r'. \1', text)

    # Replace any whitespace to space
    text = re.sub(r'\s', ' ', text)
    # Replace sequence of spaces with single space
    text = ' '.join(text.split())

    return text


def tokenize(html: str, language='english') -> List[str]:
    """ Find sentences in input HTML code """
    text = html2text(html)
    text = preprocess_text(text)
    sentences = nltk.tokenize.sent_tokenize(text, language)
    good_sentences = [sent for sent in sentences \
        if len(sent.split()) > 1]
    return good_sentences
