import bpy
import bmesh
from mathutils import Vector
import os
import math
import random
from datetime import datetime

start_time = datetime.now()

ITERATION_COUNT = 5

OUTPUT_DIRECTORY = os.path.join(os.path.dirname(bpy.data.filepath), "output")
OUTPUT_FILENAME = "" # string at the beginning of the file name
RENDER_RESOLUTION = (320, 320)
SUBSURF_LEVEL = -1 # subdivision surface level
AMBIENT_OCCLUSION = -1 # ao factor between 0 and 1
ANTIALIASING = False

CAMERA_NAME = "Camera"
LIGHT1_NAME = "Sun"
LIGHT2_NAME = "Hemi"
MATERIAL_NAME = "SuperShape"
OBJECT_NAME = "SuperShape"
MESH_NAME = OBJECT_NAME

SHAPE_SCALE = 1
OBJECT_SIZE = 10
RECYCLE_MESH = True
MESH_RESOLUTION = (100, 100) # vertices for longitude and latitude

# (value, max distance from value)
# ((shape1[longitude]), (shape2[latitude]))
P_M_val = ((12, 8), (0, 5))
P_A_val = ((1, 0.2), (1, 0.2))
P_B_val = ((1, 0.2), (1, 0.2))
P_1_val = ((0.5, 0.25), (0.5, 0.25))
P_2_val = ((4, 3), (4, 4))
P_3_val = ((4, 2), (4, 2))
# True <=> integer only
P_M_int = (False, False)
P_A_int = (False, False)
P_B_int = (False, False)
P_1_int = (False, False)
P_2_int = (False, False)
P_3_int = (False, False)

