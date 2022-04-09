#Orignal Creator: KingEnderBrine
#Modified by: RuneFox237
#Version 1.0.1

import bpy
import re
from math import radians
from mathutils import Vector


bonesOrder = ['ROOT', 'base', 'stomach', 'chest', 'clavicle.l', 'upper_arm.l', 'lower_arm.l', 'hand.l', 'finger1.1.l', 'finger1.2.l', 'finger1.3.l', 'finger2.1.l', 'finger2.2.l', 'finger2.3.l', 'finger3.1.l', 'finger3.2.l', 'finger3.3.l', 'finger4.1.l', 'finger4.2.l', 'finger4.3.l', 'thumb.1.l', 'thumb.2.l', 'GripControl.l', 'finger1IKTarget.l', 'finger2IKTarget.l', 'finger3IKTarget.l', 'finger4IKTarget.l', 'thumbIKTarget.l', 'neck', 'head', 'mech.base', 'mech.upper_arm.l', 'mech.lower_arm.l', 'mech.handle.l', 'mech.hand.l', 'mech.hand.end.l', 'mech.finger1.1.l', 'mech.finger1.2.l', 'mech.finger1.3.l', 'mech.finger2.1.l', 'mech.finger2.2.l', 'mech.finger2.3.l', 'mech.finger3.1.l', 'mech.finger3.2.l', 'mech.finger3.3.l', 'mech.thumb.1.l', 'mech.thumb.2.l', 'mech.GripControl.l', 'mech.finger1IKTarget.l', 'mech.finger2IKTarget.l', 'mech.finger3IKTarget.l', 'mech.thumbIKTarget.l', 'mech.hydraulictarget.l', 'mech.hydraulic.base.l', 'mech.hydraulic.piston.l', 'mech.upper_arm.r', 'mech.lower_arm.r', 'mech.handle.r', 'mech.hand.r', 'mech.hand.end.r', 'mech.finger1.1.r', 'mech.finger1.2.r', 'mech.finger1.3.r', 'mech.finger2.1.r', 'mech.finger2.2.r', 'mech.finger2.3.r', 'mech.finger3.1.r', 'mech.finger3.2.r', 'mech.finger3.3.r', 'mech.thumb.1.r', 'mech.thumb.2.r', 'mech.GripControl.r', 'mech.finger1IKTarget.r', 'mech.finger2IKTarget.r', 'mech.finger3IKTarget.r', 'mech.thumbIKTarget.r', 'mech.hydraulictarget.r', 'mech.hydraulic.base.r', 'mech.hydraulic.piston.r', 'clavicle.r', 'upper_arm.r', 'lower_arm.r', 'hand.r', 'finger1.1.r', 'finger1.2.r', 'finger1.3.r', 'finger2.1.r', 'finger2.2.r', 'finger2.3.r', 'finger3.1.r', 'finger3.2.r', 'finger3.3.r', 'finger4.1.r', 'finger4.2.r', 'finger4.3.r', 'thumb.1.r', 'thumb.2.r', 'GripControl.r', 'finger1IKTarget.r', 'finger2IKTarget.r', 'finger3IKTarget.r', 'finger4IKTarget.r', 'thumbIKTarget.r', 'pelvis', 'thigh.l', 'calf.l', 'foot.l', 'toe.l', 'thigh.r', 'calf.r', 'foot.r', 'toe.r', 'IKArmTarget.l', 'IKArmPole.l', 'mech.IKArmTarget.l', 'mech.IKArmPole.l', 'IKArmTarget.r', 'IKArmPole.r', 'mech.IKArmTarget.r', 'mech.IKArmPole.r', 'HeelRoll.l', 'ToeRoll.l', 'FootRoll.l', 'IKLegTarget.l', 'ToeControl.l', 'IKToe.l', 'IKFoot.l', 'IKLegPole.l', 'HeelRoll.r', 'ToeRoll.r', 'FootRoll.r', 'IKLegTarget.r', 'ToeControl.r', 'IKToe.r', 'IKFoot.r', 'IKLegPole.r']
srcArmName = 'Armature'
srcMeshName = 'LoaderMechMesh'

meshOffset = Vector((0, 1.3, 0)) # Vector((1, 1, 1))
meshSpecificOffset = {'LoaderMechMesh': Vector((0, 1.3, 0))} # {'TestMesh'=Vector((1, 1, 1))}

meshesScale = (1,1,1) # (1, 1, 1)
meshSpecificScale = {'LoaderMechMesh': (0.5,0.5,0.5)} # {'TesMesh'=(1, 1, 1)}

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