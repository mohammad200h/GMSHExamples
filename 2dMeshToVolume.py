import gmsh
import math

#https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/examples/api/remesh_stl.py?ref_type=heads

# Initialize Gmsh
gmsh.initialize()

# Merge the STL file
# gmsh.merge("object.stl")
gmsh.merge("shark_low_res.stl")


# get all surfaces
s = gmsh.model.getEntities(2)

# create a surface loop from all the surfaces
l = gmsh.model.geo.addSurfaceLoop([e[1] for e in s])

# add a volume bounded by that surface loop
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)


# Save the mesh
gmsh.write("shark.msh")

# Finalize Gmsh
gmsh.finalize()