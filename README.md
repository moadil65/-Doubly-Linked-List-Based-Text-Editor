# -Doubly-Linked-List-Based-Text-Editor
A lightweight, console-based text editor built from scratch using doubly linked lists in Python. Supports character-by-character editing, cursor navigation, undo/redo functionality, and file saving/loading, all without relying on built-in text structures. Designed as a data structure-focused learning project.

## 🚀 Features

- 📄 **Line-by-line document structure** using a doubly linked list
- ✏️ **Character-level insertion and deletion**
- 🧭 **Cursor navigation** (forward, back, home, end, goto)
- ↩️ **Undo/Redo** operations with state management
- 💾 **Save and load** documents from plain text files
- 📊 **Character and line counting**
- 📟 **Console interface** with user-friendly commands


## How it Works:

- Each line in the document is a node in a doubly linked list.
- Each character in a line is a node in another doubly linked list.
- The editor maintains a cursor with its row, column, and a direct reference to the character node.
- Undo/redo is implemented using deep copies of the editor state.

## Commands

- Command	        -->       Description
- goto row col	  -->       Move cursor to specific row and column
- forward	        -->       Move cursor forward
- back	          -->       Move cursor backward
- home	          -->       Move cursor to start of line
- end	            -->       Move cursor to end of line
- insert string	  -->       Insert string after the cursor
- delete num	    -->       Delete num characters from cursor
- countcharacters	 -->      Count total characters in document
- countlines	    -->       Count total lines in document
- printdoc	      -->       Print current document to console
- save filename	  -->       Save document to a file
- load filename	  -->       Load document from a file
- undo	          -->       Undo last change
- redo	          -->       Redo last undone change
- quit	          -->       Exit the editor

## Here are some commands which you can try on this

- Welcome to DS Text Editor
- Enter commands at the prompt

- -> goto 0 0
- -> insert Comp 200
- -> goto 2 0
- -> insert This editor is
- -> goto 2 21
- -> insert -=COOL=-
- -> goto 3 0
- -> insert Bye
- -> goto 4 0
- -> insert .
- -> countLines
- 5
- -> printDoc
Comp 200
This editor is -=COOL=-
Bye
.
- -> quit