def set_parameters():
    m_range = ((P_M_val[0][0]-P_M_val[0][1], P_M_val[0][0]+P_M_val[0][1]),
               (P_M_val[1][0]-P_M_val[1][1], P_M_val[1][0]+P_M_val[1][1]))
    a_range = ((P_A_val[0][0]-P_A_val[0][1], P_A_val[0][0]+P_A_val[0][1]),
               (P_A_val[1][0]-P_A_val[1][1], P_A_val[1][0]+P_A_val[1][1]))
    b_range = ((P_B_val[0][0]-P_B_val[0][1], P_B_val[0][0]+P_B_val[0][1]),
               (P_B_val[1][0]-P_B_val[1][1], P_B_val[1][0]+P_B_val[1][1]))
    n1_range= ((P_1_val[0][0]-P_1_val[0][1], P_1_val[0][0]+P_1_val[0][1]),
               (P_1_val[1][0]-P_1_val[1][1], P_1_val[1][0]+P_1_val[1][1]))
    n2_range= ((P_2_val[0][0]-P_2_val[0][1], P_2_val[0][0]+P_2_val[0][1]),
               (P_2_val[1][0]-P_2_val[1][1], P_2_val[1][0]+P_2_val[1][1]))
    n3_range= ((P_3_val[0][0]-P_3_val[0][1], P_3_val[0][0]+P_3_val[0][1]),
               (P_3_val[1][0]-P_3_val[1][1], P_3_val[1][0]+P_3_val[1][1]))
    m=[
    random.randint(round(m_range[0][0]), round(m_range[0][1])) if P_M_int[0] else random.uniform(m_range[0][0], m_range[0][1]),
    random.randint(round(m_range[1][0]), round(m_range[1][1])) if P_M_int[1] else random.uniform(m_range[1][0], m_range[1][1])]
    a=[
    random.randint(round(a_range[0][0]), round(a_range[0][1])) if P_A_int[0] else random.uniform(a_range[0][0], a_range[0][1]),
    random.randint(round(a_range[1][0]), round(a_range[1][1])) if P_A_int[1] else random.uniform(a_range[1][0], a_range[1][1])]
    b=[
    random.randint(round(b_range[0][0]), round(b_range[0][1])) if P_B_int[0] else random.uniform(b_range[0][0], b_range[0][1]),
    random.randint(round(b_range[1][0]), round(b_range[1][1])) if P_B_int[1] else random.uniform(b_range[1][0], b_range[1][1])]
    n1=[
    random.randint(round(n1_range[0][0]), round(n1_range[0][1])) if P_1_int[0] else random.uniform(n1_range[0][0], n1_range[0][1]),
    random.randint(round(n1_range[1][0]), round(n1_range[1][1])) if P_1_int[1] else random.uniform(n1_range[1][0], n1_range[1][1])]
    n2=[
    random.randint(round(n2_range[0][0]), round(n2_range[0][1])) if P_2_int[0] else random.uniform(n2_range[0][0], n2_range[0][1]),
    random.randint(round(n2_range[1][0]), round(n2_range[1][1])) if P_2_int[1] else random.uniform(n2_range[1][0], n2_range[1][1])]
    n3=[
    random.randint(round(n3_range[0][0]), round(n3_range[0][1])) if P_3_int[0] else random.uniform(n3_range[0][0], n3_range[0][1]),
    random.randint(round(n3_range[1][0]), round(n3_range[1][1])) if P_3_int[1] else random.uniform(n3_range[1][0], n3_range[1][1])]
    #m[0] = m[0] + (1 if P_M_int[0] else 0.1) if m[0] == 0 else m[0]
    #m[1] = m[1] + (1 if P_M_int[1] else 0.1) if m[1] == 0 else m[1]
    a[0] = a[0] + (1 if P_A_int[0] else 0.1) if a[0] == 0 else a[0]
    a[1] = a[1] + (1 if P_A_int[1] else 0.1) if a[1] == 0 else a[1]
    b[0] = b[0] + (1 if P_B_int[0] else 0.1) if b[0] == 0 else b[0]
    b[1] = b[1] + (1 if P_B_int[1] else 0.1) if b[1] == 0 else b[1]
    n1[0] = n1[0] + (1 if P_1_int[0] else 0.1) if n1[0] == 0 else n1[0]
    n1[1] = n1[1] + (1 if P_1_int[1] else 0.1) if n1[1] == 0 else n1[1]
    n2[0] = n2[0] + (1 if P_2_int[0] else 0.1) if n2[0] == 0 else n2[0]
    n2[1] = n2[1] + (1 if P_2_int[1] else 0.1) if n2[1] == 0 else n2[1]
    n3[0] = n3[0] + (1 if P_3_int[0] else 0.1) if n3[0] == 0 else n3[0]
    n3[1] = n3[1] + (1 if P_3_int[1] else 0.1) if n3[1] == 0 else n3[1]
    return ((m[0],m[1]), (a[0],a[1]), (b[0],b[1]), (n1[0],n1[1]), (n2[0],n2[1]), (n3[0],n3[1]))

def set_lights():
    global LIGHT1_NAME
    global LIGHT2_NAME

    # get sun or create one
    sun = sun_ob = None
    if LIGHT1_NAME in bpy.data.lamps:
        sun = bpy.data.lamps[LIGHT1_NAME]
    else:
        sun = bpy.data.lamps.new(LIGHT1_NAME, type='SUN')
    if LIGHT1_NAME in bpy.data.objects:
        sun_ob = bpy.data.objects[LIGHT1_NAME]
    else:
        sun_ob = bpy.data.objects.new(LIGHT1_NAME, sun)
        bpy.context.scene.objects.link(sun_ob)
        
    # get hemi or create one
    hemi = hemi_ob = None
    if LIGHT2_NAME in bpy.data.lamps:
        hemi = bpy.data.lamps[LIGHT2_NAME]
    else:
        hemi = bpy.data.lamps.new(LIGHT2_NAME, type='HEMI')
    if LIGHT2_NAME in bpy.data.objects:
        hemi_ob = bpy.data.objects[LIGHT2_NAME]
    else:
        hemi_ob = bpy.data.objects.new(LIGHT2_NAME, hemi)
        bpy.context.scene.objects.link(hemi_ob)
        
    # postion
    sun_ob.location = (0,0,5)
    hemi_ob.location = (0,0,-5)
    
    # rotation
    sun_ob.rotation_euler.x = math.pi/4
    sun_ob.rotation_euler.z = math.pi/4
    hemi_ob.rotation_euler.x = math.pi
    
    # sun settings
    sun.type = 'SUN'
    sun.use_diffuse = True
    sun.use_specular = True
    sun.energy = 1.0
    sun.color = [1,1,1]
    
    # hemi settings
    hemi.type = 'HEMI'
    hemi.use_diffuse = True
    hemi.use_specular = False
    hemi.energy = 0.125
    hemi.color = [1,1,1]

