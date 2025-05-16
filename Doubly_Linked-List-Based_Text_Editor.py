import copy

class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class TextEditor:
    def __init__(self):
        '''
        Predefined member variables.
        WARNING: DO NOT MODIFY THE FOLLOWING VARIABLES
        '''
        self.doc = None
        self.cursor_row = -1
        self.cursor_col = -1
        self.cursor_node = None
        self.current_line = None
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo_levels = 100
        self._suppress_state_save = False

    def _save_state(self):
        '''Helper method to save the current state to undo_stack'''
        if self._suppress_state_save:
            return
        state = {
            'doc': copy.deepcopy(self.doc),
            'cursor_row': self.cursor_row,
            'cursor_col': self.cursor_col,
            'cursor_node': self.cursor_node,
            'current_line': self.current_line
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def get_line_at_row(self, row):
        '''Helper method to get the line at specified row'''
        line = self.doc
        current_row = 0
        while line and current_row < row:
            line = line.next
            current_row += 1
        return line

    def get_node_at_col(self, line, col):
        '''Helper method to get the node at specified column in a line'''
        node = line.data if line else None
        current_col = 0
        while node and current_col < col:
            node = node.next
            current_col += 1
        return node

    def create_empty_line(self, length):
        '''Helper method to create an empty line with specified length'''
        if length <= 0:
            return None
        head = Node(None)  # Use None instead of empty string
        current = head
        for _ in range(length - 1):
            new_node = Node(None, prev=current)
            current.next = new_node
            current = new_node
        return head

    def goto(self, row, col):
        '''
        Moves the cursor to the location indicated by the row and col parameters
        '''
        self._save_state()
        if row < 0 or col < 0:
            return


        if self.doc is None:
            self.doc = Node(self.create_empty_line(1))
            self.cursor_row = row
            self.cursor_col = col
            self.current_line = self.doc
            self.cursor_node = self.get_node_at_col(self.doc, col)
            return

        line = self.doc
        prev_line = None
        current_row = 0

        # Find the line at the requested row or the last existing line
        while current_row < row and line and line.next:
            prev_line = line
            line = line.next
            current_row += 1

        # If we have not reached the requested row, create new empty lines
        while current_row < row:
            new_line = Node(self.create_empty_line(1), prev=line)
            if line:
                line.next = new_line
            else:
                self.doc = new_line
            line = new_line
            current_row += 1

        if line.data is None:
            line.data = self.create_empty_line(1)

        current_length = 0
        temp_node = line.data
        while temp_node:
            current_length += 1
            temp_node = temp_node.next


        if current_length <= col:

            last_node = line.data
            while last_node and last_node.next:
                last_node = last_node.next

            for _ in range(col + 1 - current_length):
                new_node = Node(' ', prev=last_node)
                if last_node:
                    last_node.next = new_node
                else:
                    line.data = new_node
                last_node = new_node

        self.cursor_row = row
        self.cursor_col = col
        self.cursor_node = self.get_node_at_col(line, col)
        self.current_line = line

    def get_line_text(self, line):
        if not line or not line.data:
            return ""
        text = []
        node = line.data
        while node:
            if node.data:
                text.append(node.data)
            node = node.next
        return "".join(text)

    def forward(self):
        '''
        Moves the cursor one step forward
        '''
        if self.cursor_row == -1 or self.cursor_col == -1:
            return

        # Try to move within current line
        if self.cursor_node and self.cursor_node.next:
            self.cursor_node = self.cursor_node.next
            self.cursor_col += 1
            return


        if self.current_line and self.current_line.next and self.current_line.next.data:
            self.current_line = self.current_line.next
            self.cursor_row += 1
            self.cursor_col = 0
            self.cursor_node = self.current_line.data

    def back(self):
        '''
        Moves the cursor one step backwards
        '''
        if self.cursor_row == -1 or self.cursor_col == -1:
            return

        if self.cursor_node and self.cursor_node.prev:
            self.cursor_node = self.cursor_node.prev
            self.cursor_col -= 1
            return


        if self.current_line and self.current_line.prev and self.current_line.prev.data:
            prev_line = self.current_line.prev
            # Find last node in previous line
            last_node = prev_line.data
            while last_node.next:
                last_node = last_node.next
            self.current_line = prev_line
            self.cursor_row -= 1
            self.cursor_node = last_node

            node = prev_line.data
            col_count = 0
            while node:
                col_count += 1
                node = node.next
            self.cursor_col = col_count - 1

    def home(self):
        '''
        Moves the cursor to the start of the current line
        '''
        if self.cursor_row == -1 or self.cursor_col == -1:
            return

        if self.current_line and self.current_line.data:
            self.cursor_node = self.current_line.data
            self.cursor_col = 0

    def end(self):
        '''
        Moves the cursor to the end of the current line
        '''
        if self.cursor_row == -1 or self.cursor_col == -1:
            return

        if self.current_line and self.current_line.data:
            node = self.current_line.data
            col = 0
            while node.next:
                node = node.next
                col += 1
            self.cursor_node = node
            self.cursor_col = col

    def insert(self, string):
        '''
        Inserts the given string immediately after the cursor
        '''
        if not string:
            return

        self._save_state()

        # Handle empty document case
        if self.cursor_row == -1 or self.cursor_col == -1:
            self.doc = Node(None)
            self.doc.data = Node(string[0])
            self.cursor_node = self.doc.data
            self.current_line = self.doc
            self.cursor_row = 0
            self.cursor_col = 0
            string = string[1:]
            if not string:
                return

        # If current line is empty, initialize it
        if self.current_line.data is None:
            self.current_line.data = Node(string[0])
            self.cursor_node = self.current_line.data
            self.cursor_col = 0
            string = string[1:]
            if not string:
                return

        if not self.cursor_node:
            return


        for char in string:
            new_node = Node(char, prev=self.cursor_node, next=self.cursor_node.next)
            if self.cursor_node.next:
                self.cursor_node.next.prev = new_node
            self.cursor_node.next = new_node
            self.cursor_node = new_node
            self.cursor_col += 1

    def delete(self, num):
        '''
        Deletes specified number of characters from the cursor position
        '''
        if num <= 0 or self.cursor_row == -1 or self.cursor_col == -1:
            return

        if not self.cursor_node or not self.current_line:
            print("Error: Nothing to delete")
            return

        self._save_state()

        remaining = num
        current_node = self.cursor_node


        while remaining > 0 and current_node:
            next_node = current_node.next
            if current_node.prev:
                current_node.prev.next = current_node.next
            else:
                self.current_line.data = current_node.next
                if current_node.next:
                    current_node.next.prev = None
            if current_node.next:
                current_node.next.prev = current_node.prev
            current_node = next_node
            remaining -= 1


        if remaining == num:
            print("Error: Could not delete any characters")
            return

        if current_node:
            self.cursor_node = current_node
        elif self.cursor_node.prev:
            self.cursor_node = self.cursor_node.prev
            self.cursor_col -= 1
        elif self.current_line.prev and self.current_line.prev.data:
            prev_line = self.current_line.prev
            last_node = prev_line.data
            col_count = 0
            while last_node.next:
                last_node = last_node.next
                col_count += 1
            self.current_line = prev_line
            self.cursor_row -= 1
            self.cursor_col = col_count
            self.cursor_node = last_node
        elif self.current_line.next and self.current_line.next.data:
            self.current_line = self.current_line.next
            self.cursor_row += 1
            self.cursor_col = 0
            self.cursor_node = self.current_line.data
        else:
            self.doc = None
            self.cursor_row = -1
            self.cursor_col = -1
            self.cursor_node = None
            self.current_line = None

    def countCharacters(self):
        '''
        Returns total number of characters in the document
        '''
        count = 0
        line = self.doc
        while line:
            node = line.data
            while node:
                count += 1
                node = node.next
            line = line.next
        return count

    def countLines(self):
        '''
        Count total lines in the document.
        '''
        count = 0
        line = self.doc
        while line:
            count += 1
            line = line.next
        return count

    def printDoc(self):
        line = self.doc
        row = 0
        while line:
            node = line.data
            line_str = []
            col = 0
            has_content = False

            while node:
                if node.data:
                    line_str.append(node.data)
                    has_content = True

                if row == self.cursor_row and col == self.cursor_col:
                    line_str.append('|')

                node = node.next
                col += 1

            if row == self.cursor_row and col == self.cursor_col:
                line_str.append('|')

            # Print the line if it has content or cursor is present
            if line_str or (row == self.cursor_row and self.cursor_col == 0):
                print(''.join(line_str))

            line = line.next
            row += 1

    def save(self, filename):
        '''
        Saves the spreadsheet to a file with name given as Parameter
        Parameters:
            fileName
        Return value:
            None
        '''
        try:
            with open(filename, 'w') as file:
                line = self.doc
                while line:
                    node = line.data
                    line_content = []

                    while node:
                        if node.data:
                            line_content.append(str(node.data))
                        node = node.next


                    file.write(''.join(line_content) + '\n')

                    line = line.next
            print(f"Document saved successfully to {filename}")
        except IOError as e:
            print(f"Error saving file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def load(self, filename):
        '''
        Loads the spreadsheet from a file with name given as Parameter
        Parameters:
            fileName
        Return value:
            None
        '''
        self._save_state()
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.doc = None
                self.cursor_row = -1
                self.cursor_col = -1
                self.cursor_node = None
                self.current_line = None

                for line_num, line in enumerate(file):
                    line_content = line.rstrip('\n')

                    new_line = Node(None)
                    if not self.doc:
                        self.doc = new_line
                    else:
                        last_line = self.doc
                        while last_line.next:
                            last_line = last_line.next
                        last_line.next = new_line
                        new_line.prev = last_line

                    if line_content:
                        head = Node(line_content[0])
                        current_node = head
                        for char in line_content[1:]:
                            new_node = Node(char, prev=current_node)
                            current_node.next = new_node
                            current_node = new_node
                        new_line.data = head

                if self.doc:
                    self.goto(0, 0)

            print(f"Document loaded successfully from {filename}")
            return True

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except PermissionError:
            print(f"Error: No permission to read '{filename}'")
        except UnicodeDecodeError:
            print(f"Error: Could not decode file '{filename}' (try different encoding)")
        except Exception as e:
            print(f"Error loading file: {e}")
        return False

    def undo(self):
        '''
        Undo the most recent command and restore the previous state
        '''
        if not self.undo_stack:
            print("Nothing to undo")
            return

        current_state = {
            'doc': copy.deepcopy(self.doc),
            'cursor_row': self.cursor_row,
            'cursor_col': self.cursor_col,
            'cursor_node': self.cursor_node,
            'current_line': self.current_line
        }
        self.redo_stack.append(current_state)

        self._suppress_state_save = True
        previous_state = self.undo_stack.pop()
        self.doc = copy.deepcopy(previous_state['doc'])
        self.cursor_row = previous_state['cursor_row']
        self.cursor_col = previous_state['cursor_col']
        self.current_line = previous_state['current_line']
        self.cursor_node = previous_state['cursor_node']
        self._suppress_state_save = False

    def redo(self):
        '''
        Redo the most recent undone command and restore the next state
        '''
        if not self.redo_stack:
            print("Nothing to redo")
            return

        current_state = {
            'doc': copy.deepcopy(self.doc),
            'cursor_row': self.cursor_row,
            'cursor_col': self.cursor_col,
            'cursor_node': self.cursor_node,
            'current_line': self.current_line
        }
        self.undo_stack.append(current_state)
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack.pop(0)

        self._suppress_state_save = True
        next_state = self.redo_stack.pop()
        self.doc = copy.deepcopy(next_state['doc'])
        self.cursor_row = next_state['cursor_row']
        self.cursor_col = next_state['cursor_col']
        self.current_line = next_state['current_line']
        self.cursor_node = next_state['cursor_node']
        self._suppress_state_save = False


def main():
    editor = TextEditor()
    print("Welcome to DS Text Editor")
    print("Enter commands at the prompt")

    while True:
        command = input(">> ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "goto":
            if len(command) != 3:
                print("Usage: goto row col")
                continue
            try:
                row = int(command[1])
                col = int(command[2])
                editor.goto(row, col)
            except ValueError:
                print("Row and col must be integers")

        elif cmd == "forward":
            editor.forward()

        elif cmd == "back":
            editor.back()

        elif cmd == "home":
            editor.home()

        elif cmd == "end":
            editor.end()

        elif cmd == "insert":
            if len(command) < 2:
                print("Usage: insert string")
                continue
            string = ' '.join(command[1:])
            editor.insert(string)

        elif cmd == "delete":
            if len(command) != 2:
                print("Usage: delete num")
                continue
            try:
                num = int(command[1])
                editor.delete(num)
            except ValueError:
                print("num must be an integer")

        elif cmd == "countcharacters":
            print(editor.countCharacters())

        elif cmd == "countlines":
            print(editor.countLines())

        elif cmd == "printdoc":
            editor.printDoc()

        elif cmd == "save":
            if len(command) != 2:
                print("Usage: save filename")
                continue
            filename = command[1]
            editor.save(filename)

        elif cmd == "load":
            if len(command) != 2:
                print("Usage: load filename")
                continue
            filename = command[1]
            editor.load(filename)

        elif cmd == "undo":
            editor.undo()

        elif cmd == "redo":
            editor.redo()

        elif cmd == "quit":
            break

        else:
            print("Unknown command")


if __name__ == '__main__':
    main()