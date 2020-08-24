import bpy

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Property Example"

    def draw(self,context):
        layout = self.layout
        layout.label(text=context.scene.message, icon='INFO')
        #return
        
    def execute(self, context):
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self)

bpy.utils.register_class(DialogOperator)


# test call
#message = "Debe estar en "
#bpy.ops.object.dialog_operator('INVOKE_DEFAULT')