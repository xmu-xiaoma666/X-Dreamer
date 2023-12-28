import torch
import os
from render import mesh
from render import render
from render import regularizer
from render import util
from torch.cuda.amp import custom_bwd, custom_fwd 
import numpy as np
import torch.nn.functional as F
import torch.nn as nn


def normalize_camera(camera_data,FLAGS):
    normalized_xyz = torch.sigmoid(camera_data[:, :3]) 
    normalized_xangles = (camera_data[:, 3:4] - (-FLAGS.elevation_range[1])) / (FLAGS.elevation_range[1]-FLAGS.elevation_range[0])
    normalized_yangles = (camera_data[:, 4:5] - (-180)) / 360
    normalized_fov = (camera_data[:, 5:] - np.deg2rad(FLAGS.fovy_range[0])) / (np.deg2rad(FLAGS.fovy_range[1]) - np.deg2rad(FLAGS.fovy_range[0]))
    normalized_data = torch.cat((normalized_xyz, normalized_xangles,normalized_yangles,normalized_fov), dim=1)

    return normalized_data

class SpecifyGradient(torch.autograd.Function):
    @staticmethod
    @custom_fwd
    def forward(ctx, input_tensor, gt_grad):
        ctx.save_for_backward(gt_grad)
        # we return a dummy value 1, which will be scaled by amp's scaler so we get the scale in backward.
        return torch.ones([1], device=input_tensor.device, dtype=input_tensor.dtype)

    @staticmethod
    @custom_bwd
    def backward(ctx, grad_scale):
        gt_grad, = ctx.saved_tensors
        gt_grad = gt_grad * grad_scale
        return gt_grad, None
    
