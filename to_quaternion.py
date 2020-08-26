import bpy
from array import *
import math

class QuaternionToEuler:
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

        for bone in self.dic:
            print("Select bone: ", bone)
            
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.pose.bones[bone].bone.select = True
            
            for k in self.dic[bone]:
                q = self.getQuaternions(bone, k)
                angles = self.toEulerAngles(q)
                degress = [math.degrees(angles[0]), math.degrees(angles[1]), math.degrees(angles[2])]
                print("keyframe: ", k)
                print("quaternion: ", q)
                print("to_euler degress: ", degress)

                # modify rotation of bone
                bpy.context.object.pose.bones[bone].rotation_mode = 'XYZ'
                bpy.context.object.pose.bones[bone].rotation_euler[0] = angles[0]
                bpy.context.object.pose.bones[bone].rotation_euler[1] = angles[1]
                bpy.context.object.pose.bones[bone].rotation_euler[2] = angles[2]
                self.insertKey(k)
            # after transform delete curve old
            self.deleteFCurve(bone)
          
    def getKeyFrames(self):
        for fcu in self.action.fcurves:
                #print(fcu.data_path + " channel " + str(fcu.array_index))
                if self.isQuaternion(fcu.data_path):
                    bname = self.getNameFromDataPath(fcu.data_path)
                    colKey = [] #BASURA
                    for keyframe in fcu.keyframe_points:
                        key = int(keyframe.co[0])
                        layer = fcu.array_index
                        val = keyframe.co[1]
                        colKey.append(key)

                    self.dic.setdefault(bname, colKey)
                    
    def getQuaternions(self, n, k):
        q = {}
        for l in [0,1,2,3]:
            for fcu in self.action.fcurves:
                if self.isQuaternion(fcu.data_path):
                    bname = self.getNameFromDataPath(fcu.data_path)
                    if n == bname:
                        colKey = [] #BASURA
                        for keyframe in fcu.keyframe_points:
                            key = int(keyframe.co[0])
                            layer = fcu.array_index
                            val = keyframe.co[1]
                            if k == key and l == layer :
                                q.setdefault(l, val)
        return q                          

    def toEulerAngles(self, q):
        w, x, y, z = 0, 1, 2, 3
        
        # roll (x-axis rotation)
        sinr_cosp = 2 * (q[w] * q[x] + q[y] * q[z])
        cosr_cosp = 1 - 2 * (q[x] * q[x] + q[y] * q[y])
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sinp = 2 * (q[w] * q[y] - q[z] * q[x])
        if (abs(sinp) >= 1):
            pitch = math.copysign(M_PI / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # yaw (z-axis rotation)
        siny_cosp = 2 * (q[w] * q[z] + q[x] * q[y])
        cosy_cosp = 1 - 2 * (q[y] * q[y] + q[z] * q[z])
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return [roll, pitch, yaw]

    def insertKey(self, key):
        bpy.context.scene.frame_current = key
        bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualRot')

    def deleteFCurve(self, bone):
        for l in [0,1,2,3]:
            for f in self.action.fcurves:
                # find X Location fcurve
                if f.data_path.find("rotation_quaternion") > -1 and self.getNameFromDataPath(f.data_path) == bone:
                    self.action.fcurves.remove(f)
                    print("remove curves from rotation_quaternion: ", f)
                    break

    def isQuaternion(self, data_path):
        if data_path.find("rotation_quaternion") > -1:
            return True
        else:
            return False
            
    def getNameFromDataPath(self, data_path):
        bname = data_path.replace('pose.bones["', '')
        bname = bname.replace('"].rotation_quaternion', '')
        return bname