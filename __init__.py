# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "rotation_convert",
    "author" : "richard",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "VIEW_3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

#from . convert_op import Convert_OT_Operator
from . main_panel import MainPanel 


def register():
	#MainPanel.register()
    main_panel.register()

def unregister():
	#MainPanel.unregister()
    main_panel.register()