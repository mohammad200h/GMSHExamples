import gmsh
import numpy as np

#https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/examples/api/adapt_mesh.py?ref_type=heads
#https://gitlab.onelab.info/gmsh/gmsh/blob/master/tutorials/python/x7.py

# Initialize Gmsh
gmsh.initialize()

gmsh.open('compatible_volume_example.msh')

node_indexes,points,_ = gmsh.model.mesh.getNodes()
# print(f"nodes::type::{type(nodes)}")
# nodes_shape = nodes.reshape(-1,3)
elements = gmsh.model.mesh.getElements()


# print(f"node_indexes::{node_indexes}")
# print(f"node_indexes::shape::{node_indexes.shape[0]}")
# print(f"points::{points}")
# print(f"elements::{elements}")

triangleElementType = gmsh.model.mesh.getElementType("triangle", 1)
# print(f"elementType::triangle::{triangleElementType}")
tetrahedronElementType = gmsh.model.mesh.getElementType("tetrahedron", 1)
# print(f"elementType::tetrahedron::{tetrahedronElementType}")



# get triangles
triangles_tags, evtags = gmsh.model.mesh.getElementsByType(triangleElementType)


# print(f"triangles_tags::{triangles_tags}")
# print(f"evtags::{evtags}")

# get tetrahedron
tetrahedron, evtags = gmsh.model.mesh.getElementsByType(tetrahedronElementType)

# print(f"tetrahedron::{tetrahedron}")
print(f"evtags::{evtags}")
elements_reshaped = evtags.reshape(-1,4)
print(f"elements_reshaped::{elements_reshaped}")

# Finalize Gmsh
gmsh.finalize()