def set_camera():
    global CAMERA_NAME

    # get camera or create one
    cam = cam_ob = None
    if CAMERA_NAME in bpy.data.cameras:
        cam = bpy.data.cameras[CAMERA_NAME]
    else:
        cam = bpy.data.cameras.new(CAMERA_NAME)
    if CAMERA_NAME in bpy.data.objects:
        cam_ob = bpy.data.objects[CAMERA_NAME]
    else:
        cam_ob = bpy.data.objects.new(CAMERA_NAME, cam)
        bpy.context.scene.objects.link(cam_ob)
    
    # position
    ob = bpy.data.objects[OBJECT_NAME]
    cam_ob.location = (0,0,0)
    max_dim = max(ob.dimensions.z, max(ob.dimensions.y, ob.dimensions.x))
    dim_ratio = 1
    try:
        dim_ratio = ob.dimensions.y/ob.dimensions.x if ob.dimensions.y>ob.dimensions.x else ob.dimensions.x/ob.dimensions.y
    except ZeroDivisionError: pass
    cam_ob.location.y += max_dim * 1.1
    cam_ob.location.x += max_dim * 1.1
    cam_ob.location.z += max_dim / dim_ratio
    
    # rotation
    dir = Vector((0,0,0)) - cam_ob.location
    cam_ob.rotation_euler = dir.to_track_quat('-Z', 'Y').to_euler()
    
    # other settings
    cam.clip_start = 0.002
    cam.clip_end = 3*max(abs(cam_ob.location.z), max(abs(cam_ob.location.x), abs(cam_ob.location.y)))
    cam.show_limits = True
    # set camera as the active one
    bpy.context.scene.camera = cam_ob

def set_material(m, a, b, n1, n2, n3):
    global MATERIAL_NAME
    
    # get material or create one
    mat = None
    if MATERIAL_NAME in bpy.data.materials:
        mat = bpy.data.materials[MATERIAL_NAME]
    else:
        mat = bpy.data.materials.new(MATERIAL_NAME)
        
    # color
    t = 2+m+n1
    ps = m+a+b+n1+n2+n3
    r = g = b = 0.3
    r += 0.5*(0.5+0.5*math.sin( ps + 2*t ))
    g += 0.5*(0.5+0.5*math.sin( ps + 3*t ))
    b += 0.5*(0.5+0.5*math.sin( ps + 4*t ))
    f = 1.6
    if r == max(r, max(g, b)): r *= f
    elif g == max(r, max(g, b)): g *= f
    else: b *= f
    mat.diffuse_color = [r, g, b]
    
    # shading
    mat.diffuse_intensity = 1.0
    mat.specular_shader = 'BLINN'
    mat.specular_hardness = 80
    mat.specular_intensity = 1.0
    mat.ambient = 0.025
    
    # link material to object
    obj = bpy.data.objects[OBJECT_NAME]
    if len(obj.data.materials):
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def create_supershape(m, a, b, n1, n2, n3):
    # mesh data arrays
    verts = []
    faces = []

    lon_num = MESH_RESOLUTION[0]
    lat_num = MESH_RESOLUTION[1]
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
            x = radius * math.cos(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.cos(phi)
            z = r2 * math.sin(phi)
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
    if OBJECT_NAME in bpy.data.objects:
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
    # adjusts object size
    scale_ratio = 1
    try:
        scale_ratio = OBJECT_SIZE / (max(ob.dimensions.z, max(ob.dimensions.x, ob.dimensions.y)))
    except ZeroDivisionError: pass
    ob.dimensions.x *= scale_ratio
    ob.dimensions.y *= scale_ratio
    ob.dimensions.z *= scale_ratio
    bpy.ops.object.transform_apply(scale=True)
    
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

def render_scene(index):
    global OUTPUT_DIRECTORY
    global OUTPUT_FILENAME
    path = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILENAME + str(index))
    scn = bpy.context.scene
    scn.render.filepath = path
    bpy.ops.render.render(write_still=True)
    
