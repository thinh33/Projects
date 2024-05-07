#Name: Thinh Tran
#EID: tpt446
import tkinter as tk
from tkinter import colorchooser, messagebox


WIDTH, HEIGHT = 500,500

# Queue class; you can use this for your search algorithms
class Queue(object):
  def __init__(self):
    self.queue = []

  # add an item to the end of the queue
  def enqueue(self, item):
    self.queue.append(item)

  # remove an item from the beginning of the queue
  def dequeue(self):
    return self.queue.pop(0)

  # checks the item at the top of the Queue
  def peek(self):
    return self.queue[0]

  # check if the queue is empty
  def is_empty(self):
    return len(self.queue) == 0

  # return the size of the queue
  def size(self):
    return len(self.queue)
  
class Node:
    #stores nodes for the graph
    def __init__(self,index,x,y,color):
          self.index = index
          self.color = color
          self.x = x
          self.y = y
          self.coord = (x,y)
          self.edges = []
          self.visited = False
          self.fill = False

    def add_edge(self, node_index):
          self.edges.append(node_index)

    def visit_and_set_color(self, color):
          self.visited = True
          self.color = color
          self.fill = True

class Graph:
    #keeps track of which colors are filled on the canvas
    def __init__(self,m,color):
            self.nodes = []
            x, y = 1, 1
            for i in range(m*m):
                new_node = Node(i,x,y,color)
                if y != 1:
                  new_node.add_edge(i-m)
                if x != 1:
                  new_node.add_edge(i-1)
                if y != m:
                  new_node.add_edge(i+m)
                if x != m:
                  new_node.add_edge(i+1)
                self.nodes.append(new_node)
                if x < m:
                    x += 1
                else:
                    y += 1
                    x = 1

            self.coord_index = [x.coord for x in self.nodes]

    def reset_visited(self):
            for i in range(len(self.nodes)):
                self.nodes[i].visited = False

    def reset_fill(self):
            for i in range(len(self.nodes)):
                self.nodes[i].fill = False

    def reset_color(self,color):
            for i in range(len(self.nodes)):
                self.nodes[i].color = color

    def bfs(self, start_index, color):
            # reset visited status
            self.reset_visited()

            frontier = Queue()

            frontier.enqueue(start_index)

            original_color = self.nodes[start_index].color

            while not frontier.is_empty():
                s = frontier.dequeue()
                if self.nodes[s].color == original_color:
                  self.nodes[s].visit_and_set_color(color)

                next_nodes = self.nodes[s].edges

                for node in next_nodes:
                    if not self.nodes[node].visited and self.nodes[node].color == original_color:
                      (self.nodes[node]).visited = True
                      frontier.enqueue(node)

