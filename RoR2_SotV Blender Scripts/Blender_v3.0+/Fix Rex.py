#Orignal Creator: KingEnderBrine
#Modified by: RuneFox237
#Version 1.0.1

import bpy
import re
from math import radians
from mathutils import Vector


bonesOrder = ['ROOT', 'Base', 'HeadBase', 'Eye', 'EyeControl', 'PlatformBase', 'Thigh.Front.l', 'Calf.Front.l', 'Foot.Front.l', 'Thigh.Back.l', 'Calf.Back.l', 'Foot.Back.l', 'Thigh.Front.r', 'Calf.Front.r', 'Foot.Front.r', 'Thigh.Back.r', 'Calf.Back.r', 'Foot.Back.r', 'ArmPlatformBase', 'ArmRotatorJoint', 'clavicle.l', 'shoulder.l', 'upperArm.l', 'lowerArm.l', 'hand.l', 'WeaponPlatform', 'IKTargetArm.l', 'Antennae.1', 'Antennae.005', 'Antennae.003', 'Antennae.007', 'Antennae.002', 'Antennae.006', 'Antennae.004', 'Antennae.008', 'FlowerBase', 'FlowerPetal1.1', 'FlowerPetal1.2', 'FlowerPetal1.3', 'FlowerPetal1.4', 'FlowerPetal1.002', 'FlowerPetal1.003', 'FlowerPetal1.004', 'FlowerPetal1.005', 'FlowerPetal1.006', 'FlowerPetal1.007', 'FlowerPetal1.008', 'FlowerPetal1.009', 'FlowerPetal1.010', 'FlowerPetal1.011', 'FlowerPetal1.012', 'FlowerPetal1.013', 'FlowerPetal1.014', 'FlowerPetal1.015', 'FlowerPetal1.016', 'FlowerPetal1.017', 'FlowerPetal1.018', 'FlowerPetal1.019', 'FlowerPetal1.020', 'FlowerPetal1.021', 'FlowerPetal1.022', 'FlowerPetal1.023', 'FlowerPetal1.024', 'FlowerPetal1.025', 'FlowerPetal1.030', 'FlowerPetal1.031', 'FlowerPetal1.032', 'FlowerPetal1.033', 'FlowerPetal1.034', 'FlowerPetal1.035', 'FlowerPetal1.036', 'FlowerPetal1.037', 'FlowerPetal1.038', 'FlowerPetal1.039', 'FlowerPetal1.040', 'FlowerPetal1.041', 'FlowerPetal1.042', 'FlowerPetal1.043', 'FlowerPetal1.044', 'FlowerPetal1.045', 'FlowerPetal2.001', 'FlowerPetal2.002', 'FlowerPetal2.003', 'FlowerPetal2.004', 'FlowerPetal2.005', 'FlowerPetal2.006', 'IKTargetLeg.Front.l', 'IKTargetLeg.Back.l', 'IKTargetLeg.Front.r', 'IKTargetLeg.Back.r']

srcArmName = 'Armature'
srcMeshName = 'TreebotBotMesh'

meshOffset = Vector((0, 0.8, 0)) # Vector((1, 1, 1))
meshSpecificOffset = None # {'TestMesh'=Vector((1, 1, 1))}

meshesScale = (0.5, 0.5, 0.5) # (1, 1, 1)
meshSpecificScale = None # {'TesMesh'=(1, 1, 1)}

excessiveMeshes = [] # ['TestMesh']

applyRestToPose = False





def RemoveExcessiveMeshes(excessiveMeshes):
    for meshName in excessiveMeshes:
        bpy.data.objects.remove(bpy.data.objects[meshName])    

def CopyEditBones(bones, editBones, offset = None):
    for bone in bones:
        boneCopy = editBones.new(bone.name)
    for bone in bones:
        boneCopy = editBones[bone.name]
        boneCopy.bbone_curveinx = bone.bbone_curveinx
        boneCopy.bbone_curveinz = bone.bbone_curveinz
        boneCopy.bbone_curveoutx = bone.bbone_curveoutx
        boneCopy.bbone_curveoutz = bone.bbone_curveoutz
        if bone.bbone_custom_handle_start is not None:
            boneCopy.bbone_custom_handle_start = editBones.get(bone.bbone_custom_handle_start.name, None)
        if bone.bbone_custom_handle_end is not None:
            boneCopy.bbone_custom_handle_end = editBones.get(bone.bbone_custom_handle_end.name, None)
        boneCopy.bbone_easein = bone.bbone_easein
        boneCopy.bbone_easeout = bone.bbone_easeout
        boneCopy.bbone_handle_type_end = bone.bbone_handle_type_end
        boneCopy.bbone_handle_type_start = bone.bbone_handle_type_start
        boneCopy.bbone_rollin = bone.bbone_rollin
        boneCopy.bbone_rollout = bone.bbone_rollout
        boneCopy.bbone_scalein = bone.bbone_scalein
        boneCopy.bbone_scaleout = bone.bbone_scaleout
        boneCopy.bbone_segments = bone.bbone_segments
        boneCopy.bbone_x = bone.bbone_x
        boneCopy.bbone_z = bone.bbone_z
        boneCopy.envelope_distance = bone.envelope_distance
        boneCopy.envelope_weight = bone.envelope_weight
        if offset is None or bone.use_connect:
            boneCopy.head = bone.head
        else:
            boneCopy.head = bone.head - offset
        if offset is None:
            boneCopy.tail = bone.tail
        else:
            boneCopy.tail = bone.tail - offset
        boneCopy.head_radius = bone.head_radius
        boneCopy.hide_select = bone.hide_select
        boneCopy.inherit_scale = bone.inherit_scale
        boneCopy.layers = bone.layers
        boneCopy.lock = bone.lock
        if bone.parent is not None:
            boneCopy.parent = editBones.get(bone.parent.name, None)
        boneCopy.roll = bone.roll
        boneCopy.select = bone.select
        boneCopy.select_head = bone.select_head
        boneCopy.select_tail = bone.select_tail
        boneCopy.show_wire = bone.show_wire
        boneCopy.tail_radius = bone.tail_radius
        boneCopy.use_connect = bone.use_connect
        boneCopy.use_cyclic_offset = bone.use_cyclic_offset
        boneCopy.use_deform = bone.use_deform
        boneCopy.use_endroll_as_inroll = bone.use_endroll_as_inroll
        boneCopy.use_envelope_multiply = bone.use_envelope_multiply
        boneCopy.use_inherit_rotation = bone.use_inherit_rotation
        boneCopy.use_local_location = bone.use_local_location
        boneCopy.use_relative_parent = bone.use_relative_parent

