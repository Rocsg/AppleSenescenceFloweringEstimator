
#!/usr/bin/env python

# This example shows how to generate and manipulate texture coordinates.
# A random cloud of points is generated and then triangulated with
# vtkDelaunay3D. Since these points do not have texture coordinates,
# we generate them with vtkTextureMapToCylinder.


x_end=512
y_end=512
z_end=512
z_last=230
y_last=260
size=511
z_end_irm=300


from skimage import io
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

bmpReader = vtk.vtkBMPReader()
bmpReader.SetFileName("/home/fernandr/Bureau/masonry.BMP")
atext = vtk.vtkTexture()
atext.SetInputConnection(bmpReader.GetOutputPort())
atext.InterpolateOn()
atext.SetBlendingMode(vtk.vtkTexture.VTK_TEXTURE_BLENDING_MODE_REPLACE)
sphere = vtk.vtkPointSource()
sphere.SetRadius(400)
sphere.SetCenter(300,300,300)
sphere.SetNumberOfPoints(25)
# Triangulate the points with vtkDelaunay3D. This generates a convex hull
# of tetrahedron.
delny = vtk.vtkDelaunay2D()
delny.SetInputConnection(sphere.GetOutputPort())
delny.SetTolerance(0.01)




data_D2 = io.imread('/home/fernandr/Bureau/Test/Visu/segD2.tif')
dataImporter5 = vtk.vtkImageImport()
data_string5 = data_D2.tostring()
dataImporter5.CopyImportVoidPointer(data_string5, len(data_string5))
dataImporter5.SetDataScalarTypeToUnsignedChar()
dataImporter5.SetNumberOfScalarComponents(1)
dataImporter5.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter5.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter5.SetDataSpacing( 1,1,1 )
surface5 = vtk.vtkMarchingCubes()
surface5.SetInputConnection( dataImporter5.GetOutputPort() )
surface5.ComputeNormalsOn()
surface5.SetValue( 0, 128.5 )      #########################"
geoBoneMapper5 = vtk.vtkPolyDataMapper()
geoBoneMapper5.SetInputConnection( surface5.GetOutputPort() )
geoBoneMapper5.ScalarVisibilityOff()
actorBone5 = vtk.vtkActor()
actorBone5.SetMapper( geoBoneMapper5 )

actorBone5.GetProperty().SetColor( 1.0, 1.0, 0.1 )   ##############""
actorBone5.GetProperty().SetOpacity( 0.55 )   ##############""
actorBone5.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
actorBone5.GetProperty().SetSpecular(0.4)   ##############""
actorBone5.GetProperty().SetDiffuseColor(1.0,1.0,0.1)   ##############""
actorBone5.GetProperty().SetDiffuse(0.4)   ##############""
actorBone5.GetProperty().SetAmbientColor(1.0,1.0,0.1)   ##############""
actorBone5.GetProperty().SetAmbient(0.18)   ##############""

# The triangulation has texture coordinates generated so we can map
# a texture onto it.





# Begin by generating 25 random points in the unit sphere.
sphere = vtk.vtkPointSource()
sphere.SetRadius(40)
sphere.SetCenter(300,300,300)
sphere.SetNumberOfPoints(25)

# Triangulate the points with vtkDelaunay3D. This generates a convex hull
# of tetrahedron.
delny = vtk.vtkDelaunay2D()
delny.SetInputConnection(sphere.GetOutputPort())
delny.SetTolerance(0.01)

# The triangulation has texture coordinates generated so we can map
# a texture onto it.
tmapper = vtk.vtkTextureMapToCylinder()
tmapper.SetInputConnection(delny.GetOutputPort())
tmapper.PreventSeamOn()

# We scale the texture coordinate to get some repeat patterns.
xform = vtk.vtkTransformTextureCoords()
xform.SetInputConnection(tmapper.GetOutputPort())
xform.SetScale(40, 40, 1)

mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(xform.GetOutputPort())

# A texture is loaded using an image reader. Textures are simply images.
# The texture is eventually associated with an actor.

triangulation = vtk.vtkActor()
triangulation.SetMapper(mapper)
triangulation.SetTexture(atext)

# Create the standard rendering stuff.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
#ren.AddActor(triangulation)
ren.AddActor(actorBone5)
ren.ResetCamera()
ren.SetBackground(1, 1, 1)
renWin.SetSize(300, 300)

iren.Initialize()
renWin.Render()
iren.Start()