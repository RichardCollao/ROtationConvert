import bpy
from array import *
import math

class EulerToQuaternion:
    dic = {}
    
    def run(self, action):
        self.dic = {}
        self.action = bpy.data.actions[action]
        # complete dictionary whit tuple bone -> keyframes
        self.getKeyFrames()

        if not bool(self.dic):
            bpy.context.scene.message = "No keyframes found to modify"
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
            return
        else:
            bpy.context.scene.isWorking = True

        for bone in self.dic:
            print("Select bone: ", bone)
            
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.pose.bones[bone].bone.select = True

            for k in self.dic[bone]:
                e = self.getEulers(bone, k)
                angles = self.toEulerAngles(e)
                print("keyframe: ", k)
                print("euler: ", e)
                print("quaternion: ", angles)
            
                # modify rotation of bone
                bpy.context.object.pose.bones[bone].rotation_mode = 'QUATERNION'
                bpy.context.object.pose.bones[bone].rotation_quaternion[0] = angles[0]
                bpy.context.object.pose.bones[bone].rotation_quaternion[1] = angles[1]
                bpy.context.object.pose.bones[bone].rotation_quaternion[2] = angles[2]
                bpy.context.object.pose.bones[bone].rotation_quaternion[3] = angles[3]
                self.insertKey(k)
            # after transform delete curve old
            self.deleteFCurve(bone)
            bpy.context.scene.isWorking = False
          
    def getKeyFrames(self):
        for fcu in self.action.fcurves:
                #print(fcu.data_path + " channel " + str(fcu.array_index))
                if self.isEuler(fcu.data_path):
                    bname = self.getNameFromDataPath(fcu.data_path)
                    colKey = []
                    for keyframe in fcu.keyframe_points:
                        key = int(keyframe.co[0])
                        layer = fcu.array_index
                        val = keyframe.co[1]
                        colKey.append(key)

                    self.dic.setdefault(bname, colKey)
    
    def getEulers(self, n, k):
        e = {}
        for l in [0,1,2]:
            for fcu in self.action.fcurves:
                if self.isEuler(fcu.data_path):
                    bname = self.getNameFromDataPath(fcu.data_path)
                    if n == bname:
                        colKey = []
                        for keyframe in fcu.keyframe_points:
                            key = int(keyframe.co[0])
                            layer = fcu.array_index
                            val = keyframe.co[1]
                            if k == key and l == layer :
                                e.setdefault(l, val)
        return e                         

    def toEulerAngles(self, e):
        # yaw (Z), pitch (Y), roll (X)
        yaw, pitch, roll = 2, 1, 0
        # Abbreviations for the various angular functions
        cy = math.cos(e[yaw] * 0.5)
        sy = math.sin(e[yaw] * 0.5)
        cp = math.cos(e[pitch] * 0.5)
        sp = math.sin(e[pitch] * 0.5)
        cr = math.cos(e[roll] * 0.5)
        sr = math.sin(e[roll] * 0.5)
        
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return [w, x, y, z]

    def insertKey(self, key):
        bpy.context.scene.frame_current = key
        bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualRot')

    def deleteFCurve(self, bone):
        for l in [0,1,2]:
            for f in self.action.fcurves:
                # find X Location fcurve
                if f.data_path.find("rotation_euler") > -1 and self.getNameFromDataPath(f.data_path) == bone:
                    self.action.fcurves.remove(f)
                    print("remove curves from rotation_euler: ", f)
                    break

    def isEuler(self, data_path):
        if data_path.find("rotation_euler") > -1:
            return True
        else:
            return False
            
    def getNameFromDataPath(self, data_path):
        bname = data_path.replace('pose.bones["', '')
        bname = bname.replace('"].rotation_euler', '')
        return bname