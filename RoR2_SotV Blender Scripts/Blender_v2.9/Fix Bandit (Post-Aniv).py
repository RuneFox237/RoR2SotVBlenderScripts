#Orignal Creator: KingEnderBrine
#Modified by: RuneFox237
#Version 1.0.1

import bpy
import re
from math import radians
from mathutils import Vector


bonesOrder = ['ROOT', 'base', 'stomach', 'chest', 'clavicle.l', 'upper_arm.l', 'lower_arm.l', 'hand.l', 'finger4.1.l', 'finger4.2.l', 'finger4.3.l', 'thumb.1.l', 'thumb.2.l', 'finger3.1.l', 'finger3.2.l', 'finger3.3.l', 'finger2.1.l', 'finger2.2.l', 'finger2.3.l', 'finger1.1.l', 'finger1.2.l', 'finger1.3.l', 'head', 'hat', 'clavicle.r', 'upper_arm.r', 'lower_arm.r', 'hand.r', 'finger4.1.r', 'finger4.2.r', 'finger4.3.r', 'thumb.1.r', 'thumb.2.r', 'finger3.1.r', 'finger3.2.r', 'finger3.3.r', 'finger2.1.r', 'finger2.2.r', 'finger2.3.r', 'finger1.1.r', 'finger1.2.r', 'finger1.3.r', 'coatjiggle.1.1', 'coatjiggle.1.2', 'coatjiggle.1.3', 'coatjiggle.1.4', 'coatjiggle.2.1.r', 'coatjiggle.2.2.r', 'coatjiggle.2.3.r', 'coatjiggle.2.4.r', 'coatjiggle.3.1.r', 'coatjiggle.3.2.r', 'coatjiggle.3.3.r', 'coatjiggle.3.4.r', 'coatjiggle.2.1.l', 'coatjiggle.2.2.l', 'coatjiggle.2.3.l', 'coatjiggle.2.4.l', 'coatjiggle.3.1.l', 'coatjiggle.3.2.l', 'coatjiggle.3.3.l', 'coatjiggle.3.4.l', 'pelvis', 'thigh.l', 'calf.l', 'foot.l', 'toe.l', 'thigh.r', 'calf.r', 'foot.r', 'toe.r', 'IKArmTarget.l', 'IKArmPole.l', 'IKArmTarget.r', 'IKArmPole.r', 'MainWeapon', 'WeaponHandPlacement.r', 'WeaponHandPlacement.l', 'HeelRoll.l', 'ToeRoll.l', 'FootRoll.l', 'IKLegTarget.l', 'ToeControl.l', 'IKToe.l', 'IKFoot.l', 'IKLegPole.l', 'HeelRoll.r', 'ToeRoll.r', 'FootRoll.r', 'IKLegTarget.r', 'ToeControl.r', 'IKToe.r', 'IKFoot.r', 'IKLegPole.r', 'WeaponHandControl.r', 'WeaponHandControl.l', 'SideWeapon', 'SideWeaponSpinner']
srcArmName = 'Armature'
srcMeshName = 'Bandit2BodyMesh'

meshOffset = None#Vector((0,0,-0.1246846)) # Vector((1, 1, 1))
meshSpecificOffset = None # {'TestMesh': Vector((1, 1, 1))}

meshesScale = None # (1, 1, 1)
meshSpecificScale = None # {'TesMesh': (1, 1, 1)}

excessiveMeshes = [] # ['TestMesh']

applyRestToPose = False

bonesParentOverride = {}#{'hatJiggle2': 'hat', 'hatJiggle3': 'hat', 'hatJiggleSide.l': 'hat', 'hatJiggleSide.r': 'hat'} # {'ChildBone': 'ParentBone'}

bonesTailToHeadOverride = {}#{'stomach': 'chest'} # {'BoneName': 'BoneName'}

modelScale = Vector((1, 1, 1)) # Vector((1, 1, 1))





def RemoveExcessiveMeshes(excessiveMeshes):
    for meshName in excessiveMeshes:
        bpy.data.objects.remove(bpy.data.objects[meshName])    

def CopyEditBones(bones, editBones, offset = None):
    for bone in bones:
        boneCopy = editBones.new(bone.name)
    for bone in bones:
        boneCopy = editBones[bone.name]
        boneCopy.bbone_curveinx = bone.bbone_curveinx
        boneCopy.bbone_curveiny = bone.bbone_curveiny
        boneCopy.bbone_curveoutx = bone.bbone_curveoutx
        boneCopy.bbone_curveouty = bone.bbone_curveouty
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
        boneCopy.bbone_scaleinx = bone.bbone_scaleinx
        boneCopy.bbone_scaleiny = bone.bbone_scaleiny
        boneCopy.bbone_scaleoutx = bone.bbone_scaleoutx
        boneCopy.bbone_scaleouty = bone.bbone_scaleouty
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

def Prepare(srcArmName, applyRestToPose):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')

    roll = srcArm.data.edit_bones[0].roll 
    
    bpy.ops.object.mode_set(mode='OBJECT')
    srcArm.rotation_euler = (radians(90), 0, -roll)
    srcArm.scale = (1,1,1)
    
    if not applyRestToPose:
        bpy.ops.object.mode_set(mode='POSE')
    
        for pbone in srcArm.pose.bones:
            pbone.bone.select = True
    
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()
        bpy.ops.pose.transforms_clear()
    
        bpy.ops.object.mode_set(mode='OBJECT')
    

def PrepareMeshes(srcMeshName, meshParentBones, scale = None, meshOffset = None, meshSpecificScale = None, meshSpecificOffset = None, modelScale = None):
    srcMesh = bpy.data.objects[srcMeshName]
    bpy.context.view_layer.objects.active = srcMesh
    bpy.ops.object.mode_set(mode='OBJECT')
    
    offset = Vector(srcMesh.location)
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        if modelScale is not None and not obj.parent_bone:
            obj.scale = obj.scale * modelScale
            bpy.ops.object.transform_apply({'selected_editable_objects': [obj]}, location = False, scale = True, rotation = False)
        
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

def PrepareBones(bonesOrder, srcArmName, bonesParentOverride, bonesTailToHeadOverride):
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
    
    for bone in srcEditBones:
        if bone.name in bonesParentOverride:
            bone.parent = srcEditBones[bonesParentOverride[bone.name]]
        if bone.name in bonesTailToHeadOverride:
            bone.tail = Vector(srcEditBones[bonesTailToHeadOverride[bone.name]].head)
    
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
        
    for bone in bones:
        if bone.name not in vertexGroupNames:
            bone.use_deform = False
            bone.hide = True
            
        
def FinalizeMeshes(meshParentBones):
    for meshName in meshParentBones:
        bpy.data.objects[meshName].parent_bone = meshParentBones[meshName]

def FinalizePose(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    
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

def Finalize(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    for obj in bpy.data.objects:
        if not (obj.parent == srcArm and obj.parent_type == 'BONE'):
            bpy.ops.object.transform_apply({'selected_editable_objects': [obj]}, location = True, scale = False, rotation = True)

meshParentBones = {}

RemoveExcessiveMeshes(excessiveMeshes)
Prepare(srcArmName, applyRestToPose)
PrepareMeshes(srcMeshName, meshParentBones, meshesScale, meshOffset, meshSpecificScale, meshSpecificOffset, modelScale)
PrepareBones(bonesOrder, srcArmName, bonesParentOverride, bonesTailToHeadOverride)
FinalizeBones(bonesOrder, srcArmName)
FinalizeMeshes(meshParentBones)
FinalizePose(srcArmName)
Finalize(srcArmName)