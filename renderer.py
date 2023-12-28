import os
import argparse
import json
import numpy as np
import torch
import nvdiffrast.torch as dr
from geometry.dlmesh_01mse_came_fixbug5_multiatt8 import DLMesh
from render import material
from render import mesh
from render import light
from render import util
import cv2
import pickle


def get_camera_params(resolution= 512, fov=45, elev_angle=-45, azim_angle=250):
    fovy   = np.deg2rad(fov)
    elev = np.radians( elev_angle )
    azim = np.radians( azim_angle )
    proj_mtx = util.perspective(fovy, resolution /resolution, 1, 50)
    mv     = util.translate(0, 0, -3) @ (util.rotate_x(elev) @ util.rotate_y(azim))
    normal_rotate = util.rotate_y_1(0)
    # nomral_rotate =  util.rotate_y_1(0) @ util.rotate_x_1(0)
    mvp    = proj_mtx @ mv
    campos = torch.linalg.inv(mv)[:3, 3]
    bkgs = torch.ones(1, resolution, resolution, 3, dtype=torch.float32, device='cuda')
    return {
        'mvp' : mvp[None, ...].cuda(),
        'mv' : mv[None, ...].cuda(),
        'campos' : campos[None, ...].cuda(),
        'resolution' : [resolution, resolution],
        'spp' : 1,
        'background' : bkgs,
        'normal_rotate' : normal_rotate[None,...].cuda(),
        }
def validate_itr(glctx, target, geometry, opt_material, lgt, FLAGS, relight=None, display=None):
    result_dict = {}
    with torch.no_grad():
        if FLAGS.mode == 'appearance_modeling':
            with torch.no_grad():
                lgt.build_mips()
                if FLAGS.camera_space_light:
                    lgt.xfm(target['mv'])
                if relight != None:
                    relight.build_mips()
        buffers = geometry.render(glctx, target, lgt, opt_material, if_use_bump=FLAGS.if_use_bump)
        result_dict['shaded'] = buffers['shaded'][0, ..., 0:3]
        result_dict['shaded'] = util.rgb_to_srgb(result_dict['shaded'])
        if relight != None:
            result_dict['relight'] = \
            geometry.render(glctx, target, relight, opt_material, if_use_bump=FLAGS.if_use_bump)['shaded'][0, ..., 0:3]
            result_dict['relight'] = util.rgb_to_srgb(result_dict['relight'])
        result_dict['mask'] = (buffers['shaded'][0, ..., 3:4])
        result_image = result_dict['shaded']

        if display is not None:
            # white_bg = torch.ones_like(target['background'])
            for layer in display:
                if 'latlong' in layer and layer['latlong']:
                    if isinstance(lgt, light.EnvironmentLight):
                        result_dict['light_image'] = util.cubemap_to_latlong(lgt.base, FLAGS.display_res)
                    result_image = torch.cat([result_image, result_dict['light_image']], axis=1)
                # elif 'relight' in layer:
                #     if not isinstance(layer['relight'], light.EnvironmentLight):
                #         layer['relight'] = light.load_env(layer['relight'])
                #     img = geometry.render(glctx, target, layer['relight'], opt_material)
                #     result_dict['relight'] = util.rgb_to_srgb(img[..., 0:3])[0]
                #     result_image = torch.cat([result_image, result_dict['relight']], axis=1)
                elif 'bsdf' in layer:
                    buffers = geometry.render(glctx, target, lgt, opt_material, bsdf=layer['bsdf'],
                                              if_use_bump=FLAGS.if_use_bump)
                    if layer['bsdf'] == 'kd':
                        result_dict[layer['bsdf']] = util.rgb_to_srgb(buffers['shaded'][0, ..., 0:3])
                    elif layer['bsdf'] == 'normal':
                        result_dict[layer['bsdf']] = (buffers['shaded'][0, ..., 0:3] + 1) * 0.5
                    else:
                        result_dict[layer['bsdf']] = buffers['shaded'][0, ..., 0:3]
                    result_image = torch.cat([result_image, result_dict[layer['bsdf']]], axis=1)

        return result_image, result_dict



@torch.no_grad()
def validate(glctx, geometry, opt_material, lgt, target, out_dir, FLAGS, relight=None, display=None):


    os.makedirs(out_dir, exist_ok=True)


    result_image, result_dict = validate_itr(glctx, target, geometry, opt_material, lgt, FLAGS, relight, display)
    for k in result_dict.keys():
        np_img = result_dict[k].detach().cpu().numpy()
        if k == 'shaded':
            util.save_image(out_dir + '/' + 'shaded.png', np_img)
        elif k == 'relight':
            util.save_image(out_dir + '/' + 'relight.png', np_img)
        elif k == 'kd':
            util.save_image(out_dir + '/' + 'kd.png', np_img)
        elif k == 'ks':
            util.save_image(out_dir + '/' + 'ks.png', np_img)
        elif k == 'normal':
            util.save_image(out_dir + '/' + 'normal.png', np_img)
        elif k == 'mask':
            cv2.imwrite(out_dir + '/' + 'mask.png', np_img)
            # util.save_image(out_dir + '/' + 'mask.png', np_img)
    return 0
