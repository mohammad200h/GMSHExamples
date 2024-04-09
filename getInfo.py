import gmsh
from collections import Counter
import numpy as np

#https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/examples/api/adapt_mesh.py?ref_type=heads
#https://gitlab.onelab.info/gmsh/gmsh/blob/master/tutorials/python/x7.py

def get_maximum_occurrence(surfaces_index):
    # https://www.geeksforgeeks.org/python-count-occurrences-element-list/
    d = Counter(surfaces_index)
    max_occurrence = 0
    for s in surfaces_index:
      occ = d[s]
      if occ>max_occurrence:
        max_occurrence = occ

    return max_occurrence


def get_point_entities(entities):
  e_point = []
  for e in entities:
    if e[0]==0:
      e_point.append(e)

  return e_point

def get_curve_entities(entities):
  e_curve = []
  for e in entities:
    if e[0]==1:
      e_curve.append(e)

  return e_curve

def get_surface_entities(entities):
  e_surface = []
  for e in entities:
    if e[0]==2:
      e_surface.append(e)

  return e_surface

def get_volume_entities(entities):
  e_volume = []
  for e in entities:
    if e[0]==3:
      e_volume.append(e)

  return e_volume

def get_boundry_entities_for_volumes(entities):
  e_volumes = get_volume_entities(entities)
  e_surface = []

  for e_v in e_volumes:
    e_surface += gmsh.model.getBoundary([e_v])
  return e_surface

def is_there_a_shared_surface(entities):
  e_surface = get_boundry_entities_for_volumes(entities)
  surface = []
  for e in e_surface:
    # shared surface will be repeated but one will have opposite sign
    surface.append(abs(e[1]))

  occ = get_maximum_occurrence(surface)
  print(f"occ::{occ}")

  if occ>1:
     return True

  return False

# Initialize Gmsh
gmsh.initialize()

gmsh.open('cube_ascii_41.msh')

# https://fenicsproject.discourse.group/t/what-does-gmsh-model-getentities-dim-3-s-return-value-represent/12093/2
entities = gmsh.model.getEntities()
# print(f"gmsh.model.mesh::gmsh.model.getEntities()::{entities}")

print(f"entites::point::{get_point_entities(entities)}")
print(f"entites::curve::{get_curve_entities(entities)}")
print(f"entites::surface::{get_surface_entities(entities)}")
print(f"entites::volume::{get_volume_entities(entities)}")

for e in get_volume_entities(entities):
    print(f"boundary::gmsh.model.getBoundary([{e}])::{gmsh.model.getBoundary([e])}")

is_joint = is_there_a_shared_surface(entities)

print(f"is_joint::{is_joint}")

# node_indexes,points,_ = gmsh.model.mesh.getNodes(3,1)
# print(f"nodes::type::{type(nodes)}")
# nodes_shape = nodes.reshape(-1,3)
num_nodes,elements_index,elements_nodes_index = gmsh.model.mesh.getElements(3,1)


# print(f"node_indexes::{node_indexes}")
# print(f"node_indexes::shape::{node_indexes.shape[0]}")
# print(f"points::{points}")
print(f"num_nodes::{num_nodes}")
print(f"elements_index::{elements_index}")
print(f"elements_nodes_index::{np.array(elements_nodes_index).reshape(-1,num_nodes[0])}")


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
# print(f"evtags::{evtags}")
# elements_reshaped = evtags.reshape(-1,4)
# print(f"elements_reshaped::{elements_reshaped}")

# Finalize Gmsh
gmsh.finalize()