###############################################################################
#  Geometry interface
###############################################################################
class CameraEncoder(nn.Module):
    def __init__(self):
        super(CameraEncoder, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(6, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU()
        )
        
    def forward(self, camera_data):
        encoded_vector = self.encoder(camera_data)
        return encoded_vector


class DLMesh(torch.nn.Module):
    def __init__(self, initial_guess, FLAGS):
        super(DLMesh, self).__init__()
        self.FLAGS = FLAGS
        self.initial_guess = initial_guess
        self.mesh          = initial_guess.clone()
        self.pos_encoder = CameraEncoder().cuda()
        print("Base mesh has %d triangles and %d vertices." % (self.mesh.t_pos_idx.shape[0], self.mesh.v_pos.shape[0]))
        
    @torch.no_grad()
    def getAABB(self):
        return mesh.aabb(self.mesh)

    def getMesh(self, material):
        self.mesh.material = material

        imesh = mesh.Mesh(base=self.mesh)
        # Compute normals and tangent space
        imesh = mesh.auto_normals(imesh)
        imesh = mesh.compute_tangents(imesh)
        return imesh

    def render(self, glctx, target, lgt, opt_material, bsdf=None,if_normal=False, mode = 'appearance_modeling', if_flip_the_normal = False, if_use_bump = False):
        opt_mesh = self.getMesh(opt_material)
        return render.render_mesh(glctx, 
                                  opt_mesh,
                                  target['mvp'],
                                  target['campos'],
                                  lgt,
                                  target['resolution'], 
                                  spp=target['spp'], 
                                  msaa=True,
                                  background= target['background'] ,
                                  bsdf= bsdf,
                                  if_normal=if_normal,
                                  normal_rotate=target['normal_rotate'], 
                                  mode = mode,
                                  if_flip_the_normal = if_flip_the_normal,
                                  if_use_bump = if_use_bump
                                   )

    def tick(self, glctx, target, lgt, opt_material, iteration, if_normal, guidance,  mode, if_flip_the_normal, if_use_bump):
        # ==============================================================================================
        #  Render optimizable object with identical conditions
        # ==============================================================================================
        buffers= self.render(glctx, target, lgt, opt_material, if_normal = if_normal, mode = mode,  if_flip_the_normal = if_flip_the_normal, if_use_bump = if_use_bump)
        if self.FLAGS.add_directional_text:
            text_embeddings = torch.cat([guidance.uncond_z[target['prompt_index']], guidance.text_z[target['prompt_index']]])
            indexs = torch.cat([guidance.uncond_index[target['prompt_index']], guidance.index[target['prompt_index']]]) # [B*2, 77, 1024]
        else:
            text_embeddings = torch.cat([guidance.uncond_z, guidance.text_z])
            indexs = torch.cat([guidance.uncond_index, guidance.index]) # [B*2, 77, 1024]


        if iteration <= self.FLAGS.coarse_iter:
            srgb =  buffers['shaded'][...,0:3]
            srgb = util.rgb_to_srgb(srgb)
            mask = (buffers['shaded'][..., 3:4]).permute(0, 3, 1, 2).contiguous()
            mask2 = mask.squeeze()
            t = torch.randint( guidance.min_step_early, guidance.max_step_early+1, [self.FLAGS.batch], dtype=torch.long, device='cuda') # [B]
        else:
            srgb =   buffers['shaded'][...,0:3]
            srgb = util.rgb_to_srgb(srgb)
            mask = (buffers['shaded'][..., 3:4]).permute(0, 3, 1, 2).contiguous()
            mask2 = mask.squeeze()
            t = torch.randint( guidance.min_step_late, guidance.max_step_late+1, [self.FLAGS.batch], dtype=torch.long, device='cuda') # [B]

        pred_rgb_512 = srgb.permute(0, 3, 1, 2).contiguous() # [1, 3, H, W]
        latents = guidance.encode_imgs(pred_rgb_512)
        
        ### calculate camera pos feature
        came_pos = torch.cat([target['campos'],torch.from_numpy(target['elev']).unsqueeze(-1).cuda(),torch.from_numpy(target['azim']).cuda().unsqueeze(-1),target['fov'].unsqueeze(-1)],dim=-1)
        came_pos = torch.cat([came_pos,came_pos],dim=0) #bs*2, 5
        came_pos = normalize_camera(came_pos,self.FLAGS)
        came_posfeat = self.pos_encoder(came_pos)


        # add noise
        noise = torch.randn_like(latents)
        latents_noisy = guidance.scheduler.add_noise(latents, noise, t)
        # pred noise
        latent_model_input = torch.cat([latents_noisy] * 2)
        tt = torch.cat([t] * 2)
        noise_pred, attention_map = guidance.unet(latent_model_input, tt, encoder_hidden_states= text_embeddings, index=indexs, came_posfeat=came_posfeat)#.sample######################
        noise_pred = noise_pred.sample

        attention_map[0] = attention_map[0].reshape(self.FLAGS.batch*2, 64, 64).contiguous()
        attention_map[1] = attention_map[1].reshape(self.FLAGS.batch*2, 32, 32).contiguous()
        attention_map[2] = attention_map[2].reshape(self.FLAGS.batch*2, 16, 16).contiguous()
        attention_map[3] = attention_map[3].reshape(self.FLAGS.batch*2, 8 , 8 ).contiguous()
        attention_map[4] = attention_map[4].reshape(self.FLAGS.batch*2, 16, 16).contiguous()
        attention_map[5] = attention_map[5].reshape(self.FLAGS.batch*2, 32, 32).contiguous()
        attention_map[6] = attention_map[6].reshape(self.FLAGS.batch*2, 64, 64).contiguous()

        noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
        noise_pred = noise_pred_uncond + guidance.guidance_weight * (noise_pred_text - noise_pred_uncond)
        
        if guidance.sds_weight_strategy == 0:
            w = guidance.alphas[t] ** 0.5 * (1 - guidance.alphas[t])
        elif guidance.sds_weight_strategy == 1:
            w = 1 / (1 - guidance.alphas[t])
        elif guidance.sds_weight_strategy == 2:
            if iteration <= self.FLAGS.coarse_iter:
                w = guidance.alphas[t] ** 0.5 * (1 - guidance.alphas[t])
            else:
                w = 1 / (1 - guidance.alphas[t])
        w = w[:, None, None, None] # [B, 1, 1, 1]
        grad = w* (noise_pred -noise) 
        grad = torch.nan_to_num(grad)
        sds_loss = SpecifyGradient.apply(latents, grad) 
        img_loss = torch.tensor([0], dtype=torch.float32, device="cuda")
        reg_loss = torch.tensor([0], dtype=torch.float32, device="cuda")
        
        attention_loss = 0
        mask_sizes = [(64, 64), (32,32), (16,16), (8,8), (16,16), (32,32), (64,64)]
        for i in range(7):
            _, attention_map_text = attention_map[i].chunk(2)
            if(self.FLAGS.batch==1):
                mask2 =  F.interpolate(mask2.unsqueeze(0).unsqueeze(0), mask_sizes[i], mode='bilinear').squeeze()
            else:
                mask2 =  F.interpolate(mask2.unsqueeze(0), mask_sizes[i], mode='bilinear').squeeze()
            attention_map_text = (attention_map_text - attention_map_text.min())/(attention_map_text.max() - attention_map_text.min()+1e-6)
            attention_map_text = F.interpolate(attention_map_text.unsqueeze(0), size=mask2.shape, mode='bilinear', align_corners=False).squeeze()
            attention_loss = 0.1*F.l1_loss(mask2.float(), attention_map_text.float(), reduction="mean") #0.1  1  10
        attention_loss = attention_loss/7
        
        return sds_loss, img_loss, reg_loss, attention_loss
    