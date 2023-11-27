<p align="center">
  <img width="25%" src="image/logo_name.png"/>
</p>

# X-Dreamer 💤
A pytorch implementation of “X-Dreamer: Creating High-quality 3D Content by Bridging the Domain Gap Between Text-to-2D and Text-to-3D Generation”

[【Paper】](#)  [【Project Page】](#)

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



# BibTeX 📚
```
  Comming
```