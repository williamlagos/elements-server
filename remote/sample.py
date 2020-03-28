#
# This file is part of Coronae project.
# 
# Copyright (C) 2009-2012 William Oliveira de Lagos <william.lagos@icloud.com>
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

from network.nodes import Node
from network.runtime import Runtime,Coronae
import sys,json

class NodeSample(Coronae):
	def get(self):
		#nodes = Nodes()
		#nodes.prepare_elements('objects.json')
		#self.write('<pre>'+self.to_json(nodes.elements)+' %i</pre>'%nodes.tree.depth)
		self.write('<pre>%s</pre>'%json.load(open('elements.json')))

def main(argv):
	runtime = Runtime([('/',NodeSample)])
	runtime.run()

if __name__ == "__main__": main(sys.argv)
