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
    main_button_y=30
    step_button_y=100
    legend_y=150
    line_y=150
    scale_y=80
    
    
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
        self.canvas.create_line(0, static_variables.line_y, static_variables.size_of_board , static_variables.line_y, width=static_variables.linewidth, fill= colours.edge_colour )
        self.edge_drawing_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_deleting_enabled=False
        self.v_list=[] #list for edges (is_on_click_vertex function)
        self.v_list_delete_edges=[] # list for deleting edges
        self.graph=graph()
        self.canvas.pack(side="top", fill="both", expand=True)
        self.create_buttons()
        self.deleted_vertex_indices=[] #my crappy solution to fix indexing for deleted stuff
        self.deleted_edge_indices=[]
        self.previously_coloured=False
    
    #---------------------------------------------------------------------------
    #buttons
    #---------------------------------------------------------------------------
    
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
            button.place(x=15+static_variables.size_of_board/(self.button_number)*i, y=static_variables().main_button_y )
    
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
        
        
    def vertices(self):
        self.v_list_delete_edges=[]
        self.vertex_drawing_enabled=True
        self.vertex_deleting_enabled=False
        self.v_list=[]
        self.edge_drawing_enabled=False
        self.canvas.bind("<Button-1>", self.vertex_callback)
        self.edge_deleting_enabled=False
        #self.graph.vertex_colour_reset(self)
        
    def colouring(self):
        if self.previously_coloured==True:
            self.colour_step_scale.destroy()
        self.previously_coloured=True
        self.v_list=[]
        self.graph.current_colour_step=0
        self.v_list_delete_edges=[]
        self.vertex_deleting_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
        self.edge_deleting_enabled=False
        if not(self.graph.vertex_list==[]):
            self.graph.create_adjacency_matrix()
            self.graph.colouring_greedy()
            self.graph.assign_colours(self.graph.colours)
            #self.execute_colouring() #this was for doing the full colouring at once
            #self.canvas.bind()
            self.legend=legend(self)
            for vertex in self.graph.vertex_list: #reset vertices to white
                vertex.set_colour(colours.vertex_empty_colour, "", self )
            #self.create_colour_step_button() #this was used previously before colour scale widges was introduced
            self.create_colour_step_scale()
        
        
    def create_colour_step_button(self):
        self.colour_step_button=Button(self.window, text="Step", bg=colours.normal_button_colour)
        self.colour_step_button['command'] = self.colour_step # function without variables
        self.colour_step_button.config(height=self.button_height, width=self.button_width)
        self.colour_step_button.place(x=15+static_variables.size_of_board/(self.button_number)*5, y=static_variables.step_button_y )
        #pdb.set_trace()
    def create_colour_step_scale(self):
        x_position_left=static_variables.size_of_board/2-self.graph.size*10
        x=IntVar() 
        self.colour_step_scale=Scale(self.window, variable=x, from_ = 0, to = self.graph.size, orient=HORIZONTAL, length= self.graph.size*20,command= self.scale_step, sliderlength=15, relief=SOLID )
        self.colour_step_scale.place(x=x_position_left, y=static_variables.scale_y )
        
        #self.colour_step_scale.pack(anchor=CENTER)  
        self.colour_step_scale.set(0)
        self.current_step_value=0
    def scale_step(self, number):
        added_steps=int(number)-self.current_step_value
        if added_steps>0:
            for i in range(added_steps):
                self.colour_step()
        elif added_steps<0:
            for i in range (int(number), self.current_step_value):
                vertex_index=self.graph.permutation[i]        
                self.graph.vertex_list[vertex_index].set_colour(colours.vertex_empty_colour ,"", self)
                
                self.graph.current_colour_step-=1
        self.current_step_value+=added_steps
        
        
    def reset(self):
        self.edge_deleting_enabled=False
        self.vertex_drawing_enabled=False
        self.edge_drawing_enabled=False
        self.canvas.delete("all")
        if self.previously_coloured==True:
            self.colour_step_scale.destroy()
            self.colour_step_button.destroy()
        #reset variables:
        self.edge_drawing_enabled=False
        self.vertex_drawing_enabled=False
        self.v_list=[] #list for edges (is_on_click_vertex function)
        self.graph=graph()
        self.canvas.create_line(0, static_variables.line_y, static_variables.size_of_board , static_variables.line_y, width=static_variables.linewidth, fill= colours.edge_colour )
        self.previously_coloured=False
        
    #---------------------------------------------------------------------------
    #mainloop
    #---------------------------------------------------------------------------
        
    def mainloop(self):
        self.window.mainloop()
    
    #---------------------------------------------------------------------------
    #vertex functions
    #---------------------------------------------------------------------------
    
    def vertex_callback(self, event): #vertex is drawn on point that was clicked on
        if self.vertex_drawing_enabled:
            if not self.check_too_close(self.graph, event.x, event.y):
                v=vertex(event.x, event.y, self)
                
                
    def check_too_close(self,graph, event_x, event_y):
        too_close=False
        if event_y<(static_variables.legend_y+2*0.03*static_variables.size_of_board): # second one is diameter of vertex
            too_close=True
        #check if too close to other vertices:
        for i in range(len(graph.vertex_list)):
            if (event_x-graph.vertex_list[i].x)**2+(event_y-graph.vertex_list[i].y)**2<=4*graph.vertex_list[i].size**2:
                too_close=True
        return too_close
                           
    def execute_colouring(self):
        
        colournames= self.graph.colournames
        for i in range(len(self.graph.vertex_list)):
            self.graph.vertex_list[i].set_colour(colournames[i],self.graph.colours[i], self)
            
    
    def colour_step(self):
        if self.graph.current_colour_step<len(self.graph.vertex_list):
            colournames=self.graph.colour_names       
            vertex_index=self.graph.permutation[self.graph.current_colour_step]        
            self.graph.vertex_list[vertex_index].set_colour(colournames[vertex_index],self.graph.colours[vertex_index], self)
            self.graph.current_colour_step+=1
      
        
