

# from elements.engine.ranking import Nodes
from elements.server import Runtime,Coronae
import sys,json

class NodeSample(Coronae):
	def get(self):
		# nodes = Nodes()
		# nodes.prepare_elements('objects.json')
		# self.write('<pre>'+self.to_json(nodes.elements)+' %i</pre>'%nodes.tree.depth)
		self.write('<pre>%s</pre>'%json.load(open('elements.json')))

def main(argv):
	runtime = Runtime([('/',NodeSample)])
	runtime.run()

if __name__ == "__main__": main(sys.argv)
