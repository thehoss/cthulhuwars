
'''
Arnold Render Module

To setup for arnold rendering download the Arnold SDK from https://www.solidangle.com/arnold/download/
Install the SDK anywhere
eg /usr/local/solidangle/arnold

In PyCharm settings add the arnold bin and python directories
to the "project:cthulhuwars"->"project structure" list of content roots

/usr/local/solidangle/arnold/bin
/usr/local/solidangle/arnold/python

If you want kick (to render ass files) available at command line
you will need to add /usr/local/solidangle/arnold/bin to the path
'''
import random
from arnold import *
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Unit import Unit, UnitState, UnitType

class ArnoldRender(object):
    earth_gate_positions = {'Arctic Ocean': [0.03, 0.9], 'North Atlantic': [-0.23, 0.57],
                            'South Atlantic': [-0.05, 0.24], 'Indian Ocean': [0.69, 0.21],
                            'North Pacific': [-0.9, 0.54], 'South Pacific': [-0.53, 0.09],
                            'North America': [-0.58, 0.7], 'South America': [-0.33, 0.28],
                            'North America West': [-0.63, 0.75], 'North America East': [-0.36, 0.72],
                            'South America East': [-0.24, 0.31], 'South America West': [-0.4, 0.29],
                            'Central America': [-0.66, 0.55], 'Australia': [-0.9, 0.2],
                            'New Zealand': [-0.69, 0.25], 'Antarctica': [-0.025, 0.06],
                            'Africa': [0.21, 0.47], 'East Africa': [0.43, 0.25],
                            'West Africa': [0.21, 0.47], 'Europe': [0.37, 0.71],
                            'Scandinavia': [0.38, 0.87], 'Arabia': [0.56, 0.47], 'Asia': [0.68, 0.75],
                            'North Asia': [0.75, 0.79], 'South Asia': [0.85, 0.55]
                            }

    def __init__(self, basename):
        self._base_name = basename
        self._file_ext = '.ass'
        self._image_ext = '.png'

    def render_loop(self):
        result = AiRender(AI_RENDER_MODE_CAMERA)
        return result

    def render_unit(self, unit, prefix, color, position):
        assert isinstance(unit, Unit)
        render_def = unit.render_unit()

        shader = AiNode('standard')
        shader_name = str(prefix) + '_mtl_' + str(render_def['name'][0])
        AiNodeSetStr(shader, 'name', shader_name )
        AiNodeSetRGB(shader, 'Kd_color', unit.faction._node_color[0], unit.faction._node_color[1], unit.faction._node_color[2])
        AiNodeSetFlt(shader, 'Kd', 0.2)
        AiNodeSetFlt(shader, 'Ks', 1)
        AiNodeSetFlt(shader, 'specular_roughness', 0.35)
        AiNodeSetBool(shader, 'specular_Fresnel', True)
        AiNodeSetFlt(shader, 'Ksn', 0.015)
        AiNodeSetFlt(shader, 'Ksss', 0.8)
        AiNodeSetRGB(shader, 'Ksss_color', unit.faction._node_color[0], unit.faction._node_color[1], unit.faction._node_color[2])
        AiNodeSetRGB(shader, 'sss_radius', 0.03, 0.03, 0.03)

        unit_obj = AiNode(render_def['nodetype'][0])
        AiNodeSetStr(unit_obj, 'name', prefix + '_' + str(render_def['name'][0]))
        unit_parameters = render_def['params']

        for param in unit_parameters:
            param_type = param[0]
            param_name = param[1]
            if param_type == 'string':
                AiNodeSetStr(unit_obj, param_name, str(param[2]))
            if param_type == 'float':
                AiNodeSetFlt(unit_obj, param_name, float(param[2]))
            if param_type == 'bool':
                AiNodeSetBool(unit_obj, param_name, bool(param[2]))
            if param_type == 'int':
                AiNodeSetInt(unit_obj, param_name, int(param[2]))

        AiNodeSetPtr(unit_obj, "shader", shader)

        m = AtMatrix()
        AiM4Translation(m, AtVector(position[0], position[1], position[2]))
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, m)
        AiNodeSetArray(unit_obj, "matrix", am)

    def nodesphere(self, name, color, position):
        sphere = AiNode('sphere')
        AiNodeSetStr(sphere, 'name', name)
        AiNodeSetPnt(sphere, 'center', position[0], position[1], position[2] )
        AiNodeSetFlt(sphere, 'radius', position[3])

        shader = AiNode('standard')
        AiNodeSetStr(shader, 'name', 'sphere_mtl_%s'%name)
        AiNodeSetRGB(shader, 'Kd_color', color[0], color[1], color[2])
        AiNodeSetFlt(shader, 'Kd', 2)
        AiNodeSetFlt(shader, 'Ks', 1)
        AiNodeSetFlt(shader, 'specular_roughness', 0.15)
        AiNodeSetBool(shader, 'specular_Fresnel', True)
        AiNodeSetFlt(shader, 'Ksn', 0.4)
        AiNodeSetPtr(sphere, "shader", shader)

    def render_gate(self, name, centerX, centerY, centerZ):
        polymesh = AiNode('polymesh')
        gate_size = 0.08
        AiNodeSetStr(polymesh, "name", name)
        nsides = [4]
        AiNodeSetArray(polymesh, "nsides", AiArrayConvert(len(nsides), 1, AI_TYPE_UINT, (c_uint * len(nsides))(*nsides)))
        vidxs = [0, 1, 2, 3]
        AiNodeSetArray(polymesh, "vidxs", AiArrayConvert(len(vidxs), 1, AI_TYPE_UINT, (c_uint * len(vidxs))(*vidxs)))
        nidxs = [0, 1, 2, 3]
        AiNodeSetArray(polymesh, "nidxs", AiArrayConvert(len(nidxs), 1, AI_TYPE_UINT, (c_uint * len(nidxs))(*nidxs)))
        vlist = [-1.0 * gate_size, 0.0, -1.0 * gate_size, -1.0 * gate_size, 0.0, 1.0 * gate_size, 1.0 * gate_size, 0.0, 1.0 * gate_size, 1.0 * gate_size, 0.0, -1.0 * gate_size]
        AiNodeSetArray(polymesh, "vlist", AiArrayConvert(len(vlist), 1, AI_TYPE_FLOAT, (c_float * len(vlist))(*vlist)))
        nlist = [1]
        AiNodeSetArray(polymesh, "nlist", AiArrayConvert(len(nlist), 1, AI_TYPE_FLOAT, (c_float * len(nlist))(*nlist)))
        uvidxs = [3, 0, 1, 2]
        AiNodeSetArray(polymesh, "uvidxs", AiArrayConvert(len(vidxs), 1, AI_TYPE_UINT, (c_uint * len(uvidxs))(*uvidxs)))
        uvlist = [0, 0,
                  1, 0,
                  1, 1,
                  0, 1]
        AiNodeSetArray(polymesh, "uvlist", AiArrayConvert(len(uvlist), 1, AI_TYPE_FLOAT, (c_float * len(uvlist))(*uvlist)))

        m = AtMatrix(1, 0, 0, 0,
                     0, 1, 0, 0,
                     0, 0, 1, 0,
                     0, 0, 0, 1)
        AiM4Translation(m, AtVector(centerX, centerY, centerZ))
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, m)
        AiNodeSetArray(polymesh, "matrix", am)
        AiNodeSetBool(polymesh, "smoothing", True)
        AiNodeSetByte(polymesh, "visibility", 255)
        AiNodeSetBool(polymesh, "opaque", False)

        # Assign a shader to the polymesh node
        shader = AiNode("utility")
        image = AiNode("image")
        opacity = AiNode("image")

        AiNodeSetStr(shader, "name", 'aiUtility_%s'%name)
        AiNodeSetInt(shader, "shade_mode", 1)
        AiNodeSetStr(image, "name", 'aiImage_C_%s'%name)
        AiNodeSetStr(image, "filename", 'gate.png')

        AiNodeSetStr(opacity, "name", 'aiImage_O_%s' % name)
        AiNodeSetStr(opacity, "filename", 'gate.png')
        AiNodeSetByte(opacity, "start_channel", AtByte(3))
        AiNodeSetBool(opacity, "single_channel", True)

        AiNodeLink(image, "color", shader)
        AiNodeLink(opacity, "opacity", shader)

        AiNodeSetPtr(polymesh, "shader", shader)
        return True

    def _boardHalf(self, name, texture, centerX, centerY, centerZ):
        polymesh = AiNode('polymesh')
        AiNodeSetStr(polymesh, "name", name)
        nsides = [4]
        AiNodeSetArray(polymesh, "nsides", AiArrayConvert(len(nsides), 1, AI_TYPE_UINT, (c_uint * len(nsides))(*nsides)))

        vidxs = [0, 1, 2, 3]
        AiNodeSetArray(polymesh, "vidxs", AiArrayConvert(len(vidxs), 1, AI_TYPE_UINT, (c_uint * len(vidxs))(*vidxs)))

        nidxs = [0, 1, 2, 3]
        AiNodeSetArray(polymesh, "nidxs", AiArrayConvert(len(nidxs), 1, AI_TYPE_UINT, (c_uint * len(nidxs))(*nidxs)))

        vlist = [-1, 0, -1, -1, 0, 1, 1, 0, 1, 1, 0, -1]
        AiNodeSetArray(polymesh, "vlist", AiArrayConvert(len(vlist), 1, AI_TYPE_FLOAT, (c_float * len(vlist))(*vlist)))

        nlist = [1]
        AiNodeSetArray(polymesh, "nlist", AiArrayConvert(len(nlist), 1, AI_TYPE_FLOAT, (c_float * len(nlist))(*nlist)))

        uvidxs = [3, 0, 1, 2]
        AiNodeSetArray(polymesh, "uvidxs", AiArrayConvert(len(vidxs), 1, AI_TYPE_UINT, (c_uint * len(uvidxs))(*uvidxs)))

        uvlist = [0, 0,
                  1, 0,
                  1, 1,
                  0, 1]
        AiNodeSetArray(polymesh, "uvlist", AiArrayConvert(len(uvlist), 1, AI_TYPE_FLOAT, (c_float * len(uvlist))(*uvlist)))

        m = AtMatrix(1, 0, 0, 0,
                     0, 1, 0, 0,
                     0, 0, 1, 0,
                     0, 0, 0, 1)
        AiM4Translation(m, AtVector(centerX, centerY, centerZ))
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, m)

        AiNodeSetArray(polymesh, "matrix", am)

        AiNodeSetBool(polymesh, "smoothing", True)

        AiNodeSetByte(polymesh, "visibility", 255)

        # Assign a shader to the polymesh node
        shader = AiNode("utility")
        image = AiNode("image")

        AiNodeSetStr(shader, "name", 'aiUtility_%s'%name)
        AiNodeSetInt(shader, "shade_mode", 1)
        AiNodeSetStr(image, "name", 'aiImage_%s'%name)
        AiNodeSetStr(image, "filename", texture)

        AiNodeLink(image, "color", shader)
        AiNodeSetPtr(polymesh, "shader", shader)

    def _build_board(self):
        self._boardHalf("west", "earth3PWH.jpg", -1, 0, 0)
        self._boardHalf("east", "earth5PEH.jpg", 1, 0, 0)

    def do_render(self, frame, map):
        AiBegin()
        AiMsgSetConsoleFlags(AI_LOG_ALL)

        outputFileName = "%s%s" % (self._base_name, self._file_ext)
        imageFileName = "%s%s" % (self._base_name, self._image_ext)

        AiMsgInfo('Cthulhu Wars!')

        options = AiNode('options')
        AiNodeSetInt(options, 'AA_samples', 3)
        AiNodeSetInt(options, 'xres', 960)
        AiNodeSetInt(options, 'yres', 540)
        AiNodeSetFlt(options, 'texture_gamma', 2.2)
        AiNodeSetFlt(options, 'light_gamma', 2.2)
        AiNodeSetFlt(options, 'shader_gamma', 2.2)
        AiNodeSetInt(options, 'GI_diffuse_depth', 1)
        AiNodeSetInt(options, 'GI_glossy_depth', 1)

        #TODO: REMOVE hard coded paths
        AiNodeSetStr(options, 'texture_searchpath', 'C:/Users/Adam Martinez/PycharmProjects/cthulhuwars/tex')
        camera = AiNode('persp_camera')
        AiNodeSetStr(camera, 'name', 'theCamera')
        AiNodeSetFlt(camera, 'fov', 100)

        skydome = AiNode("skydome_light")
        AiNodeSetFlt(skydome, 'exposure', 3.5)
        sky     = AiNode("sky")
        sky_image = AiNode("image")

        AiNodeSetStr(sky, "name", "sky_env")
        AiNodeSetStr(skydome, "name", "skydome")
        AiNodeSetStr(sky_image, "name", "sky_image")

        AiNodeSetStr(sky_image, "filename", "CGSkies_0061_free.tx")
        AiNodeLink(sky_image, "color", skydome)
        AiNodeLink(sky_image, "color", sky)
        AiNodeSetRGB(sky_image, "multiply", 1, 1, 1)
        AiNodeSetInt(sky, 'format', 2)
        AiNodeSetInt(skydome, 'format', 2)
        AiNodeSetInt(skydome, 'samples', 3)

        # Matrix transform copied from maya. Cant seem to get this to work the way I want using AI calls
        m = AtMatrix( 0.768283546, 0, -0.640109718, 0,
                    -0.426140219, 0.746192694, -0.511469364, 0,
                    0.477645189, 0.66573, 0.573287547, 0,
                    1.36623037, 1.57795513, 1.57900488, 1)
        #AiM4Translation(m, AtVector(0, 0, 0))
        #AiM4RotationX(m, -10)

        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)

        AiArraySetMtx(am, 0, m)
        AiNodeSetArray(camera, "matrix", am)

        AiNodeSetPtr(options, 'camera', camera)

        driver = AiNode('driver_png')
        AiNodeSetStr(driver, 'name', 'scenerender')
        AiNodeSetStr(driver, 'filename', imageFileName)

        filter = AiNode('gaussian_filter')
        AiNodeSetFlt(filter, 'width', 3)
        AiNodeSetStr(filter, 'name', 'scenefilter')
        AiNodeSetPtr(options, 'background', sky)
        outputString = AiArrayAllocate(1, 1, AI_TYPE_STRING)
        AiArraySetStr(outputString, 0, "RGBA RGBA scenefilter scenerender")
        AiNodeSetArray(options, 'outputs', outputString )
        self._build_board()
        n = 0
        for node in map.node:
            pos = self.earth_gate_positions[node]
            zone = map.node[node]['zone']
            assert isinstance(zone, Zone)
            spherepos = (pos[0]*2 , 0.002, 1.0-(pos[1]*2), 0.05)

            if zone.gate_state is not GateState.noGate:
                self.render_gate(zone.name.replace(" ","_"), spherepos[0], spherepos[1], spherepos[2])
            p = 0
            for unit in zone.occupancy_list:
                if unit.unit_state is UnitState.in_play:
                    if unit.gate_state is GateState.occupied:
                        unitspherepos = (spherepos[0], 0.002, spherepos[2])
                    else:
                        unitspherepos = (
                                         spherepos[0] + 0.1*(math.sin(p)),
                                         0,
                                         spherepos[2] + 0.1*(math.cos(p))
                                         )

                    #self.nodesphere(str(unit.faction._name+'%04d'%n),unit.faction._node_color, unitspherepos)
                    self.render_unit(unit, '%04d'%n, unit.faction._node_color, unitspherepos)
                    p += 1
                    n += 1

        AiASSWrite(outputFileName, AI_NODE_ALL, False)
        #AiRender(AI_RENDER_MODE_CAMERA)

        AiEnd()