def Prepare(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')

    roll = srcArm.data.edit_bones[0].roll 
    
    bpy.ops.object.mode_set(mode='OBJECT')
    srcArm.rotation_euler = (radians(90), 0, -roll)
    srcArm.scale = (1,1,1)

def PrepareMeshes(srcMeshName, meshParentBones, scale = None, meshOffset = None, meshSpecificScale = None, meshSpecificOffset = None):
    srcMesh = bpy.data.objects[srcMeshName]
    bpy.context.view_layer.objects.active = srcMesh
    bpy.ops.object.mode_set(mode='OBJECT')
    
    offset = Vector(srcMesh.location)
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        if meshSpecificScale is not None and obj.name in meshSpecificScale:
            obj.scale = meshSpecificScale[obj.name]
        elif scale is not None:
            obj.scale = scale
                
        if not obj.parent_bone:
            obj.location -= offset
            if meshSpecificOffset is not None and obj.name in meshSpecificOffset:
                obj.location += meshSpecificOffset[obj.name]
            elif meshOffset is not None:
                obj.location += meshOffset
        else:
            meshParentBones[obj.name] = obj.parent_bone

def PrepareBones(bonesOrder, srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    
    tmpArm = bpy.data.objects.new('TempArmature', bpy.data.armatures.new('TempArmature'))
    bpy.context.scene.collection.objects.link(tmpArm)
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = tmpArm
    bpy.ops.object.mode_set(mode='EDIT')
    
    srcEditBones = srcArm.data.edit_bones
    
    offset = Vector(srcEditBones.get('ROOT').parent.head) if srcEditBones.get('ROOT').parent is not None else None
    
    bones = []
    for key in bonesOrder:
        bones.append(srcEditBones[key])
        
    tmpEditBones = tmpArm.data.edit_bones
    
    for bone in tmpEditBones:
        tmpEditBones.remove(bone)
    CopyEditBones(bones, tmpEditBones, offset)
    
    for bone in srcEditBones:
        srcEditBones.remove(bone)
    
    CopyEditBones(tmpEditBones, srcEditBones)
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = tmpArm
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.context.scene.collection.objects.unlink(tmpArm)
    bpy.data.armatures.remove(tmpArm.data)
  
def FinalizeBones(bonesOrder, srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bones = srcArm.data.bones
    
    meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH': 
            meshes.append(obj)
            
    vertexGroupNames = set()
    for vertexGroups in [ m.vertex_groups for m in meshes ]:
        for vertexGroup in vertexGroups:
            vertexGroupNames.add(vertexGroup.name)
        
    pattern = '\A.*IK.*\Z'
    for bone in bones:
        if bone.name not in vertexGroupNames:
            bone.use_deform = False
        if re.search(pattern, bone.name):
            bone.hide = True
        
def FinalizeMeshes(meshParentBones):
    for meshName in meshParentBones:
        bpy.data.objects[meshName].parent_bone = meshParentBones[meshName]

def FinalizePose(srcArmName, applyRestToPose = False):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    
    if not applyRestToPose:
        bpy.ops.object.mode_set(mode='POSE')
    
        for pbone in srcArm.pose.bones:
            pbone.bone.select = True
    
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()
        bpy.ops.pose.transforms_clear()
    
        bpy.ops.object.mode_set(mode='OBJECT')
        return
    
    storedModifiersInfo = {}
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if 'Armature' not in [m.name for m in obj.modifiers ]:
            continue
        
        modifier = obj.modifiers['Armature']
        
        storedModifiersInfo[obj.name] = modifier.object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier='Armature')
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if obj.name not in storedModifiersInfo:
            continue
        
        modifier = obj.modifiers.new('Armature', 'ARMATURE')
        modifier.object = storedModifiersInfo[obj.name]
        modifier.use_vertex_groups = True

def Finalize():
    for obj in bpy.data.objects:
        bpy.ops.object.transform_apply(location = True, scale = False, rotation = True)

meshParentBones = {}

RemoveExcessiveMeshes(excessiveMeshes)
Prepare(srcArmName)
PrepareMeshes(srcMeshName, meshParentBones, meshesScale, meshOffset, meshSpecificScale, meshSpecificOffset)
PrepareBones(bonesOrder, srcArmName)
FinalizeBones(bonesOrder, srcArmName)
FinalizeMeshes(meshParentBones)
FinalizePose(srcArmName, applyRestToPose)
Finalize()