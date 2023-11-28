<p align="center">
  <img width="25%" src="image/logo_name.png"/>
</p>

# X-Dreamer 💤
A pytorch implementation of “X-Dreamer: Creating High-quality 3D Content by Bridging the Domain Gap Between Text-to-2D and Text-to-3D Generation”

[【Paper】](#)  [【Project Page】](https://xmu-xiaoma666.github.io/Projects/X-Dreamer/)

# Introduction Video 🎥
[![Video Name](image/overview.png)](https://private-user-images.githubusercontent.com/33897496/285799664-fc389cff-3f8c-4287-a399-1e48b42603cd.MP4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDEwNzc0ODEsIm5iZiI6MTcwMTA3NzE4MSwicGF0aCI6Ii8zMzg5NzQ5Ni8yODU3OTk2NjQtZmMzODljZmYtM2Y4Yy00Mjg3LWEzOTktMWU0OGI0MjYwM2NkLk1QND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzExMjclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMTI3VDA5MjYyMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTMwMmI0Zjg0YWRiZGY1YmYzOTQ2MWFhZjQwZjZkNDcxN2E1ODEzNjgyYzZjOGNiZWRjZGM5NDUyMTU2OWY3NDMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.QHdxR3l_LPe0AgBXeEUmhRVl3osevGnEyYjRYWfYO5M)



# Overview 💻

<p align="center">
  <img width="80%" src="image/overview.png"/>
</p>
<p astyle="text-align: justify;">Overview of the proposed X-Dreamer, which consists of two main stages: geometry learning and appearance learning.For the geometry learning stage, we employ DMTET as the 3D representation and initialize it with a 3D ellipsoid using the mean squared error (MSE) loss. Subsequently, we optimize DMTET and CG-LoRA using the score distillation sampling (SDS) loss and our proposed attention-mask alignment (AMA) loss to ensure the alignment between the 3D representation and the input text prompt. For the appearance learning, we leverage bidirectional reflectance distribution function (BRDF) modeling. Specifically, we utilize an MLP with trainable parameters to predict surface materials. Similar to the geometry learning stage, we optimize the MLP and CG-LoRA using the SDS loss and the AMA loss to achieve alignment between the 3D representation and the input text prompt.
</p>

# News 📝
**Code is comming soon!!!**
- 2023.11.27: Create Repository


# Results 🔍
[![Video Name](image/overview.png)](https://private-user-images.githubusercontent.com/33897496/285799510-e40e917d-c202-489a-9e2c-f47409e1c879.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDEwNzc0NDIsIm5iZiI6MTcwMTA3NzE0MiwicGF0aCI6Ii8zMzg5NzQ5Ni8yODU3OTk1MTAtZTQwZTkxN2QtYzIwMi00ODlhLTllMmMtZjQ3NDA5ZTFjODc5Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzExMjclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMTI3VDA5MjU0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ0YTc2MTA2ZTQzNjM4ZjliZjZmYjQzYzVkZDMxOTUwYzQ0NzMzYTZlYmI3MTMwZmFhZDJhZWE1NTIzOGEyODUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.T3Xg2-HbWlMeRg5PmEZ7LhUMsc34vFYA6Ij3TYmj2Bg)

## Example generated objects

We conduct the experiments using four Nvidia RTX 3090 GPUs and the PyTorch library. To calculate the SDS loss, we utilize the Stable Diffusion implemented by Hugging Face Diffusers. For the DMT<sub>ET</sub> and material encoder, we implement them as a two-layer MLP and a single-layer MLP, respectively, with a hidden dimension of 32. We optimize X-Dreamer for 2000 iterations for geometry learning and 1000 iterations for appearance learning.

### Text-to-3D generation from an ellipsoid

We present representative results of X-Dreamer for text-to-3D generation, utilizing an ellipsoid as the initial geometry.

| Image | Normal |
| --- | --- |
| ![Vase Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/vase_shaded.gif) | ![Vase Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/vase_normal.gif) |
| --- | --- |
| *A DSLR photo of a blue and white porcelain vase, highly detailed, 8K, HD.* | *A DSLR photo of a blue and white porcelain vase, highly detailed, 8K, HD.* |

| ![Cabbage Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cabbage_shaded.gif) | ![Cabbage Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cabbage_normal.gif) |
| --- | --- |
| *A cabbage, highly detailed.* | *A cabbage, highly detailed.* |

| ![Cupcake Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cupcake_shaded.gif) | ![Cupcake Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cupcake_normal.gif) |
| --- | --- |
| *A chocolate cupcake, highly detailed.* | *A chocolate cupcake, highly detailed.* |

| ![Bread Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/bread_shaded.gif) | ![Bread Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/bread_normal.gif) |
| --- | --- |
| *A sliced loaf of fresh bread.* | *A sliced loaf of fresh bread.* |

| ![Pear Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/pear_shaded.gif) | ![Pear Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/pear_normal.gif) |
| --- | --- |
| *A DSLR photo of a pear, highly detailed, 8K, HD.* | *A DSLR photo of a pear, highly detailed, 8K, HD.* |

| ![Hamburger Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/hamburger_shaded.gif) | ![Hamburger Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/hamburger_normal.gif) |
| --- | --- |
| *A hamburger.* | *A hamburger.* |

| ![Corn Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/corn_shaded.gif) | ![Corn Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/corn_normal.gif) |
| --- | --- |
| *A DSLR photo of a corn, highly detailed, 8K, HD.* | *A DSLR photo of a corn, highly detailed, 8K, HD.* |

### Text-to-3D generation from coarse-grained meshes

X-Dreamer also supports text-based mesh geometry editing and is capable of delivering excellent results.

| Coarse-grained Mesh | Image | Normal |
| --- | --- | --- |
| ![Chess Piece](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/chess.png) | ![Chess Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/chess_shaded.gif) | ![Chess Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/chess_normal.gif) |
| *A beautifully carved wooden queen chess piece.* |
| ![Obama's Head](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/head.png) | ![Obama Shaded](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Obama_shaded.gif) | ![Obama Normal](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Obama1_normal.gif) |
| *Barack Obama's head.* |

# Different lighting conditions

We demonstrate how swapping the HDR environment map results in diverse lighting, thereby creating various reflective effects on the generated 3D assets in X-Dreamer.

## Environment map

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Environment 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/environment0.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Environment 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/environment1.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Environment 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/environment2.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Environment 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/environment3.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Environment 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/environment4.png) |

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Arrow](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/arrow.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Arrow](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/arrow.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Arrow](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/arrow.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Arrow](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/arrow.png) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Arrow](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/arrow.png) |

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Cowboy2 Lit 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cowboy2_lit0.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Cowboy2 Lit 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cowboy2_lit1.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Cowboy2 Lit 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cowboy2_lit2.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Cowboy2 Lit 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cowboy2_lit3.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Cowboy2 Lit 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/cowboy2_lit4.gif) |

