import bpy
from random import uniform, randint
import colorsys
import os

def doughnut():
    
    # Deselect all vertices
    def deselect():
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_all(action = 'DESELECT')
    
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
    
    # Add material to doughnut
    doughnutMaterial = bpy.data.materials.new(name = "doughnutMaterial")
    doughnutMaterial.use_nodes = True
    doughnutNodes = doughnutMaterial.node_tree.nodes
    # Colors hardcoded, can be adjusted after they get added
    doughnutPrincipled = doughnutNodes["Principled BSDF"]
    doughnutPrincipled.inputs[3].default_value = (0.615, 0.292, 0.088, 1) # Subsurface color
    doughnutPrincipled.inputs[2].default_value = (0.2, 0.2, 0.2)
    
    # Material node edtior :-)
    # Access nodes
    doughnutNodeTree = doughnutMaterial.node_tree
    doughnutNodes = doughnutNodeTree.nodes
    
    # Displacement
    doughnutDisplacement = doughnutNodes.new("ShaderNodeDisplacement")
    doughnutDisplacement.location = (-200, -420)
    doughnutDisplacement.inputs[2].default_value = 0.002 # Scale
    doughnutNodeTree.links.new(doughnutNodes.get("Material Output").inputs[2], doughnutDisplacement.outputs[0])
    
    # Overlay
    doughnutOverlay = doughnutNodes.new("ShaderNodeMixRGB")
    doughnutOverlay.blend_type = "OVERLAY"
    doughnutOverlay.location = (-200, 300)
    doughnutNodeTree.links.new(doughnutPrincipled.inputs[0], doughnutOverlay.outputs[0])
    
    # Add
    doughnutAdd = doughnutNodes.new("ShaderNodeMixRGB")
    doughnutAdd.blend_type = "ADD"
    doughnutAdd.location = (-600, -300)
    doughnutAdd.inputs[0].default_value = 0.736
    doughnutNodeTree.links.new(doughnutOverlay.inputs[0], doughnutAdd.outputs[0])
    doughnutNodeTree.links.new(doughnutDisplacement.inputs[0], doughnutAdd.outputs[0])
    
    # Color ramp
    doughnutColorRamp = doughnutNodes.new("ShaderNodeValToRGB")
    doughnutColorRamp.location = (-1000, -500)
    doughnutNodeTree.links.new(doughnutAdd.inputs[1], doughnutColorRamp.outputs[0])
    
    # Noise texture 1
    doughnutNoise1 = doughnutNodes.new("ShaderNodeTexNoise")
    doughnutNoise1.location = (-1350, -300)
    doughnutNoise1.inputs[1].default_value = 2000
    doughnutNodeTree.links.new(doughnutAdd.inputs[2], doughnutNoise1.outputs[1])
    
    # Noise texture 2
    doughnutNoise2 = doughnutNodes.new("ShaderNodeTexNoise")
    doughnutNoise2.location = (-1350, -700)
    doughnutNoise1.inputs[1].default_value = 200
    doughnutNodeTree.links.new(doughnutColorRamp.inputs[0], doughnutNoise2.outputs[1])
    
    # Texture coordinate
    doughnutTexCoord = doughnutNodes.new("ShaderNodeTexCoord")
    doughnutTexCoord.location = (-1600, -500)
    doughnutNodeTree.links.new(doughnutNoise1.inputs[0], doughnutTexCoord.outputs[3])
    doughnutNodeTree.links.new(doughnutNoise2.inputs[0], doughnutTexCoord.outputs[3])
    
    # Image texture
    doughnutImgTex = doughnutNodes.new("ShaderNodeTexImage")
    doughnutImgTex.location = (-500, 300)
    doughnutNodeTree.links.new(doughnutOverlay.inputs[1], doughnutImgTex.outputs[0])
    
    # Add this material to doughnut
    bpy.context.active_object.data.materials.append(doughnutMaterial)

    
doughnut()
