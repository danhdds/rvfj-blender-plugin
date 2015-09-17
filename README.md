# rvjf-blender-plugin
This is a plugin for blender, it add videos listed in a json file.

given the json object:

{
"stream0" : {
"startPoint" : "00:00:00.00",
"file" : "videos\/a.mp4"
},
"stream1" : {
"startPoint" : "00:00:03.00",
"file" : "videos\/b.mp4"
},
"stream2" : {
"startPoint" : "00:00:05.00",
"file" : "videos\/c.mp4"
}
}

the plugin reads the video in sequence adding them to the video editor with the starting points on each chanel been 

the "startPoint" and the video been "a, b and c" stored in a sub directory(related to the json file) called videos.
