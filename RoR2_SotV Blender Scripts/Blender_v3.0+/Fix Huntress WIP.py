#Orignal Creator: KingEnderBrine
#Modified by: RuneFox237
#Version 1.0.1

import bpy
import re
from math import radians
from mathutils import Vector

############################################################
# NOTE: Does not currently export Scarf bones correctly
############################################################

bonesOrder = ['ROOT', 'base', 'stomach', 'chest', 'upper_arm.l', 'lower_arm.l', 'hand.l', 'finger1.1.l', 'finger1.2.l', 'finger1.3.l', 'finger2.1.l', 'finger2.2.l', 'finger2.3.l', 'finger3.1.l', 'finger3.2.l', 'finger3.3.l', 'finger4.1.l', 'finger4.2.l', 'finger4.3.l', 'thumb.1.l', 'thumb.2.l', 'upper_arm.r', 'lower_arm.r', 'hand.r', 'finger1.1.r', 'finger1.2.r', 'finger1.3.r', 'finger2.1.r', 'finger2.2.r', 'finger2.3.r', 'finger3.1.r', 'finger3.2.r', 'finger3.3.r', 'finger4.1.r', 'finger4.2.r', 'finger4.3.r', 'thumb.1.r', 'thumb.2.r', 'head', 'pelvis', 'thigh.l', 'calf.l', 'foot.l', 'toe.l', 'thigh.r', 'calf.r', 'foot.r', 'toe.r', 'BowRoot', 'BowStringIKTarget', 'HelperBowString', 'BowBase', 'BowHinge1.l', 'BowHinge2.l', 'BowString.L', 'BowHinge1.r', 'BowHinge2.r', 'BowString.R', 'HelperBowBase', 'IKArmTarget.l', 'IKArmPole.l', 'IKLegTarget.l', 'IKLegPole.l', 'IKLegTarget.r', 'IKLegPole.r', 'IKArmTarget.r', 'IKArmPole.r', 'HandGripControl.l', 'HandGripControl.r']

extraArmBonesOrder = ['ScarfBase,Detatched', 'Scarf', 'Scarf.004', 'Scarf.002', 'Scarf.006', 'Scarf.001', 'Scarf.005', 'Scarf.003', 'Scarf.007']
extraArmParentBone = 'head'
extraArmName = 'HuntressScarfArmature,Detatched'
extraArmMeshes = ['HuntressScarfMesh']

srcArmName = 'Armature'
srcMeshName = 'HuntressMesh'

meshOffset = None # Vector((1, 1, 1))
meshSpecificOffset = None # {'TestMesh':Vector((1, 1, 1))}

meshesScale = None # (1, 1, 1)
meshSpecificScale = {'BowMesh':(0.086, 0.086, 0.086)} # {'TesMesh':(1, 1, 1)}

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
        
def FinalizeMeshes(meshParentBones, srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bones = srcArm.data.bones
    for meshName in meshParentBones:
        parentBoneName = meshParentBones[meshName]
        bpy.data.objects[meshName].parent_bone = parentBoneName if parentBoneName in [ bone.name for bone in bones ] else ''

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

def ExtractExtraArmature(srcArmName, extraArmName, extraArmBonesOrder, extraArmParentBone):
    global offsetFromRoot
    
    srcArm = bpy.data.objects[srcArmName]
    
    extraArm = bpy.data.objects.new(extraArmName, bpy.data.armatures.new(extraArmName))
    bpy.context.scene.collection.objects.link(extraArm)
    
    if bpy.data.collections['Collection'] is not None:
        bpy.data.scenes['Scene'].collection.objects.unlink(extraArm)
        bpy.data.collections['Collection'].objects.link(extraArm)
    
    extraArm.parent = srcArm
    extraArm.parent_type = 'BONE'
    extraArm.parent_bone = extraArmParentBone
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = extraArm
    bpy.ops.object.mode_set(mode='EDIT')
    
    srcEditBones = srcArm.data.edit_bones
    
    rootOffset = Vector(srcEditBones.get('ROOT').parent.head) if srcEditBones.get('ROOT').parent is not None else None
    offset = Vector(srcEditBones.get(extraArmBonesOrder[0]).parent.head) if srcEditBones.get(extraArmBonesOrder[0]).parent is not None else None
    
    offsetFromRoot = rootOffset - offset
    
    bones = []
    for key in extraArmBonesOrder:
        bones.append(srcEditBones[key])
        
    extraEditBones = extraArm.data.edit_bones
    
    for bone in extraEditBones:
        extraEditBones.remove(bone)
    CopyEditBones(bones, extraEditBones, offset)
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = extraArm
    bpy.ops.object.mode_set(mode='OBJECT')
    
def MoveMeshesToExtra(extraArmName, extraArmMeshes, offsetFromRoot):
    extraArm = bpy.data.objects[extraArmName]
    
    for meshName in extraArmMeshes:
        mesh = bpy.data.objects[meshName]
        mesh.parent = extraArm
        mesh.location += offsetFromRoot
    
meshParentBones = {}

RemoveExcessiveMeshes(excessiveMeshes)
Prepare(srcArmName)
PrepareMeshes(srcMeshName, meshParentBones, meshesScale, meshOffset, meshSpecificScale, meshSpecificOffset)

offsetFromRoot = None

#ExtractExtraArmature(srcArmName, extraArmName, extraArmBonesOrder, extraArmParentBone)
#MoveMeshesToExtra(extraArmName, extraArmMeshes, offsetFromRoot)

PrepareBones(bonesOrder, srcArmName)
FinalizeBones(bonesOrder, srcArmName)
FinalizeMeshes(meshParentBones, srcArmName)
FinalizePose(srcArmName, applyRestToPose)
Finalize()