A DSLR photo of a brown cowboy hat.

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Messi1 Strategy4 Lit 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Messi1_strategy4_lit0.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Messi1 Strategy4 Lit 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Messi1_strategy4_lit1.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Messi1 Strategy4 Lit 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Messi1_strategy4_lit2.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Messi1 Strategy4 Lit 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Messi1_strategy4_lit3.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Messi1 Strategy4 Lit 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/Messi1_strategy4_lit4.gif) |

Messi's head, highly detailed, 8K, HD.

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Fox1 Lit 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/fox1_lit0.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Fox1 Lit 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/fox1_lit1.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Fox1 Lit 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/fox1_lit2.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Fox1 Lit 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/fox1_lit3.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Fox1 Lit 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/fox1_lit4.gif) |

A DSLR photo of a fox, highly detailed.

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Rose Lit 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/rose_lit0.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Rose Lit 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/rose_lit1.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Rose Lit 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/rose_lit2.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Rose Lit 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/rose_lit3.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Rose Lit 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/rose_lit4.gif) |

A DSLR photo of red rose, highly detailed, 8K, HD.

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![Mouse2 Lit 0](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/mouse2_lit0.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Mouse2 Lit 1](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/mouse2_lit1.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Mouse2 Lit 2](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/mouse2_lit2.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Mouse2 Lit 3](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/mouse2_lit3.gif) | ![White](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/white.png) | ![Mouse2 Lit 4](https://media.githubusercontent.com/media/xmu-xiaoma666/xmu-xiaoma666.github.io/master/Projects/X-Dreamer/static/our_gif/mouse2_lit4.gif) |

A marble bust of a mouse.

| | | | | | | | | |
| --- |

# BibTeX 📚
```
  Comming
```