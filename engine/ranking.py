#
# This file is part of elements project.
# 
# Copyright (C) 2009-2011 William Oliveira de Lagos <william.lagos@icloud.com>
#
# Elements is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Elements is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with elements.  If not, see <http://www.gnu.org/licenses/>.
#

import os,sys

class Node:
	def __init__(self,object):
		self.object = object
		self.father = None
		self.left = None
		self.right = None
	def to_father(self,node):
		self.father = node
	def to_left(self,node):
		self.left = node
	def to_right(self,node):
		self.right = node
	def from_father(self):
		return self.father
	def from_right(self):
		return self.right
	def from_left(self):
		return self.left
	def get_item(self):
		return self.object
	def set_item(self,item):
		self.object = item

class Tree:
	def __init__(self,object):
		self.cnt = 0
		self.root = Node(object)
	def get_root(self):
		return self.root
	def add(self,object):
		self.add_node(object,self.root)
		self.cnt += 1
	def add_node(self,object,target):
		if(target == None):
			node = Node(object)
			node.to_father(target)
			return node
		if(target.get_item().__cmp__(object) < 0):
			node = self.add_node(object,target.from_right())
			target.to_right(node)
		else:
			node = self.add_node(object,target.from_left())
			target.to_left(node)
		return target
	def count(self):
		return self.cnt
	def read(self):
		return self.read_nodes(self.root)
	def read_node(self,node):
		list = ""
		if(node != None):
			left = node.from_left(); right = node.from_right()
			list = node.get_item().get_path()+"\n"+self.read_node(left)+self.read_node(right)
		return list
	def search(self,object):
		return self.search_node(object,self.root)
	def search_node(self,object,target):
		if(object == None or target == None):
			return None
		comp = target.get_item().__cmp__(object)
		if(comp == 0):
			return target
		elif(comp > 0):
			return self.search_node(object,target.from_left())
		else:
			return self.search_node(object,target.from_right())
	def contains(self,object):
		node = self.search(object)
		return node != None

class AVLNode(Node):
	def __init__(self,object):
		Node.__init__(self,object)
		self.height = 0
		self.deltah = 0
	def delta_h(self,target,direction):
		if not target: 
			if direction: pass#self.father.from_right()
			else: pass #self.father.from_left()
			h = self.height+1
		else: h = target.height
		self.deltah = self.height-h
	def __str__(self):
		return 'Node with height %i and delta height %i' % (self.height,self.deltah)

class AVLTree(Tree):
	def __init__(self,object):
		Tree.__init__(self,object)
		self.root = AVLNode(object)
		self.height = 0
		self.depth = 0
		self.path = []
	def add(self,object):
		self.add_node(object,self.root,-1)
		self.cnt += 1
		if self.height > self.depth:
			self.depth = self.height
		self.height = 0
		self.path = []
	def add_node(self,object,target,direction):
		self.height += 1
		depthpath = len(self.path)
		if depthpath: last = self.path[len(self.path)-1]
		else: last = self.root
		if target: 
			self.path.append(target)
			if(target.get_item().__cmp__(object) < 0):
				node = self.add_node(object,target.from_right(),1)
				target.to_right(node)
			else:
				node = self.add_node(object,target.from_left(),0)
				target.to_left(node)
		else:
			node = AVLNode(object)
			node.height = self.height
			node.to_father(last)
			if direction: node.delta_h(last.from_right(),1)
			elif direction is -1: node.deltah = 0
			else: node.delta_h(last.from_left(),0)
			return node
		return target
	def width(self):
		pass
	def path(self,object):
		pass
	def rotate_left(self):
		pass
	def rotate_right(self):
		pass

class Module:
	pass

class Adapter(Module):
	pass

class Extensor(Module):
	pass

class Creator(Module):
	pass

# import os,sys,json
# from elements import Element

# class Nodes():
# 	def __init__(self):
# 		self.tree = AVLTree(Element('/','Coronae'))
# 		self.root = self.tree.root
# 		self.elements = None
# 	def elements_depth(self):
# 		return self.tree.total_height
# 	def prepare_elements(self,filename):
# 		f = open(filename)
# 		e = json.load(f)
# 		f.close()
# 		self.elements = e['Elements']
# 		for t,n in self.elements.items(): 
# 			self.tree.add(Element(t,n))
# 	def create_element(self,gname):
# 		try:
# 			self.conf.read("../config/zkn.cfg")
# 			file = open("../config/zkn.cfg","w")
# 			self.conf.set("Creation",gname[:4],gname)
# 			self.conf.write(file)
# 			os.mkdir(gname)
# 		# except NoSectionError, e:
# 			# print "Problems with zkn.cfg. Check the file."
# 			# sys.exit(1)
# 		except OSError:
# 			print("Folder %s exists. Your game may have already been created."%(gname))
# 		finally:
# 			file.close()
# 	def enable_some(self,object):
# 		node = self.search(object)
# 		sys.path.append(node.get_item().get_path())
# 	def enable_all(self):
# 		self.elements_all_nodes(self.root)
# 	def enable_all_nodes(self,node):
# 		if(node != None):
# 			sys.path.append(node.get_item().get_path())
# 			self.elements_all_nodes(node.from_left())
# 			self.elements_all_nodes(node.from_right())
# 	def disable_some(self,name):
# 		cont = len(sys.path)-1
# 		spath = os.path.abspath(name)
# 		while cont != self.cnt:
# 			if(spath == sys.path[cont]):
# 				sys.path[cont] = ""
# 			cont -= 1