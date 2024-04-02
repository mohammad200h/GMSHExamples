
import gmsh

def get_rectangle(center = [0,0],length = 3.0, width = 3.0,mesh_size=1):

  # Define the coordinates of the square
  x_min = center[0] - length / 2
  x_max = center[0] + length / 2
  y_min = center[1] - width / 2
  y_max = center[1] + width / 2

  # Define the points
  p1 = gmsh.model.geo.addPoint(x_min, y_min, 0 , mesh_size)
  p2 = gmsh.model.geo.addPoint(x_max, y_min, 0 , mesh_size)
  p3 = gmsh.model.geo.addPoint(x_max, y_max, 0 , mesh_size)
  p4 = gmsh.model.geo.addPoint(x_min, y_max, 0 , mesh_size)

  # Define the lines
  l1 = gmsh.model.geo.addLine(p1, p2)
  l2 = gmsh.model.geo.addLine(p2, p3)
  l3 = gmsh.model.geo.addLine(p3, p4)
  l4 = gmsh.model.geo.addLine(p4, p1)

  # Define the loop
  loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])


  return loop

def main():

  # Initialize Gmsh
  gmsh.initialize()

  # Create a new model
  gmsh.model.add("Surface")


  c1 = get_rectangle()

  surface = gmsh.model.geo.addPlaneSurface([c1])

  # Synchronize the geometry
  gmsh.model.geo.synchronize()
  # generate mesh
  gmsh.model.mesh.generate(2)

  # Save the mesh
  gmsh.write("surface_example.msh")

  # Finalize GMSH
  gmsh.finalize()



if __name__== "__main__":
   main()

if __name__ == "__main__":
    main()