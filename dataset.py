import numpy as np
from collections import Counter

def read_word_list(filepath):
    """Reads a list of words from a given filepath

    Parameters
    ----------
    filepath : str
        The file location of the dataset

    Returns
    -------
    list
        a list of strings. Each string is one word
        from the dataset
    """
    words = []
    with open(filepath, "r", encoding="iso-8859-2") as fp:
        for line in fp:
            line = line.rstrip()
            words.append(line)
    return words


def pairs(list_of_words, distance):
    """Returns a list of tuples, each containing two words from the input list.

    Args:
        list_of_words (list): Input list of words
        distance (int): Distance between words in output tuples

    Yields:
        tuple: word pair
    """
    # assert len(list_of_words) > distance + 1

    for word1, word2 in zip(list_of_words, list_of_words[distance:]):
        yield (word1, word2)


# tests for pairs function
assert list(pairs([1, 2, 3, 4], 1)) == [(1, 2), (2, 3), (3, 4)]
assert list(pairs([1, 2, 3, 4], 2)) == [(1, 3), (2, 4)]
assert list(pairs([1, 2, 3, 4], 10)) == []


def find_common_words(list_of_words, occurence_threshold):
    counter = Counter(list_of_words)
    return {elem for elem, count in counter.items() if count >= occurence_threshold}


find_common_words([0, 0, 0, 0, 1, 1, 2, 2, 3], 1) == {0, 1, 2, 3}
find_common_words([0, 0, 0, 0, 1, 1, 2, 2, 3], 2) == {0, 1, 2}
find_common_words([0, 0, 0, 0, 1, 1, 2, 2, 3], 4) == {0}
find_common_words([0, 0, 0, 0, 1, 1, 2, 2, 3], 5) == set()
find_common_words([], 0) == set()


def filter_pairs_by_vocabulary(pairs, vocabulary):
    for word1, word2 in pairs:
        if word1 not in vocabulary or word2 not in vocabulary:
            continue
        yield (word1, word2)


_test_pairs = [(1, 2), (2, 3), (1, 3)]
assert list(filter_pairs_by_vocabulary(_test_pairs, {1, 2, 3, 4})) == _test_pairs
assert list(filter_pairs_by_vocabulary(_test_pairs, {1, 3})) == [(1, 3)]
assert list(filter_pairs_by_vocabulary(_test_pairs, {1})) == []


def read_ptg_corpus(filepath):
    """Reads tagged sentences from a given filepath

    Parameters
    ----------
    filepath : str
        The file location of the dataset

    Returns
    -------
    list
        a list of lists of tuples. Each list represents
        a sentence and each tuple represents a tagged token.
    """
    tagged_sentences = []
    with open(filepath, "r", encoding="iso-8859-2") as fp:
        # skip the first line
        next(fp)
        sentence = []
        for line in fp:
            line = line.rstrip()
            if line == "###/###":
                # do not add empty sentences
                if sentence:
                    tagged_sentences.append(sentence)
                sentence = []
            else:
                token, tag = line.split("/")
                sentence.append((token, tag))

    # filter out "empty" sentences in the czech corpus
    tagged_sentences = filter_empty_sentences(tagged_sentences)

    return np.array(tagged_sentences, dtype=object)


def filter_empty_sentences(sentences):
    """Goes through a list of tagged sentences and filters out
    sentences comprised only out of the tag "Z:-------------".
    """
    result = []
    for sentence in sentences:
        if not all([tag == "Z:-------------" for _, tag in sentence]):
            result.append(sentence)
    return result


# def test_read_ptg_corpus():
#     tagged_sentences = read_ptg_corpus("data/TEXTCZ2.ptg")
#     for i,sentence in enumerate(tagged_sentences):
#         assert len(sentence) > 0, i
#         for word in sentence:
#             assert len(word) == 2, word

# def test_filter_empty_sentences():
#     a = filter_empty_sentences([
#         [("-", "Z:-------------"), ("Je", "VB-S---3P-AA---")],
#         [("-", "Z:-------------"),("-", "Z:-------------")]
#     ])
#     assert len(a) == 1

# test_filter_empty_sentences()
# test_read_ptg_corpus()
