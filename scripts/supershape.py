import bpy
import bmesh
import math

OBJECT_NAME = "SuperShape"
MESH_NAME = OBJECT_NAME
SHAPE_SCALE = 2
SUBSURF_LEVEL = 1
RECYCLE_OBJECT = True
RECYCLE_MESH = RECYCLE_OBJECT

# mesh data arrays
verts = []
faces = []

# supershape parameters
m = (14, 6)
a = (-0.3, 0.2)
b = (0.2, 0.2)
n1 = (0.1, 0.1)
n2 = (2, 1)
n3 = (2, 4)

lon_num = 100
lat_num = 100
lon_inc = 2*math.pi/lon_num
lat_inc = math.pi/lat_num

# create vertices
# [longitude loop]
theta = -math.pi
for j in range(0, lon_num+1):
    r1 = 1 / (((abs((math.cos(m[0]*theta/4)/a[0])**n2[0])+abs((math.sin(m[0]*theta/4)/b[0])**n3[0])))**n1[0])
    # [latitude loop]
    phi = -math.pi/2
    for i in range(0, lat_num+1):
        r2 = 1 / (((abs((math.cos(m[1]*phi/4)/a[1])**n2[1])+abs((math.sin(m[1]*phi/4)/b[1])**n3[1])))**n1[1])
        # cartesian coordinates of the vertex (spherical product)
        radius = r1*r2
        x = SHAPE_SCALE * radius * math.cos(theta) * math.cos(phi)
        y = SHAPE_SCALE * radius * math.sin(theta) * math.cos(phi)
        z = SHAPE_SCALE * r2 * math.sin(phi)
        verts.append((x, y, z))
        phi += lat_inc 
    theta += lon_inc

# create faces
latitude_index = 0 # between 0 and lat_num-1
for i in range(0, lon_num * (lat_num+1)):
    if latitude_index < lat_num:
        A = i
        B = i + 1
        C = i + lat_num+1 + 1
        D = i + lat_num+1
        faces.append((A, B, C, D))
        latitude_index += 1
    else:
        latitude_index = 0

# create mesh and object or use existing ones
scn = bpy.context.scene
ob = me = None
if MESH_NAME in bpy.data.meshes and RECYCLE_MESH:
    me = bpy.data.meshes[MESH_NAME]
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.clear()
    bm.to_mesh(me)
    bm.free()
else:
    me = bpy.data.meshes.new(MESH_NAME)
if OBJECT_NAME in bpy.data.objects and RECYCLE_OBJECT:
    ob = bpy.data.objects[OBJECT_NAME]
    ob.data = me
else:
    ob = bpy.data.objects.new(OBJECT_NAME, me)
    scn.objects.link(ob)
    
# select object
bpy.ops.object.select_all(action='DESELECT')
scn.objects.active = ob
ob.select = True

# fill mesh data
me.from_pydata(verts, [], faces)
me.update(calc_edges=True)
# remove dupliactes and recalculate normals
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.remove_doubles() 
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')
 # origin to center of mass
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
ob.location = (0, 0, 0)

# subdivision surface modifier
if SUBSURF_LEVEL > 0:
    for mo in ob.modifiers:
        if mo.type == 'SUBSURF': bpy.ops.object.modifier_remove(modifier=mo.name)
    ob.modifiers.new("Subsurf", type='SUBSURF')
    ob.modifiers['Subsurf'].levels = SUBSURF_LEVEL
    ob.modifiers['Subsurf'].render_levels = SUBSURF_LEVEL
else:
    for mo in ob.modifiers:
        if mo.type == 'SUBSURF': bpy.ops.object.modifier_remove(modifier=mo.name)      
# smooth shading
for p in me.polygons: p.use_smooth = True
