class Stack:
    """Simple LIFO (Last In First Out) stack built on a Python list."""

    def __init__(self):
        self._items: list = []

    # ----- core stack operations -----
    def push(self, item):
        """Add item to the top (O(1))."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item (O(1))."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """True if the stack has no items."""
        return len(self._items) == 0

    def size(self):
        """Current number of items in the stack."""
        return len(self._items)



# Demonstration problem: reverse a string

def reverse_string(s: str) -> str:
    """Return s reversed by pushing each char then popping."""
    st = Stack()
    for ch in s:  # push every character
        st.push(ch)

    out_chars = []
    while not st.is_empty():  # pop produces reverse order
        out_chars.append(st.pop())
    return ''.join(out_chars)


if __name__ == "__main__":
    original = "Hello, my name is Mikhail and I study in BSBI!"
    print(f"{original} -> {reverse_string(original)}")
    # Output:  Hello, my name is Mikhail and I study in BSBI! -> !IBSB ni yduts I dna liahkiM si eman ym ,olleH
