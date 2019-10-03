import bpy
from random import uniform, randint

def doughnut():
    # Helper functions:
    
    # Deselect all vertices
    def deselect():
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
    
    # Add fluid sim of given type
    def fluidSim(x):
        bpy.ops.object.modifier_add(type='FLUID_SIMULATION')
        bpy.context.object.modifiers["Fluidsim"].settings.type = x
    
    # Units are in meters
    r = uniform(0.025, 0.05)
    mr = r / uniform(1.8, 3)
    
    # Add torus
    bpy.ops.mesh.primitive_torus_add(
        align = 'WORLD', 
        location = (0, 0, 0),
        rotation = (0, 0, 0), 
        major_radius = r, 
        minor_radius = mr,
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
    
    # Make the doughnut a fluid obstacle
    fluidSim("OBSTACLE")
    
    # Add a circle
    icingRadius = uniform(r - mr, r)
    bpy.ops.mesh.primitive_circle_add(radius = icingRadius, enter_editmode = True, location = (0, 0, 1.55 * mr))
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region = {
            "use_normal_flip": False, 
            "mirror": False
        }, 
        TRANSFORM_OT_translate = {
            "value": (0, 0, 0), 
            "orient_type": 'GLOBAL', 
            "orient_matrix": ((0, 0, 0), (0, 0, 0), (0, 0, 0)), 
            "orient_matrix_type": 'GLOBAL', 
            "constraint_axis": (False, False, False), 
            "mirror": False, 
            "use_proportional_edit": False, 
            "snap": False, 
            "snap_target": 'CLOSEST', 
            "snap_point": (0, 0, 0), 
            "snap_align": False, 
            "snap_normal": (0, 0, 0), 
            "gpencil_strokes": False, 
            "cursor_transform": False, 
            "texture_space": False, 
            "remove_on_cancel": False, 
            "release_confirm": False, 
            "use_accurate": False
        }
    )
    
    # Scale up the icing
    icingScale = uniform(1.25, 1.5) # Will need to tweak these around
    bpy.ops.transform.resize(
        value = (icingScale * r / icingRadius, icingScale * r / icingRadius, icingScale * r / icingRadius),
        orient_type = 'GLOBAL', 
        orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type = 'GLOBAL', 
        mirror = True, 
        use_proportional_edit = False,
        proportional_size = 1, 
        use_proportional_connected = False, 
        use_proportional_projected = False
    )
    
    # Extrude it up
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region = {
            "use_normal_flip" : False, 
            "mirror" : False
        }, 
        TRANSFORM_OT_translate = {
            "value" : (0, 0, 0.0025), 
            "orient_type": 'LOCAL', 
            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            "orient_matrix_type": 'LOCAL', 
            "constraint_axis": (False, False, True), 
            "mirror": False, 
            "use_proportional_edit": False, 
            "proportional_edit_falloff":'SMOOTH', 
            "snap": False, 
            "snap_target": 'CLOSEST', 
            "snap_point": (0, 0, 0), 
            "snap_align": False, 
            "snap_normal": (0, 0, 0), 
            "gpencil_strokes": False, 
            "cursor_transform": False, 
            "texture_space": False, 
            "remove_on_cancel": False, 
            "release_confirm": False, 
            "use_accurate": False
        }
    )
    
    # Recalculate normals
    bpy.ops.mesh.select_all(action = 'SELECT')
    bpy.ops.mesh.normals_make_consistent(inside = False)
    
    bpy.ops.object.mode_set(mode = 'OBJECT')  
    
    # Make that icing a fluid
    fluidSim("FLUID")
    
    # Add a box
    bpy.ops.mesh.primitive_cube_add(size = 2, enter_editmode = False, location = (0, 0, 0))
    bpy.ops.transform.resize(
        value = (r * 2, r * 2, r), 
        orient_type= 'GLOBAL', 
        orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type = 'GLOBAL', 
        mirror = True, 
        use_proportional_edit = False
    )
    
    # Make that a fluid domain
    fluidSim("DOMAIN")
    bpy.context.object.modifiers["Fluidsim"].settings.resolution = 90
    bpy.context.object.modifiers["Fluidsim"].settings.viscosity_base = 1
    bpy.context.object.modifiers["Fluidsim"].settings.viscosity_exponent = 2

    
doughnut()
