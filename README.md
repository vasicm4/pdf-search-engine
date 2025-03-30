# 📄 PDF Search Engine

PDF Search Engine is keyword-based PDF search engine with fully functioning logical operations, trie autocomplete, graph-based ranking and highlighted key-word exports.

Evaluating Search Engine performance is accomplished using Data Structures and Algorithms in Python book which can be found in [public directory](./public).

***
## 🔧 Technologies
![Static Badge](https://img.shields.io/badge/python-3.12%2B-blue)
![Static Badge](https://img.shields.io/badge/Library-PyPDF-blue)
![Static Badge](https://img.shields.io/badge/Library-PyMuPDF-blue)
![Static Badge](https://img.shields.io/badge/Library-Pickle-green)
![Platform](https://img.shields.io/badge/Platform-Windows_|_Linux_|_MacOS-lightgrey?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

<a name="specification"><a/>
## 📌 Specification:

1. **Pre-Indexing**

The system processes the PDF document upon startup, extracting data from text into efficient data structures for quick retrieval.

2. **Ranked Search Results**

Results are ranked based on keyword occurrences. Additional ranking heuristics include keyword density and relative importance.

3. **Multi-Word Queries**

Users can enter one or more words separated by spaces. Pages containing all words are prioritized over partial matches. Frequency of each word in the document affects ranking.

4. **Logical Operators**

Supports AND, OR, NOT for complex query logic.

5. **Pagination**

Displays a limited number of results per page. Users can navigate through pages to view more results.

6. **Graph-Based Ranking**

Uses references within the document (e.g., "See page X") to improve ranking. Pages referenced frequently by other pages gain higher ranking.

7. **Trie-Based Indexing**

Uses a Trie (prefix tree) for fast word lookup, allows efficient autocomplete and prefix searches, reduces search time compared to traditional list-based approaches.

8. **Auto-Complete & Suggestions**

Provides query completion based on indexed words. "Did you mean?" feature suggests alternative words if the query has few or no results.

9. **PDF Export & Highlighting**

Allows users to save search results as a separate PDF file, extracted pages with relevant matches are compiled into a new document, highlights keywords in the exported PDF for easier identification.

***
## 📋 Contents
1. [Specification](#specification)
2. [Dependencies](#dependencies)
3. [Getting Started](#start)
4. [Functionalities](#functionalities)
    1. [Single/Multiple Word Search](#word-search)
    2. [Phrase Search](#phrase)
    3. [Logical Operations](#logical-operations)
    4. [Autocomplete](#autocomplete)
4. [License](#license)
5. [Contact](#contact)

***
<a name="dependencies"><a/>
## ⚒️ Dependencies
In order to run this project properly you need to make sure that you have installed:
1. **Python programming language - Version 3.12 and above**: you can download python [here](https://www.python.org/downloads/).
2. **MyPDF Library**: free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files
3. **pyMuPDF Library**:   high-performance Python library for data extraction, analysis, conversion & manipulation of PDF (and other) documents.
4. **Python IDE or text editor**: you can use either [PyCharm](https://www.jetbrains.com/pycharm/) or [Visual Studio Code](https://code.visualstudio.com/)
5. **Git** (optional): if you want to download this project and contribute to it

***
<a name="start"><a/>
## 🚀 Getting Started

1. **Clone the Repository**:
   
    Open a terminal and run the following command to clone the repository:


   ```bash
   https://github.com/vasicm4/pdf-search-engine.git
    ```
    Alternatively, download the repository as a ZIP file and extract it.

2. **Installation of additional libraries and dependencies**:
   - Open terminal or command prompt based on operating system
   - Navigate to the folder where the repository is located
   - Insert `pip install -r requirements.txt` in terminal
   
   Alternatively you can execute `pip install pypdf PyMuPDF`

3. **Run the program**:
    - To start the program type `python source/main.py` in your terminal

4. **Make a choice and enter desired query**:
    - You can enter anything you want, but try to stay within context of the file for optimal results.
    
    Here are a few examples of good inputs:
        
        tree
        python AND node
        python NOT value

    Here are some of them with unoptimal results:
        
        sunflower
        corn AND pasta
        airoplane NOT water 
    
    
***
<a name="functionalities"><a/>
## 💡 Functionalities
   
  Upon starting the program a simple menu with 3 options appear, by inserting one of the numbers you can:
    
1. search for a query
2. view a guide
3. exit the program

There are multiple search options available:

1. [Single/Multiple Word Search](#word-search)
2. [Phrase Search](#phrase)
3. [Logical Operations](#logical-operations)
4. [Autocomplete](#autocomplete)

They will all be listed subsequently
   
***
<a name="word-search"><a/>
## 🔍 Single/Multi Word Search

On entering a query, the system scans the document and created data structures for ranked results, after which it displays them based on it's value.

### Page Ranking

- **Keyword Appearance:** more occurences - higher rank
- **Page Reference:** if another page references the current one, it's rank increases
- **Distinct keywords bonus**: More unique keywords = better ranking.


### Example Queries:

    python
    node 
    linked list
    
### Example Result:
    Page 35
    Line 16
     Index: 1
       pythonnt, and r=n%m being the “remainder” to ensure that q
    Page 35
      Line 25
         Index: 2
           pythonise exclusive-or
    Page 35
      Line 29
         Index: 3
           Each of Pytpythonbuilt-in sequence types ( str,tuple ,a n dlist) support the following
    Page 35
      Line 31
         Index: 4
           s[j] element at index jpython

***
<a name="phrase"><a/>
## 🔍 Phrase Search
   
   Phrase search allows users to look for an exact sequence of words (phrase) by enclosing them in double quotes (").
   
   ### Example Query:
If you enter a phrase:

    "linked list"
    
The system will only return results where "linked list" appears exactly as written, rather than separate occurrences of "linked" and "list" on the same page. This ensures that the search retrieves only results where the words appear together in the correct order.

Below is an example of phrase search results:
   
    Page 278
    Line 1
     Index: 1
       7.1. Singly Linlinked list57
    Page 278
    Line 10
     Index: 2
       by following each node’s next reference, we can reach the linked list list. We can
    Page 278
    Line 12
     Index: 3
       commonly known as traversilinked listed list. Because the next reference of a
    Page 278
    Line 14
     Index: 4
       a list is allinked list link hopping orpointer hopping .
    Page 278
    Line 18
     Index: 5
       would be no way to locate that nodelinked listctly, any others). There is not an
    Page 278
    Line 18
     Index: 6
       ctly, any others)linked listnot an
   
***
<a name="logical-operations"><a/>
## 🔍 Logical Operations

Search Engine allows users to filter query entries using logical operators `AND`, `OR` and `NOT` where:
 - `AND` - returns results that contain both words 
 - `OR` - returns results that contain either of words inserted
 - `NOT` - returns pages that don't contain particular entry
 
 It is possible for users to group multiple logical operations by using brackets ( )

### Example Queries:


    python AND node
    linked OR tree
    node NOT tree
    python AND node NOT tree
    python OR (linked AND list)
    
These queries will return results based on previous definitions of logical operators `AND`, `OR` and `NOT`.

    Page 278
      Line 10
    In this chapter, we introduce a data structure known as a linked list ,w h i c h
         Index: 2
           In this chapter, we introduce a data structure known as a linked list ,w h i c h
    Page 278
      Line 12
    array-based sequences and linked lists keep elements in a certain order, but us-
         Index: 3
           array-based sequences and linked lists keep elements in a certain order, but us-
    Page 278
      Line 14
    elements. A linked list, in contrast, relies on a more distributed representation in
         Index: 4
           elements. A linked list, in contrast, relies on a more distributed representation in
    Page 278
      Line 18

### Example


***
<a name="autocomplete"><a/>
## 🔍 Autocomplete

Search engine provides us autocomplete suggestions when we insert * at the end of our query. This helps us optimize search results without typing the whole word we want to look for. 


   ### Example Query: 
   
    lin*
    
   ### Results:
   ```
    1. linked
    2. linear
    3. line
    4. linkedbinarytree
    5. lines
    6. link
    7. linkedqueue
    8. links
    9. linkedstack
    10. linking
    11. linda
    12. linkeddeque
   ```
   
   ### Word Choice:
  Next step is to choose one of the words via typing a number that is right in front of it.
  
  `Enter the number of the word you want to search: 3`
  
  This choice will trigger [Single Word Search](#single-word) for the word `line`
   
    Page 24
    Line 19
     Index: 1
        )line
    Page 24
      Line 19
         Index: 2
            )line
    Page 53
      Line 16
         Index: 3
           fp.read()line
    Page 53
      Line 16
         Index: 4
           fp.read()line
    Page 175
      Line 11
         Index: 5
           linerval(3)
    Page 175
      Line 20
         Index: 6
           line(1)
   
***
<a name="license"><a/>
## ⚖️ License
This project is licensed under the [MIT License](./LICENSE). See the [LICENSE](./LICENSE) file for details.

***
<a name="contact"><a/>
## ☎️ Contact me

 - **Email**: [vasicmaksim4@gmail.com](mailto:vasicmaksim4@gmail.com)
 - **Github**: [vasicm4](https://github.com/vasicm4)
 - **Linkedin**: [Maksim Vasic](https://rs.linkedin.com/in/maksim-vasi%C4%87-514b11327)
***