class vertex:
    def __init__(self, x_coordinate, y_coordinate, board):
        self.index=0 #dummy value
        self.x=x_coordinate
        self.y=y_coordinate
        self.size=0.03*static_variables.size_of_board
        self.thickness=static_variables.linewidth
        self.outlinecolour= colours.vertex_outlinecolour
        self.colour=colours.vertex_empty_colour
        self.add_to_graph(board.graph)
        self.color_change=True
        self.id=self.draw_vertex(board)
        self.neighbourhood=[] # list containing all neighbours of v
        
    
    def add_to_graph(self, graph):
        self.index=len(graph.vertex_list)
        graph.vertex_list.append(self) 
        #new_matrix=zeros([len(graph.vertex_list), len(graph.vertex_list)])
        #new_matrix[len(graph.vertex_list)-1, len(graph.vertex_list)-1]= graph.adjacency_matrix
    
    def draw_vertex(self, board):
        oval=board.canvas.create_oval(self.x - self.size, self.y - self.size,
                                self.x + self.size, self.y + self.size, width=self.thickness,
                                outline=self.outlinecolour, fill="white")
        board.canvas.tag_bind(oval, "<Enter>" , lambda event=None : self.on_enter_vertex(board))
        board.canvas.tag_bind(oval, "<Leave>" , lambda event=None : self.on_leave_vertex(board))
        board.canvas.tag_bind(oval, "<ButtonPress-1>", lambda event=None : self.on_vertex_click(board))
        board.canvas.tag_lower(oval)
        self.text=board.canvas.create_text(self.x, self.y, text="")
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
        # if board.edge_deleting_enabled:
        #     if board.v_list_delete_edges==[]:
        #         board.v_list_delete_edges.append(self)
        #         board.canvas.itemconfigure(self.id, outline=colours.vertex_on_click_colour_delete)                  
        #     elif board.v_list_delete_edges[0]==self:
        #         board.v_list_delete_edges=[]
        #         board.canvas.itemconfig(self.id, outline=colours.vertex_outlinecolour)
        #     else: 
                
        #         if self.neighbourhood.__contains__(board.v_list_delete_edges[0]):
        #             for e in board.graph.edge_list:
        #                 if (e.v1==self and e.v2==board.v_list_delete_edges[0]) or (e.v2==self and e.v1==board.v_list_delete_edges[0]): 
        #                     e.delete(board)
        #             board.canvas.itemconfig(board.v_list_delete_edges[0].id, outline=colours.vertex_outlinecolour)

        #             board.v_list_delete_edges=[]
        if board.vertex_deleting_enabled:
            for e in board.graph.edge_list:
                if e.v1==self or e.v2==self:
                    e.delete(board)        
            board.canvas.delete(self.id)
            board.canvas.delete(self.text)
            board.graph.vertex_list.remove(self)
    def edge_drawn(self, board, v1):
        board.canvas.itemconfig(v1, colours.vertex_outlinecolour)
    
    def set_colour(self, colour, colournumber, board):
        board.canvas.itemconfigure(self.id, fill=colour)
        board.canvas.itemconfigure(self.text, text= str(colournumber))
        
    # def step_through_colours(self, board):
    #     print("hello")
        
        
