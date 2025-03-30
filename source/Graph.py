import pickle, re, pypdf

class Vertex:
    def __init__(self, text, page):
        self.text = text
        self.page = page

    def __hash__(self):
        return hash(self.page)


class Edge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def endpoints(self):
        return self.origin, self.destination

    def __hash__(self):
        return hash((self.origin, self.destination))

class Graph:
    def __init__(self):
        self.vertices = {}
        self.outgoing = {}
        self.incoming = {}

    def insert_vertex(self, text, page):
        vertex = Vertex(text, page)
        self.vertices[page] = vertex
        self.outgoing[page] = []
        self.incoming[page] = []

    def get_vertex(self, page):
        return self.vertices[page]

    def edge_count(self):
        count = 0
        for edges in self.outgoing.values():
            count += len(edges)
        return count

    def edge(self, u, v):
        return self.outgoing[u][v]

    def incident_edges(self, vertex):
        return self.outgoing[vertex]

    def evaluate_page(self, page):
        return len(self.incoming[page])

    def insert_edge(self, origin, destination):
        edge = Edge(origin, destination)
        self.outgoing[origin].append(edge)
        self.incoming[destination].append(edge)

    def remove_edge(self, edge):
        self.outgoing[edge.origin].remove(edge)
        self.incoming[edge.destination].remove(edge)

def load_graph():
    graph = Graph()
    with open("source/objects/graph.pickle", "rb") as file:
        graph = pickle.load(file)
    return graph

def generate_graph(reader):
    graph = Graph()
    i = 2
    for page_number in range(23, len(reader.pages)):
        page_content = reader.pages[page_number].extract_text()
        graph.insert_vertex(page_content, i)
        i += 1
    pattern = r'\b(?:see|on)\s+pages?\s+\d+(?:\s+(?:and|-)\s+\d+)*\b'
    for page_number in range(23, len(reader.pages)):
        page = reader.pages[page_number].extract_text()
        matches = re.findall(pattern, page)
        for match in matches:
            match = match.replace("\n", " ")
            word_split = match.split(" ")
            if word_split[1] != "pages":
                try:
                    graph.insert_edge(page_number+1, int(word_split[2]))
                except ValueError:
                    print("Invalid page number")
                    continue
            else:
                for split in match.split(" "):
                    if '-' in split:
                        word_split = split.split("-")
                for i in range(2, len(word_split)):
                    try:
                        graph.insert_edge(page_number+1, int(word_split[i]))
                    except ValueError:
                        print("Invalid page number")
                        continue
    with open("source/objects/graph.pickle", "wb") as file:
        pickle.dump(graph, file)

if __name__ == "__main__":
    generate_graph(pypdf.PdfReader("public/Data Structures and Algorithms Using Python.pdf"))