def renderer(glctx, load_path, FLAGS, save_path,display,lgt,load_material_path):
    base_mesh = mesh.load_mesh(load_path)
    geometry = DLMesh(base_mesh, FLAGS)
    # mat = base_mesh.material
    with open(load_material_path, 'rb') as f:
        materials = pickle.load(f)
    mat = material.Material({'kd_ks_normal' : materials})
    mat['bsdf'] = 'pbr'
    if FLAGS.mode == 'geometry_modeling':
        pass
    elif FLAGS.mode == 'appearance_modeling':
        if FLAGS.relight != None:
            relight = light.load_env(FLAGS.relight, scale=FLAGS.env_scale)
        else:
            relight = None
    target = get_camera_params(
        resolution=512,
        fov=45,
        elev_angle=-35,
        azim_angle=129.6,
    )
    validate(glctx, geometry, mat, lgt, target, save_path, FLAGS, relight, display)



    return
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='nvdiffrec')
    parser.add_argument('--config', type=str, default=None, help='Config file')
    parser.add_argument('-i', '--iter', type=int, default=5000)
    parser.add_argument('-b', '--batch', type=int, default=1)
    parser.add_argument('-s', '--spp', type=int, default=1)
    parser.add_argument('-l', '--layers', type=int, default=1)
    parser.add_argument('-r', '--train-res', nargs=2, type=int, default=[512, 512])
    parser.add_argument('-dr', '--display-res', type=int, default=None)
    parser.add_argument('-tr', '--texture-res', nargs=2, type=int, default=[1024, 1024])
    parser.add_argument('-si', '--save-interval', type=int, default=1000, help="The interval of saving an image")
    parser.add_argument('-vi', '--video_interval', type=int, default=10,
                        help="The interval of saving a frame of the video")
    parser.add_argument('-mr', '--min-roughness', type=float, default=0.08)
    parser.add_argument('-mip', '--custom-mip', action='store_true', default=False)
    parser.add_argument('-rt', '--random-textures', action='store_true', default=False)
    parser.add_argument('-bg', '--train_background', default='black',
                        choices=['black', 'white', 'checker', 'reference'])
    parser.add_argument('-o', '--out-dir', type=str, default=None)
    parser.add_argument('-rm', '--ref_mesh', type=str)
    parser.add_argument('-bm', '--base-mesh', type=str, default=None)
    parser.add_argument('--validate', type=bool, default=True)
    parser.add_argument("--local_rank", type=int, default=0, help="For distributed training: local_rank")
    parser.add_argument("--seed", type=int, default=42, help="A seed for reproducible training.")
    parser.add_argument("--add_directional_text", action='store_true', default=False)
    parser.add_argument('--mode', default='geometry_modeling', choices=['geometry_modeling', 'appearance_modeling'])
    parser.add_argument('--text', default=None, help="text prompt")
    parser.add_argument('--sdf_init_shape', default='ellipsoid', choices=['ellipsoid', 'cylinder', 'custom_mesh'])
    parser.add_argument('--camera_random_jitter', type=float, default=0.4,
                        help="A large value is advantageous for the extension of objects such as ears or sharp corners to grow.")
    parser.add_argument('--fovy_range', nargs=2, type=float, default=[25.71, 45.00])
    parser.add_argument('--elevation_range', nargs=2, type=int, default=[-10, 45],
                        help="The elevatioin range must in [-90, 90].")
    parser.add_argument("--guidance_weight", type=int, default=100, help="The weight of classifier-free guidance")
    parser.add_argument("--sds_weight_strategy", type=int, nargs=1, default=0, choices=[0, 1, 2],
                        help="The strategy of the sds loss's weight")
    parser.add_argument("--translation_y", type=float, nargs=1, default=0,
                        help="translation of the initial shape on the y-axis")
    parser.add_argument("--coarse_iter", type=int, nargs=1, default=1000,
                        help="The iteration number of the coarse stage.")
    parser.add_argument('--early_time_step_range', nargs=2, type=float, default=[0.02, 0.5],
                        help="The time step range in early phase")
    parser.add_argument('--late_time_step_range', nargs=2, type=float, default=[0.02, 0.5],
                        help="The time step range in late phase")
    parser.add_argument("--sdf_init_shape_rotate_x", type=int, nargs=1, default=0,
                        help="rotation of the initial shape on the x-axis")
    parser.add_argument("--if_flip_the_normal", action='store_true', default=False,
                        help="Flip the x-axis positive half-axis of Normal. We find this process helps to alleviate the Janus problem.")
    parser.add_argument("--front_threshold", type=int, nargs=1, default=45,
                        help="the range of front view would be [-front_threshold, front_threshold")
    parser.add_argument("--if_use_bump", type=bool, default=True,
                        help="whether to use perturbed normals during appearing modeling")
    parser.add_argument("--uv_padding_block", type=int, default=4, help="The block of uv padding.")
    FLAGS = parser.parse_args()
    FLAGS.mtl_override = None  # Override material of model
    FLAGS.dmtet_grid = 64  # Resolution of initial tet grid. We provide 64, 128 and 256 resolution grids. Other resolutions can be generated with https://github.com/crawforddoran/quartet
    FLAGS.mesh_scale = 2.1  # Scale of tet grid box. Adjust to cover the model

    FLAGS.env_scale = 1.0  # Env map intensity multiplier
    FLAGS.envmap = None  # HDR environment probe
    FLAGS.relight = None  # HDR environment probe(relight)
    FLAGS.display = None  # Conf validation window/display. E.g. [{"relight" : <path to envlight>}]
    FLAGS.camera_space_light = False  # Fixed light in camera space. This is needed for setups like ethiopian head where the scanned object rotates on a stand.
    FLAGS.lock_light = False  # Disable light optimization in the second pass
    FLAGS.lock_pos = False  # Disable vertex position optimization in the second pass
    FLAGS.pre_load = True  # Pre-load entire dataset into memory for faster training
    FLAGS.kd_min = [0.0, 0.0, 0.0, 0.0]  # Limits for kd
    FLAGS.kd_max = [1.0, 1.0, 1.0, 1.0]
    FLAGS.ks_min = [0.0, 0.08, 0.0]  # Limits for ks
    FLAGS.ks_max = [1.0, 1.0, 1.0]
    FLAGS.nrm_min = [-1.0, -1.0, 0.0]  # Limits for normal map
    FLAGS.nrm_max = [1.0, 1.0, 1.0]
    FLAGS.cam_near_far = [1, 50]
    FLAGS.learn_light = False
    FLAGS.gpu_number = 1
    FLAGS.sdf_init_shape_scale = [1.0, 1.0, 1.0]
    # FLAGS.local_rank = 0
    FLAGS.multi_gpu = "WORLD_SIZE" in os.environ and int(os.environ["WORLD_SIZE"]) > 1

    if FLAGS.multi_gpu:
        FLAGS.gpu_number = int(os.environ["WORLD_SIZE"])
        FLAGS.local_rank = int(os.environ["LOCAL_RANK"])
        torch.distributed.init_process_group(backend="nccl", world_size=FLAGS.gpu_number, rank=FLAGS.local_rank)
        torch.cuda.set_device(FLAGS.local_rank)

    if FLAGS.config is not None:
        data = json.load(open(FLAGS.config, 'r'))
        for key in data:
            FLAGS.__dict__[key] = data[key]

    # if FLAGS.display_res is None:
    #     FLAGS.display_res = FLAGS.train_res
    # if FLAGS.out_dir is None:
    #     FLAGS.out_dir = 'out/cube_%d' % (FLAGS.train_res)
    # else:
    #     FLAGS.out_dir = 'out/' + FLAGS.out_dir

    # if FLAGS.local_rank == 0:
    #     print("Config / Flags:")
    #     print("---------")
    #     for key in FLAGS.__dict__.keys():
    #         print(key, FLAGS.__dict__[key])
    #     print("---------")
    #
    # seed_everything(FLAGS.seed, FLAGS.local_rank)

    os.makedirs(FLAGS.out_dir, exist_ok=True)

    # glctx = dr.RasterizeGLContext()
    glctx = dr.RasterizeCudaContext()
    # ==============================================================================================
    #  Create data pipeline
    # ==============================================================================================
    # dataset_train = DatasetMesh(glctx, FLAGS, validate=False)
    # dataset_validate = DatasetMesh(glctx, FLAGS, validate=True)
    # dataset_gif = DatasetMesh(glctx, FLAGS, gif=True)

    # ==============================================================================================
    #  Create env light with trainable parameters
    # ==============================================================================================
    if FLAGS.mode == 'appearance_modeling' and FLAGS.base_mesh is not None:
        if FLAGS.learn_light:
            lgt = light.create_trainable_env_rnd(512, scale=0.0, bias=1)
        else:
            lgt = light.load_env(FLAGS.envmap, scale=FLAGS.env_scale)
    else:
        lgt = None
    load_path = FLAGS.base_mesh
    # load_path = '/data/mayiwei/Code/3DStyle/Fantasia3D_CVPR24_final/results/result_XDreamer_alllayer_cglora_lr_grad/mesh.obj'
    load_material_path = os.path.join(FLAGS.out_dir, "material.pkl")
    save_path = os.path.join(FLAGS.out_dir, 'change_view')
    display = [{"bsdf" : "kd"}, {"bsdf" : "ks"}, {"bsdf" : "normal"}]
    renderer(glctx, load_path, FLAGS, save_path, display, lgt,load_material_path)