def _init():
    global OUTPUT_DIRECTORY
    global OUTPUT_FILENAME
    global ITERATION_COUNT
    
    # exit if the blend file is not save somewhere
    if not bpy.data.filepath:
        print("!!! The blend file must be saved in a directory !!!")
        ITERATION_COUNT = 0
        return

    # create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        
    # filename
    now = datetime.now()
    OUTPUT_FILENAME += now.strftime("%Y%m%d_%H%M.") + str(now.microsecond)[:2] + "_"
    
    # render settings
    scn = bpy.context.scene
    scn.render.resolution_x = RENDER_RESOLUTION[0]
    scn.render.resolution_y = RENDER_RESOLUTION[1]
    scn.render.resolution_percentage = 100
    scn.render.use_border = False
    scn.render.use_antialiasing = ANTIALIASING
    scn.render.antialiasing_samples = '5'
    scn.render.image_settings.file_format = 'PNG'
    
    scn.render.use_stamp = True
    scn.render.use_stamp_note = True
    scn.render.use_stamp_camera = False
    scn.render.use_stamp_filename = False
    scn.render.use_stamp_date = False
    scn.render.use_stamp_scene = False
    scn.render.use_stamp_time = False
    scn.render.use_stamp_render_time = False
    scn.render.use_stamp_frame = False
    scn.render.stamp_font_size = RENDER_RESOLUTION[1] / 40
    
    # world lighting
    world = bpy.context.scene.world
    world.horizon_color = [0, 0, 0]
    world.ambient_color = [1, 1, 1]
    if AMBIENT_OCCLUSION > 0:
        world.light_settings.use_ambient_occlusion = True
        world.light_settings.ao_factor = AMBIENT_OCCLUSION
    else:
        world.light_settings.use_ambient_occlusion = False
        
    # lamps
    set_lights()

# INITIALIZATION
_init()
    
# MAIN LOOP
skipped_itr = 0
for i in range(1, ITERATION_COUNT+1):
    # supershape parameters (random)
    params = set_parameters()
    m = params[0]
    a = params[1]
    b = params[2]
    n1 = params[3]
    n2 = params[4]
    n3 = params[5]
    
    # create supershape
    try:
        create_supershape(m, a, b, n1, n2, n3)
    except:
        skipped_itr += 1
        print("Iteration " + str(i) + " skipped")
        pass
        continue
    
    # material color (based on parameters)
    set_material(m[0]+m[1], a[0]+a[1], b[0]+b[1], n1[0]+n1[1], n2[0]+n2[1], n3[0]+n3[1])
    
    # camera
    set_camera()
    
    # render and save
    bpy.context.scene.render.stamp_note_text = "{m1} {a1} {b1} {n11} {n21} {n31} | {m2} {a2} {b2} {n12} {n22} {n32}".format(
    m1=round(m[0],2), a1=round(a[0],2), b1=round(b[0],2), n11=round(n1[0],2), n21=round(n2[0],2), n31=round(n3[0],2),
    m2=round(m[1],2), a2=round(a[1],2), b2=round(b[1],2), n12=round(n1[1],2), n22=round(n2[1],2), n32=round(n3[1],2))
    render_scene(i)

# execution time
print("Iterations: {itr} ({skipped} skipped), Time: {t}".format(
    itr=ITERATION_COUNT-skipped_itr,
    skipped=skipped_itr,
    t=datetime.now()-start_time
))
