from collections import UserList


class Stack(UserList):

    def __init__(self):
        super(Stack, self).__init__()


    def push (self, item):
        self.data.append(item)

    def pop(self):
        if len(self.data) == 0:
            return None
        else:
            return self.data.pop(-1)

    def top(self):
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

