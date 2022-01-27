from collections import defaultdict


class WordIndexedSparseMatrix:
    """A WordIndexedSparseMatrix object represents a 2D table with string indexing
    and fast access to all added values in specific rows/columns."""

    def __init__(self):
        self.rows = {}
        self.cols = {}

    def from_bigram_list(bigram_list):
        """Constructs a WordIndexedSparseMatrix object using a list of bigrams.
        The matrix values are counts of the bigrams"""
        matrix = WordIndexedSparseMatrix()
        for (word1, word2) in bigram_list:
            matrix[word1, word2] += 1

        return matrix

    def __getitem__(self, key):
        word1, word2 = key
        if word1 in self.rows and word2 in self.rows[word1]:
            return self.rows[word1][word2]
        else:
            # When accessing non-existent value, always return 0
            return 0

    def __setitem__(self, key, value):
        word1, word2 = key

        if word1 not in self.rows:
            self.rows[word1] = {}
        if word2 not in self.cols:
            self.cols[word2] = {}

        self.rows[word1][word2] = value
        self.cols[word2][word1] = value

    def get_sparse_column(self, key):
        return self.cols[key]

    def get_sparse_row(self, key):
        return self.rows[key]

    def union_keys(self, key1, key2, dim):
        """Returns a set of keys that are present in both rows/columns that were specified.
        `dim` is either "row" to select two rows or "column" to select two columns
        """
        if dim not in ["row", "column"]:
            raise ValueError("dim must be 'row' or 'column'")

        if dim == "row":
            get_dict_fn = self.get_sparse_row
        if dim == "column":
            get_dict_fn = self.get_sparse_column

        dict1 = get_dict_fn(key1)
        dict2 = get_dict_fn(key2)
        keys = set().union(dict1.keys(), dict2.keys())

        return keys

    def values(self):
        """Return all values stored in the matrix"""
        return [val for row in self.rows.values() for val in row.values()]

    def keys(self):
        """Return all keys stored in the matrix"""
        return [(key1, key2) for key1 in self.rows for key2 in self.rows[key1]]


class Classes:
    """Classes object maintains a mapping from words to word classes."""

    def __init__(self, classes_list):
        self.classes_list = classes_list
        self.classes = {key: idx for idx, key in enumerate(self.classes_list)}
        self.classes_set = list(set(self.classes_list))

    def get_unique_classes(self):
        return self.classes_set

    def map_word_to_class(self, word):
        if word in self.classes:
            class_idx = self.classes[word]
            return self.classes_list[class_idx]
        else:
            return word

    def map_bigram_to_classes(self, bigram):
        word1, word2 = bigram
        return self.map_word_to_class(word1), self.map_word_to_class(word2)

    def merge_classes(self, class1, class2):
        """Merges the `class2` into the `class1`"""
        idx1 = self.classes[class1]
        idx2 = self.classes[class2]
        # print("bef", self.classes_list)

        for cls, idx in self.classes.items():
            if idx == idx2:
                self.classes[cls] = idx1
        for i, cls in enumerate(self.classes_list):
            if cls == class2:
                self.classes_list[i] = class1

        # print("aftr", self.classes_list)
        self.classes_set = list(set(self.classes_list))

    def get_class_members(self):
        class_members = defaultdict(list)
        for word in self.classes:
            cls = self.map_word_to_class(word)
            class_members[cls].append(word)
        return dict(class_members)


classes = Classes([1, 2, 3, 4, 5, 6, 7, 8, 9])
assert classes.get_unique_classes() == [1, 2, 3, 4, 5, 6, 7, 8, 9]
classes.merge_classes(1, 5)
assert classes.map_word_to_class(1) == 1
assert classes.map_word_to_class(5) == 1
assert classes.map_word_to_class(3) == 3
assert classes.get_unique_classes() == [1, 2, 3, 4, 6, 7, 8, 9]
classes.merge_classes(2, 1)
assert classes.map_word_to_class(1) == 2
assert classes.map_word_to_class(2) == 2
assert classes.map_word_to_class(5) == 2
classes.get_unique_classes()
assert classes.get_unique_classes() == [2, 3, 4, 6, 7, 8, 9]
