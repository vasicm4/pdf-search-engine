from Graph import load_graph, Graph, Vertex, Edge
from Trie import load_tries, Trie, TrieNode
import Results
import Menu
import re
import pypdf


class Main:
    def __init__(self):
        self.reader = pypdf.PdfReader("public/Data Structures and Algorithms Using Python.pdf")
        self.tries = load_tries()
        self.graph = load_graph()
        self.word_pages = {}
        self.query = Menu.start()
        # self.query = "python"
        self.search()

    def search(self):
        words_to_search = self.query.split(" ")
        if re.match(r'.*\*$', self.query):
            self.autocomplete(self.query[:-1].rstrip())
        elif len(words_to_search) == 1:
            self.single_word_search(self.query.strip())
            if len(self.word_pages) < 20:
                self.alternative_text(self.query)
            else:
                print(self.query)
        elif re.match(r'^[\'"].*[\'"]$', self.query):
            self.phrase_search(self.query)
        elif any(token in {"AND", "OR", "NOT"} for token in words_to_search):
            self.logical_operations(self.query)
        else:
            self.multiple_word_search(self.query)

    def print_text(self, text):
        i = 1

        inverted = {}
        for key in self.word_pages[text].keys():
            if self.word_pages[text][key] not in inverted:
                inverted[self.word_pages[text][key]] = [key]
            inverted[self.word_pages[text][key]].append(key)
        values = sorted(inverted.keys(), reverse=True)
        breakable = False

        for value in values:
            for page_number in inverted[value]:
                indexes = self.tries[page_number - 1].search(text.split(" ")[0])
                for line_number in indexes.keys():
                    j = 0
                    for index in indexes[line_number]:
                        print(f"Page {page_number}")
                        print(f"  Line {line_number + 1}")
                        line = self.reader.pages[page_number].extract_text().split("\n")[line_number]
                        print("     Index: " + str(i))
                        if (indexes[line_number].index(index) == 0 or indexes[line_number].index(index)
                                == len(indexes[line_number]) - 1):
                            print("       " + line[j:index] + '\033[91m' + text + '\033[0m' + line[index + len(text):])
                        else:
                            print("       " + line[j:index] + '\033[91m' + text + '\033[0m')
                        j = index + len(text)
                        i += 1
                    if i % 10 == 0:
                        choice = input("Enter 0 to exit, any other key to continue: ")
                        if choice == "0":
                            breakable = not breakable
                            break
                        else:
                            print("\n")
                if breakable:
                    break
            if breakable: 
                break

        save = input("Do you want to save the results? (y/n): ")
        match save:
            case "y" | "Y":
                Results.save_results(self.reader, inverted, text)
                exit()
            case "n" | "N":
                exit()
            case _:
                print("Invalid choice")

    def print_multiple_text(self, pages_evaluation, words):
        i = 1
        inverted = {}
        for key in pages_evaluation.keys():
            if pages_evaluation[key] == 0:
                continue
            if pages_evaluation[key] not in inverted:
                inverted[pages_evaluation[key]] = [key]
            inverted[pages_evaluation[key]].append(key)
        values = sorted(inverted.keys(), reverse=True)
        breakable = False
        for value in values:
            for page_number in inverted[value]:
                j = 0
                indexes = {}
                if len(words) == 1:
                    indexes[words[0]] = self.tries[page_number - 1].search(words[0])
                else:
                    for word in words:
                        indexes[word] = self.tries[page_number - 1].search(word)
                for line_number in indexes[words[0]].keys():
                    print(f"Page {page_number}")
                    print(f"  Line {line_number + 1}")
                    # for index in indexes[words[0]][line_number]:
                    line = self.reader.pages[page_number - 1].extract_text().split("\n")[line_number]
                    print(line)
                    print("     Index: " + str(i))
                    for word in words:
                        line = re.sub(f'\\b({re.escape(word)})\\b', r'\033[1;31m\1\033[0m',
                                      line, flags=re.I)
                    print("       " + line)
                    i += 1
                    j += 1
                    if i % 10 == 0:
                        choice = input("Enter 0 to exit, any other key to continue: ")
                        if choice == "0":
                            breakable = not breakable
                            break
                        else:
                            print("\n")
                if breakable:
                    break
            if breakable: 
                break
        save = input("Do you want to save the results? (y/n): ")
        match save:
            case "y" | "Y":
                Results.save_results(self.reader, inverted, words)
                exit()
            case "n" | "N":
                exit()
            case _:
                print("Invalid choice")

    def words_and(self, operand, values):
        for page in range(23, len(self.reader.pages)):
            page_number = page + 1
            if page_number in operand.keys() and page_number in values.keys():
                if operand[page_number] == 0 or values[page_number] == 0:
                    values.pop(page_number)
                    continue
                result = operand[page_number] + values[page_number] + self.graph.evaluate_page(page_number)
                values[page_number] = result
            elif page_number in values.keys():
                values.pop(page_number)
        return values

    def words_or(self, operand, values):
        for page in operand.keys():
            if page in values.keys():
                result = operand[page] + values[page] + self.graph.evaluate_page(page)
                values[page] = result
            else:
                result = operand[page] + self.graph.evaluate_page(page)
                values[page] = result
        for page in values.keys():
            if page not in operand.keys():
                result = values[page] + self.graph.evaluate_page(page)
                values[page] = result
        return values

    def words_not(self, operand, values):
        pages = list(operand.keys())
        for page in pages:
            if values[page] != 0:
                values.pop(page)
            else:
                values[page] = operand[page] + self.graph.evaluate_page(page)
        return values

    def logical_operations(self, text):
        tokens = []
        queue = []
        stack = []
        words = []
        pattern = re.compile(r'\b(?:AND|OR|NOT)\b|\(|\)|\w+', re.IGNORECASE)
        for match in re.finditer(pattern, text):
            tokens.append(match.group())
        for token in tokens:
            if token not in ["AND", "OR", "NOT", "(", ")"]:
                queue.append(token)
                words.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    queue.append(stack.pop())
                stack.pop()
            elif token == "NOT":
                if stack and stack[-1] == "NOT":
                    queue.append(stack.pop())
                stack.append(token)
            elif len(stack) != 0:
                if stack[-1] == "NOT":
                    queue.append(stack.pop())
                    if stack[-1] == "AND":
                        queue.append(stack.pop())
                    stack.append(token)
                elif stack[-1] == "AND":
                    queue.append(stack.pop())
                    stack.append(token)
                elif stack[-1] == "OR":
                    stack.append(token)
                else:
                    stack.append(token)
            else:
                stack.append(token)
        while stack:
            queue.append(stack.pop())
        for token in queue:
            if token not in ["AND", "OR", "NOT"]:
                stack.append(token)
            elif token == "AND":
                word1 = stack.pop()
                word2 = stack.pop()
                if isinstance(word1, str):
                    operand = self.single_word_search(word1)
                else:
                    operand = word1
                if isinstance(word2, str):
                    values = self.single_word_search(word2)
                else:
                    values = word2
                stack.append(self.words_and(operand, values))
            elif token == "OR":
                word1 = stack.pop()
                word2 = stack.pop()
                if isinstance(word1, dict):
                    operand = word1
                else:
                    operand = self.single_word_search(word1)
                if isinstance(word2, dict):
                    values = word2
                else:
                    values = self.single_word_search(word2)
                stack.append(self.words_or(operand, values))
            elif token == "NOT":
                word1 = stack.pop()
                word2 = stack.pop()
                if isinstance(word1, str) and isinstance(word2, str):
                    values = self.single_word_search(word1)
                    operand = self.single_word_search(word2)
                    words.remove(word1)
                else:
                    #word1 will always be negated
                    if isinstance(word1, dict):
                        values = word1
                    else:
                        values = self.single_word_search(word1)
                        words.remove(word1)
                    if isinstance(word2, dict):
                        operand = word2
                    else:
                        operand = self.single_word_search(word2)
                stack.append(self.words_not(operand, values))
        values = stack.pop()
        self.print_multiple_text(values, words)

    def single_word_search(self, word):
        for page in self.tries.keys():
            result = self.tries[page].evaluate(word) + self.graph.evaluate_page(page)
            if word not in self.word_pages.keys():
                self.word_pages[word] = {page: result}
            else:
                self.word_pages[word][page] = result

    def multiple_word_search(self, words):
        words_split = words.split(" ")
        pages_evaluation = {}
        for word in words_split:
            self.single_word_search(word)
            for page in self.word_pages[word].keys():
                if page not in pages_evaluation:
                    pages_evaluation[page] = 0
                pages_evaluation[page] += self.word_pages[word][page]
        for page in pages_evaluation:
            for word in words_split:
                if word not in self.word_pages.keys():
                    continue
                pages_evaluation[page] += len(words_split) * 10
        self.print_multiple_text(pages_evaluation, words_split)

    def phrase_search(self, text):
        text = text[1:-1]
        words = text.split(" ")
        phrase_evaluation = {}
        phrase_evaluation[text] = {}
        for page in self.tries.keys():
            boolean = True
            for word in words:
                result = self.tries[page].search(word)
                if len(result) == 0:
                    boolean = False
                    break
                if page not in phrase_evaluation.keys():
                    phrase_evaluation[word] = {page: 0}
                phrase_evaluation[word][page] += len(result)
            if boolean:
                for word in words:
                    if page not in phrase_evaluation[text].keys():
                        phrase_evaluation[text][page] = 0
                    phrase_evaluation[text][page] += phrase_evaluation[word][page]
                    if phrase_evaluation[text][page] == 0:
                        phrase_evaluation[text].pop(page)
        for word in words:
            del phrase_evaluation[word]
        self.word_pages[text] = phrase_evaluation[text]
        self.print_text(text)

    def alternative_text(self, text):
        new_text = text[:len(text)//2]
        found = {}
        ranked = {}
        for page in self.tries.keys():
            suggestions = self.tries[page].search_autocomplete(new_text)
            for suggestion in suggestions:
                if suggestion not in found:
                    found[suggestion] = self.tries[page].evaluate(suggestion)
                found[suggestion] += self.tries[page].evaluate(suggestion)
                if len(suggestion) == len(text):
                    found[suggestion] += 10
        for page in found.keys():
            if found[page] < 5:
                continue
            ranked[found[page]] = page
        keys = list(sorted(ranked.keys(), reverse=True))
        if ranked[keys[0]] == text:
            self.single_word_search(ranked[keys[0]])
            self.print_text(ranked[keys[0]])
        print("Did you mean: " + ranked[keys[0]])
        while True:
            choice = input("(y/n): ")
            if choice == "y" or choice == "Y":
                self.single_word_search(ranked[keys[0]])
                self.print_text(ranked[keys[0]])
            elif choice == "n" or choice == "N":
                return
            else:
                print("Invalid choice")
                continue

    def autocomplete(self, text):
        found = {}
        ranked = {}
        for page in self.tries.keys():
            suggestions = self.tries[page].search_autocomplete(text)
            for suggestion in suggestions:
                if suggestion not in found:
                    found[suggestion] = self.tries[page].evaluate(suggestion)
                found[suggestion] += self.tries[page].evaluate(suggestion)
        for page in found.keys():
            if found[page] < 5:
                continue
            ranked[found[page]] = page
        keys = list(sorted(ranked.keys(), reverse=True))
        while ValueError:
            try:
                if len(keys) == 0:
                    print("No results found")
                    return
                for i in range(len(keys)):
                    print(f"{i+1}. {ranked[keys[i]]}")
                choice = input("Enter the number of the word you want to search: ")
                if 0 < int(choice) < len(keys)+1:
                    self.single_word_search(ranked[keys[int(choice)-1]])
                    self.print_text(ranked[keys[int(choice)-1]])
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid choice")

if __name__ == "__main__":
    main = Main()
