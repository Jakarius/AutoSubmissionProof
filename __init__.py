
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, FloatProperty, EnumProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from datetime import datetime
from os import linesep

class AutoSubmissionProofPreferences(AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __package__

    username: StringProperty(
        name = "Discord Username"
    )

    thickness: FloatProperty(
        name = "Default Thickness",
        default = 4.0
    )

    dateformat: EnumProperty(
        name = "Date Format",
        items = [
            ('%d/%m/%y', 'UK/EU: dd/mm/yyyy', ''),
            ('%m/%d/%y', 'US: mm/dd/yyyy', '')
        ]
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "username")
        layout.prop(self, "thickness")
        layout.prop(self, "dateformat")


def add_object(self, context):
    my_prefs = bpy.context.preferences.addons[__package__].preferences
    my_username = my_prefs.username

    my_date_string = datetime.now().strftime(my_prefs.dateformat)
        
    text_curve = bpy.data.curves.new(type="FONT", name="Submission Proof")

    text_curve.body = my_username + linesep + my_date_string
    text_curve.extrude = my_prefs.thickness
    text_obj = bpy.data.objects.new(name="SubmissionProof", object_data=text_curve)


    bpy.context.scene.collection.objects.link(text_obj)


class OBJECT_OT_add_object(Operator):
    """Create a thick text object with discord username and today's date"""
    bl_idname = "curves.auto_submission_proof"
    bl_label = "Add Submission Proof"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Submission Proof",
        icon='OUTLINER_OB_FONT')

def register():
    bpy.utils.register_class(AutoSubmissionProofPreferences)

    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(AutoSubmissionProofPreferences)
    
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
