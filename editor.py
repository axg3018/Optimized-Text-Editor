class Rope:
    "Constructor to initialize rope from a string or list of strings"
    def __init__(self, data="", parent=None):
        if  isinstance(data, list):
            if len(data) == 0:
                self.__init__()
            elif len(data) == 1:
                self.__init__(data[0], parent = parent)
            else:
                self.current = self
                idiv = len(data)//2 + (len(data)%2 > 0)
                self.left = Rope(data[:idiv], parent = self.current)
                self.right = Rope(data[idiv:], parent = self.current)
                self.parent = parent
                self.data = ""
                self.weight = len(self.data.join(data[:idiv]))
        else:
            self.left = None
            self.right = None
            self.data = data
            self.weight = len(data)
            self.parent = parent
            self.current = self
    """
    Concatenate 2 nodes into a single rope
    """
    def concat(self, node1, node2):
        self.left = node1
        self.right = node2
        self.weight = self.length(node1)
        return self
    
    """
    Calculate weight of a rope node
    """
    def length(self, node):
        if node.left is None and node.right is None:
            return len(node.data)
        elif node.left is not None and node.right is None:
            return self.length(node.left)
        elif node.left is None and node.right is not None:
            return self.length(node.right)
        else:
            return self.length(node.left) + self.length(node.right)

    """
    Search for an index in rope and return the node containing the index
    """
    def search(self, node, i):
        if node.weight <= i and node.right is not None:
            return self.search(node.right, i-node.weight)
        elif node.left is not None:
            return self.search(node.left, i)
        return node, i
    
    """
    split a rope leaf node into 2 nodes 
    """
    def split_node(self, node, i):
        arr = node.data
        node1 = Rope(arr[:i])
        node2 = Rope(arr[i:])

        return node1, node2

    """
    Balances the rope tree by sepearting target and leaf node, incase of split
    """
    def splits_helper(self, rootnode, index):
        target, i = self.search(rootnode, index)
        
        if target.parent is None:
            return self.split_node(target, i)
        else:
            if i!= 0:
                split1, split2 = self.split_node(target, i)
                target.left = split1
                target.right = split2
                target.weight = len(split1.data)
                rightnode = target.right
                target.right = None
                target.parent.weight -= len(rightnode.data)
                

    """
    split a rope tree into 2 ropes and rebalance using splits_helper
    """
    def splits(self, root, i):

        node, t = self.search(root, i)
        #print(node.data)
        node1 = Rope(node.data[0:t])
        node2 = Rope(node.data[t:])

        node.data = ""
        node.weight = len(node1.data)
        node.left = node1
        node.right = node2
        node1.parent = node
        node2.parent = node
        self.splits_helper(root, i)
        self.splits_helper(root, 0)

        
        return node1, node2
        
    """
    Delete a string between 2 indexes using splits and concat
    """
    def delete(self, i, j):
        node2, node3 = self.splits(self, j)

        
        node1, node2 = self.splits(self, i)

        final = Rope()
        final.concat(node1, node3)
        

        
        return final, self.getrope(node2, [])

    """
    Return a string between 2 indexes using splits and concat
    """
    def get(self, i, j):
        node2, node3 = self.splits(self, j)

        
        node1, node2 = self.splits(self, i)

        
        
        return self.getrope(node2, [])

        
    """
    Insert a string at an index using splits and concat
    """

    def insert(self, i, s):
        

        node1, node2 = self.splits(self, i)
        s_rope = Rope(s.split())
        self.concat(node1, s_rope)

        final = Rope()
        final.concat(self, node2)

        return final
    
    
    """
    Retreive string from a root node
    """
    def getrope(self, node, list_final):
        if node.left == None and node.right == None:
            if node.data != None:
                list_final.append(node.data)
        elif node.left == None:
            self.getrope(node.right, list_final)
        elif node.right == None:
            self.getrope(node.left, list_final)
        else:
            self.getrope(node.left, list_final)
            self.getrope(node.right, list_final)
        return "".join(list_final)

class SimpleEditor: 
    def __init__(self, document, undo_redo_limit=100):
        self.stack = [None]*undo_redo_limit
        self.stack[0] = document
        self.top = 0
        self.document = Rope(document.split())
        self.dictionary = set()
        self.undo_redo_limit = undo_redo_limit
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = ""


    def cut(self, i, j):
    	self.top = (self.top + 1)%self.undo_redo_limit
    	self.document, self.paste_text = self.document.delete(i, j)
    	self.stack[self.top] = self.document

    def copy(self, i, j):
        self.paste_text = self.document.get(i, j)
    def paste(self, i):
    	self.top = (self.top + 1)%self.undo_redo_limit
    	self.document = self.document.insert(i, self.paste_text)
    	#print(self.document)
    	self.stack[self.top] = self.document


    def get_text(self):
        return self.document.getrope(self.document, [])

    def misspellings(self):
        result = 0
        string = self.get_text().split(" ")
        for word in string:
            if word not in self.dictionary:
                result = result + 1
        return result

    def undo(self):
        if self.top > 0:
            self.top -= 1
        if self.top != None:
            self.document = self.stack[self.top]

    def redo(self):
        if self.top < self.undo_redo_limit - 1:
            self.top += 1
        if self.top != None:
            self.document = self.stack[self.top]
    def load(self):
        try:
            f = open("new.txt", "r")
        except:
            f = open("new.txt", "rw")
        self.document = Rope(f.read().replace("\n", "").split())
    def save(self):
        f = open("new.txt", "w")
        f.write(self.get_text())
import timeit
import time
class EditorBenchmarker:
    new_editor_case = """
from __main__ import SimpleEditor
s = SimpleEditor("{}")"""

    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, 3)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 3)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    editor_undo = """
for n in range({}):
    s.undo()"""

    editor_redo = """
for n in range({}):
    s.redo()"""

    editor_load = """
for n in range({}):
    s.load()"""

    editor_save = """
for n in range({}):
    s.save()"""



    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)
        self.editor_undo = self.editor_undo.format(N)
        self.editor_redo = self.editor_redo.format(N)
        self.editor_save = self.editor_save.format(N)
        self.editor_load = self.editor_load.format(N)

    def benchmark(self):
        for case in self.cases:
            print("Evaluating case: {}".format(case))
            new_editor = self.new_editor_case.format(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            undo_time = timeit.timeit(stmt=self.editor_undo,setup=new_editor,number=1)
            print("{} undo operations took {} s".format(self.N, undo_time))
            redo_time = timeit.timeit(stmt=self.editor_redo,setup=new_editor,number=1)
            print("{} redo operations took {} s".format(self.N, redo_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
            load_time = timeit.timeit(stmt=self.editor_load,setup=new_editor,number=1)
            print("{} load operations took {} s".format(self.N, load_time))
            save_time = timeit.timeit(stmt=self.editor_save,setup=new_editor,number=1)
            print("{} save operations took {} s".format(self.N, save_time))
            time.sleep(5)
            

if __name__ == "__main__":
    f = open("Pride.txt", "r", encoding='utf8')
    textfile = f.read().replace("\n", "")
    b = EditorBenchmarker(["hello friends", textfile], 100)
    b.benchmark()