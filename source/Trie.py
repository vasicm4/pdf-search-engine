import pickle, re, pypdf

class TrieNode:
    def __init__(self):
        self.children = {}
        self.indexes = {}
        self.is_end_of_word = False

    def evaluate_node(self):
        return len(self.indexes.values())


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, expression, line, index):
        node = self.root
        for char in expression.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if node.indexes is {}:
            node.indexes = {line: [index]}
        elif line not in node.indexes:
            node.indexes[line] = [index]
        else:
            node.indexes[line].append(index)

    def depth_first_search(self, node, expression, suggestions):
        if node.is_end_of_word:
            suggestions.append(expression)
        for char, child in node.children.items():
            self.depth_first_search(child, expression + char, suggestions)

    def search_autocomplete(self, expression):
        node = self.root
        for char in expression.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        suggestions = []
        self.depth_first_search(node, expression.lower(), suggestions)
        return suggestions

    def search(self, expression):
        node = self.root
        for char in expression.lower():
            if char not in node.children:
                return {}
            node = node.children[char]
        return node.indexes

    def evaluate(self, expression):
        node = self.root
        for char in expression.lower():
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.evaluate_node()
    
def load_tries():
    tries = {}
    with open("source/objects/tries.pickle", "rb") as file:
        tries = pickle.load(file)
    return tries

def generate_trie(reader, tries = {}):
    i = 2
    for page_number in range(23, len(reader.pages)):
        trie = Trie()
        tries[i] = trie
        line_list = reader.pages[i].extract_text().split("\n")
        for line in range(len(line_list)):
            for match in re.finditer(r"\b\w+\b", line_list[line]):
                word = match.group()
                trie.insert(word, line, match.start())
        i += 1
    with open("source/objects/tries.pickle", "wb") as file:
        pickle.dump(tries, file)

if __name__ == "__main__":
    generate_trie(pypdf.PdfReader("public/Data Structures and Algorithms Using Python.pdf"))
