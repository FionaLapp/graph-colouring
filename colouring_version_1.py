# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:18:23 2021

@author: Fiona
"""

from tkinter import *
import numpy as np
import pdb
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl

class static_variables:
    linewidth=3
    size_of_board = 700
    button_height=2
    button_width=10
    button_number=6
    
    
class colours:
    background_colour='#000000' #black
    active_button_colour="#22FF00" #light green
    vertex_outlinecolour= "#A1A1A1" #grey
    vertex_empty_colour="#FFFFFF" #white
    edge_colour="#A1A1A1" #grey
    normal_button_colour="#FFFFFF" #white
    vertex_on_click_colour="#22FF00" #light green
    vertex_on_click_colour_delete= "#f21000" #red


class board:
    def __init__(self):
        self.window=Tk()
        self.window.title("Graph colouring")
        self.button_height=static_variables.button_height
        self.button_width=static_variables.button_width
        self.canvas = Canvas(self.window, width=static_variables.size_of_board, height=static_variables.size_of_board, bg=colours.background_colour)
        self.button_number=static_variables.button_number
        self.edge_drawing_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_deleting_enabled=False
        self.v_list=[] #list for edges (is_on_click_vertex function)
        self.v_list_delete_edges=[] # list for deleting edges
        self.graph=graph()
        # self.edge_button = Button(self.window, text ="edge", command = self.edges)
        # self.edge_button.place(x=size_of_board/(self.button_number+2)*1, y=10)
        # self.edge_button.config(height=self.button_height, width=self.button_width)
        
        # self.vertex_button = Button(self.window, text ="vertex", command = self.vertices)
        # self.vertex_button.place(x=size_of_board/(self.button_number+2)*2, y=10)
        # self.vertex_button.config(height=self.button_height, width=self.button_width)
        
        # self.colouring_button = Button(self.window, text ="colouring", command = self.colouring)
        # self.colouring_button.place(x=size_of_board/(self.button_number+2)*3, y=10)
        # self.colouring_button.config(height=self.button_height, width=self.button_width)
        
        # self.reset_button = Button(self.window, text ="reset", command = self.reset)
        # self.reset_button.place(x=size_of_board/(self.button_number+2)*4, y=10)
        # self.reset_button.config(height=self.button_height, width=self.button_width)
        
        self.canvas.pack(side="top", fill="both", expand=True)
        self.create_buttons()
    
    def custom_button(self, name):
        if name == "draw edge":
            self.edges()
        elif name == "draw vertex":
            self.vertices()
        elif name=="colouring":
            self.colouring()
        elif name == "delete edge":
            self.delete_edges()
        elif name== "delete vertex":
            self.delete_vertex()
        else:
            self.reset()
            
    def create_buttons(self):
        button_names= ["reset", "draw vertex", "delete vertex", "draw edge", "delete edge",  "colouring"] #this needs to have as many elements as buttonnumber in static class
        for i, name in enumerate(button_names, 0):
            
            button = Radiobutton(self.window, text=name, bg=colours.normal_button_colour, value=i)  # assign variable and value
            button['indicatoron'] = 0
            button['selectcolor'] = colours.active_button_colour # color after selection

            button['command'] = lambda arg=name:self.custom_button(arg) # function without variables
            button.config(height=self.button_height, width=self.button_width)
            button.place(x=static_variables.size_of_board/(self.button_number)*i, y=15)
    def delete_edges(self):
        self.v_list=[]
        self.edge_deleting_enabled=True
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
        self.vertex_deleting_enabled=False
    
    def delete_vertex(self):
        self.v_list=[]
        self.v_list_delete_edges=[]
        self.vertex_deleting_enabled=True
        self.edge_deleting_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
    
    def edges(self):
        self.v_list_delete_edges=[]
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=True
        self.edge_deleting_enabled=False
        self.vertex_deleting_enabled=False
        #self.canvas.bind("<Button-1>", self.edge_callback)
        
        
    def vertices(self):
        self.v_list_delete_edges=[]
        self.vertex_drawing_enabled=True
        self.vertex_deleting_enabled=False
        self.v_list=[]
        self.edge_drawing_enabled=False
        self.canvas.bind("<Button-1>", self.vertex_callback)
        self.edge_deleting_enabled=False
        
        
    def colouring(self):
        self.v_list=[]
        self.v_list_delete_edges=[]
        self.vertex_deleting_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
        self.edge_deleting_enabled=False
        if not(self.graph.vertex_list==[]):
            self.graph.create_adjacency_matrix()
            self.graph.colouring_greedy()
            self.execute_colouring()
            
        
        
    def reset(self):
        self.edge_deleting_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
        self.canvas.delete("all")
        #reset variables:
        self.edge_drawing_enabled=False
        self.vertex_drawing_enabled=False
        self.v_list=[] #list for edges (is_on_click_vertex function)
        self.graph=graph()
        
        
    def mainloop(self):
        self.window.mainloop()

    def vertex_callback(self, event): #vertex is drawn on point that was clicked on
        if self.vertex_drawing_enabled:

            if not self.check_too_close(self.graph, event.x, event.y):
                v=vertex(event.x, event.y, self)
                v.add_to_graph(self.graph)
                #v.draw_vertex(self)
    def check_too_close(self,graph, event_x, event_y):
        too_close=False
        #check if too close to other vertices:
        for i in range(len(graph.vertex_list)):
            if (event_x-graph.vertex_list[i].x)**2+(event_y-graph.vertex_list[i].y)**2<=4*graph.vertex_list[i].size**2:
                too_close=True
        #check if too close to edges:
            
        return too_close
            
    def edge_callback(self, event):
        if self.edge_drawing_enabled:
            self.is_click_on_vertex(event.x, event.y, self.graph)
    
    def is_click_on_vertex(self, x_click, y_click, graph):
        if self.v_list==[]:
            for vertex in graph.vertex_list:
                rad_squared=(x_click-vertex.x)**2+ (y_click-vertex.y)**2
                if rad_squared<=vertex.size**2:
                    self.v_list.append(vertex)
                    self.canvas.itemconfig(vertex, fill='blue')
                    
        else:
            for vertex in graph.vertex_list:
                rad_squared=(x_click-vertex.x)**2+ (y_click-vertex.y)**2
                if rad_squared<=vertex.size**2:
                    
                    e=edge(self.v_list[0], vertex, self)

                    self.v_list=[]
                    
    def execute_colouring(self):
        colournames=self.graph.assign_colours(self.graph.colours)
        for i in range(len(self.graph.vertex_list)):
            self.graph.vertex_list[i].set_colour(colournames[i], self)
    
            
            
    
        
        
class vertex:
    def __init__(self, x_coordinate, y_coordinate, board):
        self.index=0 #dummy value
        self.x=x_coordinate
        self.y=y_coordinate
        self.size=0.03*static_variables.size_of_board
        self.thickness=static_variables.linewidth
        self.outlinecolour= colours.vertex_outlinecolour
        self.colour=colours.vertex_empty_colour
        #self.circle_object=self.draw_vertex(board)
        self.board=board
        self.color_change=True
        self.id=self.draw_vertex(board)
        self.neighbourhood=[] # list containing all neighbours of v
        
        #print(board.canvas.itemcget(self.id, "outline"))
        #board.canvas.lower(self.circle_object)
        #board.canvas.tag_lower(self.circle_object)
        #self.circle_object.lower()
        
    
    def add_to_graph(self, graph):
        self.index=len(graph.vertex_list)
        graph.vertex_list.append(self) 
    
    def draw_vertex(self, board):
        oval=board.canvas.create_oval(self.x - self.size, self.y - self.size,
                                self.x + self.size, self.y + self.size, width=self.thickness,
                                outline=self.outlinecolour, fill="white")
        board.canvas.tag_bind(oval, "<Enter>" , lambda event=None : self.on_enter_vertex(board))
        board.canvas.tag_bind(oval, "<Leave>" , lambda event=None : self.on_leave_vertex(board))
        board.canvas.tag_bind(oval, "<ButtonPress-1>", lambda event=None : self.on_vertex_click(board))
        board.canvas.tag_lower(oval)
        return oval
    def on_enter_vertex(self, board):
        if board.edge_drawing_enabled:
            board.canvas.itemconfigure(self.id, outline=colours.vertex_on_click_colour)
        elif board.edge_deleting_enabled or board.vertex_deleting_enabled:
            board.canvas.itemconfigure(self.id, outline=colours.vertex_on_click_colour_delete)
    def on_leave_vertex(self, board):
        if board.edge_drawing_enabled and (board.v_list==[] or board.v_list[0]!=self):
            board.canvas.itemconfigure(self.id, outline=colours.vertex_outlinecolour)
        elif board.edge_deleting_enabled and (board.v_list_delete_edges==[] or board.v_list_delete_edges[0]!=self):
            board.canvas.itemconfigure(self.id, outline=colours.vertex_outlinecolour)
        elif board.vertex_deleting_enabled:
            board.canvas.itemconfigure(self.id, outline=colours.vertex_outlinecolour)
            
    def on_vertex_click(self, board):
        if board.edge_drawing_enabled:

            if board.v_list==[]:
                board.v_list.append(self)
                board.canvas.itemconfigure(self.id, outline=colours.vertex_on_click_colour)
                    
            elif board.v_list[0]==self:
                board.v_list=[]
                board.canvas.itemconfig(self.id, outline=colours.vertex_outlinecolour)
            else: 
                
                if not self.neighbourhood.__contains__(board.v_list[0]):
                    edge(board.v_list[0], self, board)
                    board.canvas.itemconfig(board.v_list[0].id, outline=colours.vertex_outlinecolour)
                    board.v_list[0].neighbourhood.append(self)
                    self.neighbourhood.append(board.v_list[0])
                    board.v_list=[]
        if board.edge_deleting_enabled:
            if board.v_list_delete_edges==[]:
                board.v_list_delete_edges.append(self)
                board.canvas.itemconfigure(self.id, outline=colours.vertex_on_click_colour_delete)
                    
            elif board.v_list_delete_edges[0]==self:
                board.v_list_delete_edges=[]
                board.canvas.itemconfig(self.id, outline=colours.vertex_outlinecolour)
            else: 
                
                if self.neighbourhood.__contains__(board.v_list_delete_edges[0]):
                    for e in board.graph.edge_list:
                        if (e.v1==self and e.v2==board.v_list_delete_edges[0]) or (e.v2==self and e.v1==board.v_list_delete_edges[0]): 
                            board.canvas.delete(e.edge_line)
                            board.graph.edge_list.remove(e)
                    board.canvas.itemconfig(board.v_list_delete_edges[0].id, outline=colours.vertex_outlinecolour)
                    board.v_list_delete_edges[0].neighbourhood.remove(self)
                    self.neighbourhood.remove(board.v_list_delete_edges[0])
                    board.v_list_delete_edges=[]
        if board.vertex_deleting_enabled:
            for e in board.graph.edge_list:
                if e.v1==self or e.v2==self:
                    board.canvas.delete(e.edge_line)
                    board.graph.edge_list.remove(e)
            board.canvas.delete(self.id)
            board.graph.vertex_list.remove(self)
    def edge_drawn(self, board, v1):
        board.canvas.itemconfig(v1, colours.vertex_outlinecolour)
    
    def set_colour(self, colour, board):
        board.canvas.itemconfigure(self.id, fill=colour)

        

        
class edge():
    def __init__(self, vertex1,vertex2, board):
        self.v1=vertex1
        self.v2=vertex2
        self.add_to_list(board.graph)
        self.edge_line=self.draw_edge(board)
        board.canvas.tag_bind(self.edge_line, "<Enter>" , lambda event=None : self.on_enter_edge(board))
        board.canvas.tag_bind(self.edge_line, "<Leave>" , lambda event=None : self.on_leave_edge(board))
        board.canvas.tag_bind(self.edge_line, "<ButtonPress-1>", lambda event=None : self.on_edge_click(board))
        
        
        
    def add_to_matrix(self, graph): #this will only be called in the colouring process
        graph.adjacency_matrix[self.v1.index, self.v2.index]=1
        graph.adjacency_matrix[self.v2.index, self.v1.index]=1
    
    def add_to_list(self, graph): #this is called for every edge immediately upon creation
        graph.edge_list.append(self)
        
    def draw_edge(self, board):
        norm_factor=((self.v1.x-self.v2.x)**2+(self.v1.y-self.v2.y)**2)**-0.5 #one over length of line, to normalise
        x_dir=norm_factor*(self.v2.x-self.v1.x)*self.v1.size #length to be added or subtracted in x direction (vectorcomponent, normalised, multiplied by vertex radius)
        y_dir=norm_factor*(self.v2.y-self.v1.y)*self.v1.size #same for y
        x1_coord=x_dir+self.v1.x
        y1_coord=y_dir+self.v1.y
        x2_coord=-x_dir+self.v2.x
        y2_coord=-y_dir+self.v2.y
        return board.canvas.create_line(x1_coord, y1_coord , x2_coord, y2_coord, fill=colours.edge_colour, width=static_variables.linewidth)
    def on_enter_edge(self, board):
        if board.edge_deleting_enabled:
            board.canvas.itemconfigure(self.edge_line, fill=colours.vertex_on_click_colour_delete)
    def on_leave_edge(self, board):
        
        if board.edge_deleting_enabled:
            board.canvas.itemconfigure(self.edge_line, fill=colours.vertex_outlinecolour)
    def on_edge_click(self, board):
        if board.edge_deleting_enabled: 
            board.canvas.delete(self.edge_line)
            board.graph.edge_list.remove(self)
        
        
class graph:
    def __init__(self):
        self.vertex_list=[]
        self.edge_list=[]
        self.colours=np.zeros(0)
        self.size=len(self.vertex_list)
    def create_adjacency_matrix(self): #this will only be called in the colouring process
        self.size=len(self.vertex_list)
        self.adjacency_matrix=np.zeros([self.size, self.size])
        for edge in self.edge_list:
            edge.add_to_matrix(self)
    def colouring_greedy(self):
        self.colours=np.zeros(self.size, dtype=int)
        vertex_degrees=sum(self.adjacency_matrix,0).astype(int)#a vector of degrees of all vertices (in order)
        sorted_indices=np.argsort(vertex_degrees)[::-1]
        
        #current_vertex_index=sorted_indices[0]
        for i in range(len(self.adjacency_matrix)):
            need_colour=True
            current_vertex_index=sorted_indices[i]
            current_colour=1
            while need_colour:
                #pdb.set_trace()
                if  np.dot((self.colours==current_colour).astype(int),self.adjacency_matrix[current_vertex_index, :].astype(int))==0:
                    need_colour=False
                    #current_colour=i
                else:
                    current_colour+=1
            self.colours[current_vertex_index]=current_colour 
            #current_vertex_index=sorted_indices[i+1] 
        
    def assign_colours(self, colour_vector):
        number_of_colours=max(colour_vector)
        self.colour_names=[]
        cmap=plt.get_cmap("gist_ncar", number_of_colours+3) #purely because the start of the colourmap is ugly
        #pdb.set_trace()
        for i in range (len(colour_vector)):
            print("v" +str(i)+ " has colour " +str(self.colours[i]))
            c=mpl.colors.rgb2hex(cmap(colour_vector[i]))
            self.colour_names.append(c)   
        return self.colour_names
        
        

        
my_board = board()
my_board.mainloop()
