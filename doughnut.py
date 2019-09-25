import bpy
from random import uniform, randint

def doughnut():
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
    
    # Enter edit mode
    bpy.ops.object.mode_set(mode = 'EDIT') 
    
    # Randomly select some vertices
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.select_random(percent = randint(5, 10), seed = randint(1, 10))
    
    # Get all selected vertices
    bpy.ops.object.mode_set(mode = 'OBJECT')
    selectedVerts = [i for i, v in enumerate(bpy.context.active_object.data.vertices) if v.select]
    
    # Misshape the doughnut at each selected vertex
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

doughnut()