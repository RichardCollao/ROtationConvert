import bpy 
from . convert_op import Convert_OT_Operator
from . dialog_op import DialogOperator
from bpy.props import StringProperty

class MainPanel(bpy.types.Panel):
    bl_idname = "Main Panel"
    bl_label = "Rotation convert"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'View'
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        layout.label(text="Rotation convert", icon='ARMATURE_DATA')
        layout.prop(scene, "action")
        layout.separator()
        layout.operator(Convert_OT_Operator.bl_idname, text="Quaternion to Euler XYZ").property = 'to_quaternion'
        layout.operator(Convert_OT_Operator.bl_idname, text="Euler to Quaternion WXYZ").property = 'to_euler'

    def arma_items(self, context):
        print("arma_items")
        obs = []
        for ob in context.scene.objects:
            if ob.type == 'ARMATURE':
                obs.append((ob.name, ob.name, ""))
        return obs

    def actions_items(self, context):
        actions = bpy.data.actions
        if actions is None:
            return
        return [(action.name, action.name, "") for action in bpy.data.actions]


classes = (
    Convert_OT_Operator, MainPanel
)

def register():
    for clss in classes:
        bpy.utils.register_class(clss)
    bpy.types.Scene.action = bpy.props.EnumProperty(items=MainPanel.actions_items)

def unregister():
    for clss in classes:
        bpy.utils.unregister_class(clss)

if __name__ == "__main__":
    register()

bpy.types.Scene.message = StringProperty(default="")