import fitz
import pypdf

def highlight_words(text):
    doc = fitz.open("results.pdf")
    if isinstance(text, str):
        text = [text]
    for page in doc:
        for el in text:
            text_instances = page.search_for(el)
            for inst in text_instances:
                page.add_highlight_annot(inst)
    doc.save("results.pdf", incremental=True, encryption=0)

def save_results(reader, results, text):
    values = sorted(results.keys(), reverse=True)
    writer = pypdf.PdfWriter()
    output = "results.pdf"
    i = 1
    while i < 10 or IndexError:
        try:
            if isinstance(results[values[i]], list):
                page_number = results[values[i]][0]
            else:
                page_number = results[values[i]]
            writer.add_page(reader.pages[page_number - 1])
            i += 1
        except IndexError:
            i += 1
            break
    with open(output, "wb") as f:
        writer.write(f)
    highlight_words(text)
