import xmltodict
import dicttoxml
import code
import glob
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import sys, os
import lxml.etree as etree

hasComments = False;
hasBranchpoints = False;
#Use sys.argv to accept a path wich will be globbed

if len(sys.argv) < 3:
	print '-------------------------------'
	print 'wk_skeleton_merger, written by Michael Morehead, Nathan Spencer, & Anna Whelan.'
	print 'Usage: python wk_skeleton_merger.py [directory_to_skeletons] [output_file_name]'
	print 'Example: python wk_skeleton_merger.py testset/ output.nml'
	print 'Warning: not enough parameters'
	print '-------------------------------'
	sys.exit()

directory_skeletons = sys.argv[1]
file_to_write = sys.argv[2]
files_to_merge = glob.glob(directory_skeletons + '/*.nml')

things = Element('things')



nodeCount = 0
thingCount = 0
for ii, file in enumerate(files_to_merge):
	thingCount += 1

	with open(file) as fd:
    		doc = xmltodict.parse(fd.read())
	

	if ii == 0:
		parameters = SubElement(things, 'parameters')
		SubElement(parameters, 'experiment', {'name ':doc['things']['parameters']['experiment']['@name']})
		scale = SubElement(parameters, 'scale' , {'x':doc['things']['parameters']['scale']['@x'], 
							'y':doc['things']['parameters']['scale']['@y'],
							'z':doc['things']['parameters']['scale']['@z']})
		offset = SubElement(parameters, 'offset' ,{'x':doc['things']['parameters']['offset']['@x'], 
							'y':doc['things']['parameters']['offset']['@y'],
							'z':doc['things']['parameters']['offset']['@z']})
		time_ms = SubElement(parameters,'time', {'ms':doc['things']['parameters']['time']['@ms']})
		activeNode_id = SubElement(parameters , 'activeNode', {'id':doc['things']['parameters']['activeNode']['@id']})
		editPosition = SubElement(parameters, 'editPositioin' ,{'x':doc['things']['parameters']['editPosition']['@x'], 
							'y':doc['things']['parameters']['editPosition']['@y'],
							'z':doc['things']['parameters']['editPosition']['@z']})
		zoomlevel_zoom = SubElement(parameters, 'zoomlevel', {'zoom':doc['things']['parameters']['zoomLevel']['@zoom']})
	if 'branchpoint' in doc['things'].keys() and doc['things']['branchpoints'].keys():
		hasBranchpoints = True;
	print file
	

	if  not doc['things']['comments'] == None:
		hasComments = True;

	thing = SubElement(things, 'thing', {'id':str(thingCount),
					'color.r':doc['things']['thing']['@color.r'],
					'color.g':doc['things']['thing']['@color.g'],
					'color.b':doc['things']['thing']['@color.b'],
					'color.a':doc['things']['thing']['@color.a'],
					'name':'Tree' + str(thingCount)})
	nodes = SubElement(thing, 'nodes')
	lastNodeCount = nodeCount
	for jj, node in enumerate(doc['things']['thing']['nodes']['node']):
		
		
			
		node = SubElement(nodes, 'node', {'id':str(int(node['@id']) + lastNodeCount),
					'radius':node['@radius'],
					'x':node['@x'],		
					'y':node['@y'],	
					'z':node['@z'],	
					'rotX':node['@rotX'],
					'rotY':node['@rotY'],	
					'rotZ':node['@rotZ'],
					'inVp':node['@inVp'],			
					'inMag':node['@inMag'],
					'bitDepth':node['@bitDepth'],
					'interpolation':node['@interpolation'],
					'time':node['@time']})
		
		nodeCount = int(node.attrib['id']) + lastNodeCount
	print nodeCount
	edges = SubElement(thing, 'edges')
	for edge in doc['things']['thing']['edges']['edge']:
		edge = SubElement(edges, 'edge', {'source':(str(int(edge['@source']) + lastNodeCount)),
					'target':(str(int(edge['@target']) + lastNodeCount))})

	if hasBranchpoints:
		branchpoints = SubElement(thing, 'branchpoints')
		for branchpoint in doc['things']['branchpoints']['branchpoint']:
			branchpoint = SubElement(branchpoints, 'branchpoint', {'id':str(int(branchpoint['@id']) + lastNodeCount) })	
		
	if hasComments:
		comments = SubElement(thing, 'comments')
		for comment in doc['things']['comments']['comment']:	
			comment = SubElement(comments, 'comment', {'node':str(int(comment['@node']) + lastNodeCount), 
						'content':comment['@content']})

tree = ElementTree(things)
tree.write(file_to_write)
x = etree.parse(file_to_write)
f = open(file_to_write, "w")
f.write(etree.tostring(x, pretty_print = True))
f.close()