class edge:
    def __init__(self, vertex1,vertex2, board):
        self.v1=vertex1
        self.v2=vertex2
        self.id=len(board.graph.edge_list)
        self.add_to_list(board.graph)
        
        self.draw_edge(board)
        
    def add_to_matrix(self, graph): #this will only be called in the colouring process
        
        graph.adjacency_matrix[graph.vertex_list.index(self.v1), graph.vertex_list.index(self.v2)]=1
        graph.adjacency_matrix[graph.vertex_list.index(self.v2), graph.vertex_list.index(self.v1)]=1
    
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
        self.edge_line=board.canvas.create_line(x1_coord, y1_coord , x2_coord, y2_coord, fill=colours.edge_colour, width=static_variables.linewidth)
        board.canvas.tag_bind(self.edge_line, "<Enter>" , lambda event=None : self.on_enter_edge(board))
        board.canvas.tag_bind(self.edge_line, "<Leave>" , lambda event=None : self.on_leave_edge(board))
        board.canvas.tag_bind(self.edge_line, "<ButtonPress-1>", lambda event=None : self.on_edge_click(board))
        
    def on_enter_edge(self, board):
        if board.edge_deleting_enabled:
            board.canvas.itemconfigure(self.edge_line, fill=colours.vertex_on_click_colour_delete)
    def on_leave_edge(self, board):
        
        if board.edge_deleting_enabled:
            board.canvas.itemconfigure(self.edge_line, fill=colours.vertex_outlinecolour)
    def on_edge_click(self, board):
        #pdb.set_trace()
        if board.edge_deleting_enabled: 
            self.delete(board)
    def delete(self, board):
        board.canvas.delete(self.edge_line)
        self.v1.neighbourhood.remove(self.v2)
        self.v2.neighbourhood.remove(self.v1)
        board.graph.edge_list.remove(self)
        #board.graph.adjacency_matrix=zeros(np.shape(board.graph.adjacency_matrix))
        del self
    
class graph:
    def __init__(self):
        self.vertex_list=[]
        self.edge_list=[]
        self.colours=np.zeros(0)
        self.size=len(self.vertex_list)
        self.current_colour_step=0
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
        self.permutation=sorted_indices
    
    
    # def vertex_colour_reset(self, board):
    #     for v in graph.vertex_list:
    #         board.canvas.itemconfigure(v.id, fill=colours.vertex_empty_colour )
    def assign_colours(self, colour_vector):
        number_of_colours=max(colour_vector)
        self.colour_names=[]
        self.cmap=plt.get_cmap("hsv", number_of_colours+1) #purely because the start of the colourmap is ugly
        #pdb.set_trace()
        for i in range (len(colour_vector)):
            #print("v" +str(i)+ " has colour " +str(self.colours[i]))
            c=mpl.colors.rgb2hex(self.cmap(colour_vector[i]))
            self.colour_names.append(c) 
        #return self.colour_names
class legend:
    def __init__(self, board):
        
        self.y=static_variables.legend_y
        self.circle_size=0.03*static_variables.size_of_board
        self.thickness=static_variables.linewidth
        self.outlinecolour=colours.edge_colour
        #board.canvas.create_rectangle()
        #pdb.set_trace()
        for i in range(max(board.graph.colours)):
            index=np.where(board.graph.colours==i+1)[0][0]
            self.create_circle(i+1,board.graph.colour_names[int(index)] , board)
    def create_circle(self, i, colour_name, board):
        x_centre=(3*i-1)*self.circle_size
        board.canvas.create_oval(x_centre - self.circle_size, self.y - self.circle_size,
                                x_centre + self.circle_size, self.y + self.circle_size, width=self.thickness,
                                outline=self.outlinecolour, fill=colour_name)
        
        board.canvas.create_text(x_centre, self.y, text=str(i))
        
my_board = board()
my_board.mainloop()

"""
next steps:
    implement other algorithms
    button placement other algorithms
    step by step /scale of colouring
"""
    