class Paint:
    #GUI CLASS
    def __init__(self):
        #sets up window
        self.root = tk.Tk()

        self.root.geometry('550x555')
        self.root.title('Canvas')
        
        #sets default brush settings
        self.brush_size = 5
        self.brush_color = 'black'
        self.shape_fill = 'white'
        self.anchor1 = None
        self.anchor2 = None
        self.history = []
        self.clipboard = []
        self.shape_fill_toggle = False

        #creates canvas
        self.canvas = tk.Canvas(self.root, width=WIDTH,height=HEIGHT,bg='white')
        self.canvas.pack()


        #controls tool
        self.canvas.bind('<Shift-Button-1>', self.fill)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Control-Button-1>', self.anchor_points)
        self.canvas.bind('<Alt-Button-1>', self.cut)
        self.canvas.master.bind('<r>', self.rectangle)

        #creates graph
        self.graph = Graph(500, 'white')

        #setups buttons
        self.button_frame = tk.Frame(self.root)

        self.button_frame.columnconfigure(0, weight = 1)
        self.button_frame.columnconfigure(1, weight = 1)
        self.button_frame.columnconfigure(2, weight = 1)

        self.clear_button = tk.Button(self.button_frame, text='Clear', command = self.clear)
        self.clear_button.grid(row=0,column=0,sticky=tk.W + tk.E)

        self.bplus_button = tk.Button(self.button_frame, text='B+', command = self.bplus)
        self.bplus_button.grid(row=0,column=1,sticky=tk.W + tk.E)

        self.bminus_button = tk.Button(self.button_frame, text='B-', command = self.bminus)
        self.bminus_button.grid(row=0,column=2,sticky=tk.W + tk.E)

        self.color_button = tk.Button(self.button_frame, text='Change Color', command = self.change_color)
        self.color_button.grid(row=1,column=1,sticky=tk.W + tk.E)
        
        self.fill_button = tk.Button(self.button_frame, text='Shortcuts', command = self.shortcuts)
        self.fill_button.grid(row=1,column=0,sticky=tk.W + tk.E)
        
        self.shape_button = tk.Button(self.button_frame, text='Toggle Shape Fill', command = self.toggle_fill)
        self.shape_button.grid(row=1,column=2,sticky=tk.W + tk.E)
        
        self.button_frame.pack(fill='x')

        #setups menu
        self.menubar = tk.Menu(self.root)
        self.brushmenu = tk.Menu(self.menubar, tearoff = 0)
        self.colormenu = tk.Menu(self.menubar, tearoff = 0)
        self.anchor1menu = tk.Menu(self.menubar, tearoff = 0)
        self.anchor2menu = tk.Menu(self.menubar, tearoff = 0)
        self.shapefillmenu = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(menu=self.colormenu, label=f'Brush Size:{self.brush_size}')
        self.menubar.add_cascade(menu=self.brushmenu, label=f'Brush Color:{self.brush_color}')
        self.menubar.add_cascade(menu=self.anchor1menu, label=f'Anchor1:{self.anchor1}')
        self.menubar.add_cascade(menu=self.anchor2menu, label=f'Anchor2:{self.anchor2}')
        self.menubar.add_cascade(menu=self.shapefillmenu, label=f'Shape Fill:{self.shape_fill_toggle}')
        self.root.config(menu=self.menubar)

        #runs window
        self.root.mainloop()

    def paint(self, event):
        #controls paintbrush
        x,y = event.x, event.y
        self.canvas.create_rectangle(x,y,x,y, outline = self.brush_color, fill = self.brush_color, width = self.brush_size)
        

        #updates matrix of canvas
        left_corner = (x - self.brush_size // 2, y - self.brush_size // 2)
        index = self.graph.coord_index.index(left_corner)
      
        x = 1
        for _ in range(self.brush_size**2):
            self.graph.nodes[index].color = self.brush_color
            if x < self.brush_size :
              index += 1
              x += 1
            else:
              index += 500 - self.brush_size + 1
              x = 1

    def clear(self):
        #clears canvas
        self.canvas.delete('all')
        self.graph.reset_color('white')
        

    def bplus(self):
        #increases brush size by two
        if self.brush_size >= 1:
            self.brush_size += 2
            self.menubar.entryconfigure(1, label=f'Brush Size:{self.brush_size}')

    def bminus(self):
        #decreases brush size by two
        if self.brush_size > 1:
            self.brush_size -= 2
            self.menubar.entryconfigure(1, label=f'Brush Size:{self.brush_size}')

    def change_color(self):
        #changes color
        _, self.brush_color = colorchooser.askcolor(title="Choose A Color")
        self.menubar.entryconfigure(2, label=f'Brush Color:{self.brush_color}')

    def anchor_points(self, event):
        #sets anchor points for shapes
        if self.anchor1 is None:
            self.anchor1 = (event.x, event.y)
            self.menubar.entryconfigure(3, label=f'Anchor1:{self.anchor1}')
        elif self.anchor2 is None:
            self.anchor2 = (event.x, event.y)
            self.menubar.entryconfigure(4, label=f'Anchor2:{self.anchor2}')
            self.outline()
        else:
            self.anchor1, self.anchor2 = None, None
            self.menubar.entryconfigure(3, label=f'Anchor1:{self.anchor1}')
            self.menubar.entryconfigure(4, label=f'Anchor2:{self.anchor2}')
            self.reset()

    def outline(self):
        #creates visible outline for anchor points and keeps previous colors intact; can toggle to include fill in history
        left_corner = (min(self.anchor1[0],self.anchor2[0]), min(self.anchor1[1],self.anchor2[1]))
        m = abs(self.anchor1[0] - self.anchor2[0]) 
        n = abs(self.anchor1[1] - self.anchor2[1])
        index = self.graph.coord_index.index(left_corner) 
        x, y = 1, 1
        for _ in range(m * n):
            if x in [1,m] or y in [1,n]:
              self.history.append([index, self.graph.nodes[index].color])
            else:
              self.clipboard.append([index, self.graph.nodes[index].color])
            if x < m:
              index += 1
              x += 1
            else:
              index += 500 - m + 1
              y += 1
              x = 1
        for i in self.history:
            self.canvas.create_rectangle((self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y,self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y), fill = 'white', outline = "#ff0000", width = 1)
        # self.canvas.create_rectangle((self.anchor1[0],self.anchor1[1],self.anchor2[0],self.anchor2[1]), fill = 'white', outline = "#ff0000", width = 1)
        
    def reset(self):
        #resets outline
        for i in self.history:
            self.canvas.create_rectangle((self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y,self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y), fill = i[1], outline = i[1], width = 1)
        self.history = []
        self.clipboard = []

    def cut(self,event):
        index = self.graph.coord_index.index((event.x,event.y))
        shift = index - self.clipboard[0][0]

        for i in self.clipboard:
            self.graph.nodes[i[0]].color = 'white'
            self.canvas.create_rectangle((self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y,self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y), fill = 'white', outline = 'white', width = 1)
        
        for i in self.history:
            self.canvas.create_rectangle((self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y,self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y), fill = i[1], outline = i[1], width = 1)
        
        for i in range(len(self.clipboard)):     
            self.clipboard[i][0] += shift

        
        for i in self.clipboard:
            self.canvas.create_rectangle((self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y,self.graph.nodes[i[0]].x,self.graph.nodes[i[0]].y), fill = i[1], outline = i[1], width = 1)
            self.graph.nodes[i[0]].color = i[1]

        self.history = []
        self.clipboard = []
          
    def rectangle(self,event):
        #creates a rectangle using anchor points and resets them
        self.reset()
        self.canvas.create_rectangle((self.anchor1[0],self.anchor1[1],self.anchor2[0],self.anchor2[1]), fill = self.shape_fill, outline = self.brush_color, width = self.brush_size)
        
        #updates matrix of canvas
        left_corner = (min(self.anchor1[0],self.anchor2[0]) - self.brush_size // 2 , min(self.anchor1[1],self.anchor2[1]) - self.brush_size // 2)
        m = abs(self.anchor1[0] - self.anchor2[0]) + self.brush_size // 2 * 2
        n = abs(self.anchor1[1] - self.anchor2[1]) + self.brush_size // 2 * 2
        index = self.graph.coord_index.index(left_corner)
      
        x, y = 1, 1
        for _ in range(m * n):
            if self.shape_fill_toggle == False:
              if x in [1,m] or y in [1,n]:
                self.graph.nodes[index].color = self.brush_color
            else:
              self.graph.nodes[index].color = self.brush_color
            if x < m:
              index += 1
              x += 1
            else:
              index += 500 - m + 1
              y += 1
              x = 1

        self.anchor1, self.anchor2 = None, None
        self.menubar.entryconfigure(3, label=f'Anchor1:{self.anchor1}')
        self.menubar.entryconfigure(4, label=f'Anchor2:{self.anchor2}')

    def toggle_fill(self):
        #toggles fill on rectangle
        if self.shape_fill_toggle is not True:
            self.shape_fill = self.brush_color
            self.shape_fill_toggle = True
        else:
            self.shape_fill = 'white'
            self.shape_fill_toggle = False
        self.menubar.entryconfigure(5, label=f'Shape Fill:{self.shape_fill_toggle}')

    def shortcuts(self):
        #displays important shortcuts
        tk.messagebox.showinfo(title='Shortcuts', message='FILL: SHIFT+LEFT_CLICK \nAnchor Point: CTRL-LEFT-CLICK\nRectangle: R\nCUT: ALT+LEFT_CLICK')

    def fill(self,event):
        #flood fill function using BFS
        x,y = event.x,event.y

        start_index = self.graph.coord_index.index((x,y))

        self.graph.bfs(start_index, self.brush_color)

        for i in self.graph.nodes:
            if i.fill:
                self.canvas.create_rectangle((i.x,i.y,i.x,i.y), fill = self.brush_color, outline = self.brush_color, width = 1)

        self.graph.reset_fill()
  
Paint()