"""
rvfj Plugin
Creative Commons 2015 Danilo Abreu (danhdds)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "rvfj Plugin",
    "author": "Danilo Abreu (danhdds)",
    "version": (0, 0, 1),
    "blender": (2, 7, 5),
    "location": "Video Editor >> Properties Panel >> rvfj Plugin",
    "description": "Allows the user to select a directory, and it adds the videos listed on a JSON file in the directory to the Video editor.",
    "category": "Tools"
}

import bpy
import random
import os
import json

class rvfjPanel(bpy.types.Panel):
    """rvfj Addon Panel"""
    bl_category = "rvfj Plugin"
    bl_idname = "tools.rvfj_panel"
    bl_context = "objectmode"
    bl_label = "rvfj Plugin"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        directory = context.scene.rvfj_directory_path
        
        layout = self.layout
        
        row = layout.row()
        row.label(text = "Read a JSON file")
        row = layout.row()
        row.prop(context.scene, "rvfj_directory_path", text="")
        
        row = layout.row()
        
        #Display information about the selected directory       
        if directory == "":
            row.label(text = "Choose a directory")
        else:
            #Check if it is a path
            if os.path.exists(os.path.dirname(directory)):
                
                compatible_files = ('.json')
                
                file_list = []
                for f in os.listdir(directory):
                    if f.endswith(compatible_files):
                        file_list.append(f)
                row.label(text = "Number of files: " + str(len(file_list)))
            else:
                row.label(text = "Invalid Path")
        
        row = layout.row()
        
        layout.separator()
        row = layout.row()
        
        #options
        split = layout.split()
        col = split.column(align = True)
        col.prop(context.scene, "rvfj_clear_sequencer")
        row = layout.row()
        row = layout.row()
        row.operator("tools.rvfj_addon")
        

class rvfj(bpy.types.Operator):
    """Add files to the Video Sequence Editor using the values above"""
    bl_idname = "tools.rvfj_addon"
    bl_label = "Add files from JSON to Video Editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #Get the files from the directory, based on file type
        path = context.scene.rvfj_directory_path
        
        file_list = []
        startPoint = []
        for f in os.listdir(path):
            if f.endswith('.json'):
                with open(path+f) as data_file:
                    data = json.load(data_file)
                    for i in range(0, len(data)):
                        file_list.append((data["stream"+str(i)]["file"]))
                        s = data["stream"+str(i)]["startPoint"]
                        hourToSec = (int(s[0:2])) * 3600
                        minToSec = (int(s[3:5])) * 60
                        sec = float(s[6:11])                            
                        startPoint.append((hourToSec + minToSec + sec) * 25) # formula seconds to FPS
                
        for item in file_list:
            print(item)
            
        strips = []
        
        for strip in file_list:
            strips.append(os.path.join(path, strip)) #if you prefer to ref. the full pathway to videos, the full pathway should be configured using strips.append(ostrip) strip only.

        #Add the strips
        bpy.context.area.type = 'SEQUENCE_EDITOR'
        
        if context.scene.rvfj_clear_sequencer:
            bpy.context.scene.sequence_editor_clear()

        channel_offset = 0
        strip_number = 1

        for i in range(0, len(strips)):
            
            channel_offset += 1
            #offset = startPoint[i]
            bpy.ops.sequencer.movie_strip_add(filepath = strips[i], frame_start = startPoint[i], channel = channel_offset)
            #Make into meta strip
            bpy.ops.sequencer.meta_make()
            
            #Rename for easy selecting
            bpy.context.selected_sequences[0].name = str(strip_number)            
            
            strip_number += 1
            
        return {'FINISHED'}
        
def register():
    bpy.utils.register_class(rvfj)
    bpy.utils.register_class(rvfjPanel)    
    bpy.types.Scene.rvfj_clear_sequencer = bpy.props.BoolProperty(name="Clear Sequencer", description="Clear the sequencer before running", default = True)
    bpy.types.Scene.rvfj_directory_path = bpy.props.StringProperty(name="Directory", description="Choose the folder where the JSON files are located", default="", subtype='DIR_PATH')

def unregister():
    bpy.utils.unregister_class(rvfj)
    bpy.utils.unregister_class(rvfjPanel)
    
if __name__ == "__main__":
    register()
