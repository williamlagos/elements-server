#
# This file is part of Coronae project.
# 
# Copyright (C) 2009-2012 William Oliveira de Lagos <william.lagos1@gmail.com>
#
# Coronae is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coronae is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Coronae.  If not, see <http://www.gnu.org/licenses/>.
#

import os,sys,json
from structure import Node,Tree,AVLTree
from elements import Element

class Nodes():
	def __init__(self):
		self.tree = AVLTree(Element('/','Coronae'))
		self.root = self.tree.root
		self.elements = None
	def elements_depth(self):
		return self.tree.total_height
	def prepare_elements(self,filename):
		f = open(filename)
		e = json.load(f)
		f.close()
		self.elements = e['Elements']
		for t,n in self.elements.items(): 
			self.tree.add(Element(t,n))
	def create_element(self,gname):
		try:
			self.conf.read("../config/zkn.cfg")
			file = open("../config/zkn.cfg","w")
			self.conf.set("Creation",gname[:4],gname)
			self.conf.write(file)
			os.mkdir(gname)
		except NoSectionError, e:
			print "Problems with zkn.cfg. Check the file."
			sys.exit(1)
		except OSError, e:
			print "Folder %s exists. Your game may have already been created."%(gname)
		finally:
			file.close()
	def enable_some(self,object):
		node = self.search(object)
		sys.path.append(node.get_item().get_path())
	def enable_all(self):
		self.zhockon_all_nodes(self.root)
	def enable_all_nodes(self,node):
		if(node != None):
			sys.path.append(node.get_item().get_path())
			self.zhockon_all_nodes(node.from_left())
			self.zhockon_all_nodes(node.from_right())
	def disable_some(self,name):
		cont = len(sys.path)-1
		spath = os.path.abspath(name)
		while cont != self.cnt:
			if(spath == sys.path[cont]):
				sys.path[cont] = ""
			cont -= 1
