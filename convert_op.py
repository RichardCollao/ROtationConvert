import bpy
from . to_quaternion import QuaternionToEuler
from . to_euler import EulerToQuaternion
from bpy.props import StringProperty

class Convert_OT_Operator(bpy.types.Operator):
    bl_idname = "convert.operator"
    bl_label = "Simple operator"
    dl_description = "convert to quaternion or euler rotation"

    property = bpy.props.StringProperty()

    def execute(self, context):
        print('RUN.....')

        # clip animation
        action = bpy.context.scene.action

        if len(action) <= 0:
            bpy.context.scene.message = "You must select an action"
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
            return {'FINISHED'}

        if bpy.context.object.mode != "POSE":
            bpy.context.scene.message = "You must be in POSE mode"
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
            return {'FINISHED'}

        if bpy.context.scene.isWorking == True:
            bpy.context.scene.message = "wait for current conversion to finish"
            bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
            return {'FINISHED'}

        if self.property == 'to_quaternion':
            op = QuaternionToEuler()
            op.run(action)
        elif self.property == 'to_euler':
            op = EulerToQuaternion()
            op.run(action)


        return {'FINISHED'}