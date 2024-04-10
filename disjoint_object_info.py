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


# a surface belong to volume if they share a node index
def get_nodes_indexes_for_volume_given_volume_entity(entity):
  num_nodes,elements_index,elements_nodes_index = gmsh.model.mesh.getElements(entity[0],entity[1])
  #find unique node_indexs
  node_indexes = np.unique(elements_nodes_index)
  # print(f"unique::node_indexes::{node_indexes}")
  return node_indexes


def get_node_indexes_for_surface_given_surface_entity(entity):
  num_nodes,elements_index,elements_nodes_index = gmsh.model.mesh.getElements(entity[0],entity[1])
  #find unique node_indexs
  node_indexes = np.unique(elements_nodes_index)
  # print(f"unique::node_indexes::{node_indexes}")
  return node_indexes

def is_surface_part_of_volume(e_v,e_s):
  s_node_indexes = get_node_indexes_for_surface_given_surface_entity(e_s)
  v_node_indexes = get_nodes_indexes_for_volume_given_volume_entity(e_v)
  match = np.in1d(s_node_indexes, v_node_indexes)
  print(f"is_surface_part_of_volume::{match}")



# Initialize Gmsh
gmsh.initialize()

gmsh.open('disjoint_object.msh')

# https://fenicsproject.discourse.group/t/what-does-gmsh-model-getentities-dim-3-s-return-value-represent/12093/2
entities = gmsh.model.getEntities()
# print(f"gmsh.model.mesh::gmsh.model.getEntities()::{entities}")

# print(f"entites::point::{get_point_entities(entities)}")
# print(f"entites::curve::{get_curve_entities(entities)}")
# print(f"entites::surface::{get_surface_entities(entities)}")
# print(f"entites::volume::{get_volume_entities(entities)}")

boundaries = []
for e in get_volume_entities(entities):
  print(f"boundary::gmsh.model.getBoundary([{e}])::{gmsh.model.getBoundary([e])}")
  t  = (e,gmsh.model.getBoundary([e]))
  boundaries.append(t)

for e in get_volume_entities(entities):
  get_nodes_indexes_for_volume_given_volume_entity(e)


# for e in get_volume_entities(entities):
#   num_nodes,elements_index,elements_nodes_index = gmsh.model.mesh.getElements(e[0],e[1])
#   print(f"{e} :: elements_nodes_index:: ",elements_nodes_index)


for t in boundaries:
  print("\n\n")
  e_v = t[0]
  for e_s in t[1]:
    e_s = (e_s[0],abs(e_s[1]))
    is_surface_part_of_volume(e_v,e_s)



# Finalize Gmsh
gmsh.finalize()