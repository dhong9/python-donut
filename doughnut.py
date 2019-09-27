import bpy
import bmesh
from random import uniform, randint
from mathutils.geometry import distance_point_to_plane
from mathutils import Vector

def doughnut():
    # Helper functions:
    
    # Deselect all vertices
    def deselect():
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
    
    # Units are in meters
    radius = uniform(0.025, 0.05)
    
    # Add torus
    bpy.ops.mesh.primitive_torus_add(
        align = 'WORLD', 
        location = (0, 0, 0),
        rotation = (0, 0, 0), 
        major_radius = radius, 
        minor_radius = radius / uniform(1.8, 3),
        major_segments = 28,
        minor_segments = 16,
        abso_major_rad = 1.25, 
        abso_minor_rad = 0.75
    )
    
    deselect()
    
    # Randomly select some vertices
    bpy.ops.mesh.select_random(percent = randint(5, 10), seed = randint(1, 10))
    
    # Get all selected vertices
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selectedVerts = [i for i, v in enumerate(bpy.context.active_object.data.vertices) if v.select]
    deselect()
    
    # Find top half of doughnut
    context = bpy.context
    bbox = lambda ob: (Vector(b) for b in ob.bound_box)
    bbox_center = lambda ob: sum(bbox(ob), Vector()) / 8
    def bbox_axes(ob):
        bb = list(bbox(ob))
        return tuple(bb[i] - bb[0] for i in (4, 3, 1))
    ob = context.edit_object
    o = bbox_center(ob)
    x, y, z = bbox_axes(ob)
    top_doughnut = [i for i, v in enumerate(bpy.context.active_object.data.vertices) if distance_point_to_plane(v.co, o, z) >= 0.01]
    
    # Misshape the doughnut at each selected vertex
    bpy.ops.mesh.select_all(action = 'DESELECT')
    for i in selectedVerts:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type = "VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj.data.vertices[i].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.transform.translate(
            value = (0, 0, uniform(-0.006, 0.006)), 
            orient_type = 'NORMAL', 
            orient_matrix = (
                (1, 0, 0), 
                (0, 1, 0), 
                (0, 0, 1)
            ), 
            orient_matrix_type = 'NORMAL', 
            mirror = True, 
            use_proportional_edit = True, 
            proportional_edit_falloff = 'SMOOTH', 
            proportional_size = uniform(0.01667, 0.025), 
            use_proportional_connected = False, 
            use_proportional_projected = False
        )
    
    # Shade the doughnut smooth
    # OBJECT mode is required.
    bpy.ops.object.mode_set(mode = 'OBJECT')       
    bpy.ops.object.shade_smooth()
    
    # Add subsurf modifer
    bpy.ops.object.modifier_add(type='SUBSURF')
    
    # Go back to edit mode
    bpy.ops.object.mode_set(mode = 'EDIT')
    
    # Select the top half
    for i in top_doughnut:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type = "VERT")
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj.data.vertices[i].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        
    # Duplicate it
    bpy.ops.mesh.duplicate_move(
        MESH_OT_duplicate = {"mode" : 1}, 
        TRANSFORM_OT_translate = {
            "value": (0, 0, 0), 
            "orient_type": 'GLOBAL', 
            "orient_matrix":(
                (0, 0, 0), 
                (0, 0, 0), 
                (0, 0, 0)
            ), 
            "orient_matrix_type": 'GLOBAL', 
            "constraint_axis": (False, False, False), 
            "mirror": False, 
            "use_proportional_edit": False, 
            "proportional_edit_falloff": 'SMOOTH', 
            "proportional_size": 1, 
            "use_proportional_connected": False, 
            "use_proportional_projected": False, 
            "snap": False, 
            "snap_target":'CLOSEST', 
            "snap_point":(0, 0, 0), 
            "snap_align": False, 
            "snap_normal":(0, 0, 0), 
            "gpencil_strokes": False, 
            "cursor_transform": False, 
            "texture_space": False, 
            "remove_on_cancel": False, 
            "release_confirm": False, 
            "use_accurate": False
        }
    )
    
    # Separate it
    bpy.ops.mesh.separate(type = 'SELECTED')
    
    # Go to object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    icing = bpy.context.selected_objects[1]
    

doughnut()
