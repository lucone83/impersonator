# impersonator

**Impersonator** is a ML-based software providing photorealistic avatars for videoconferencing applications.

This software is a fork of an open-source project called [_Avatarify_](https://github.com/alievk/avatarify) based on a machine learning model called [First Order Motion Model](https://github.com/AliaksandrSiarohin/first-order-model) (FOMM).

It aims to have a better separation of concerns between server and client side and simplifies the installation of the server.


## Requirements

### Server
- The server part is meant to work with a machine having a CUDA-enabled NVIDIA GPU. It's possible to run it without it, but keep in mind that it will become much slower. Some examples of performance with common GPUs are:
  - GeForce GTX 1080 Ti: **33 frames per second**;
  - GeForce GTX 1070: **15 frames per second**;
  - GeForce GTX 950: **9 frames per second**;
- Docker up and running (and [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) for GPU machines);
- Expose ports 5557 and 5558 and make sure they are reachable from the machine where the client will be running;

A Linux machine is recommended for hosting the server (tested myself with a GCP instance with GPU).

### Client
The client has been tested only with MacOS and Linux (Ubuntu) platforms;
In order to run the client you need a conda environment:

- Install [anaconda](https://docs.anaconda.com/anaconda/install/);
- Create a conda environment with Python 3.7 and install requirements `pip install -r src/client/requirements.txt`;
- Activate your environment before running;
- Change the `SERVER_HOST` parameter on `Makefile` according to where you want to run the server;

#### Linux (Ubuntu):
Besides your "phisical" webcams you might need a virtual camera. From the root folder of the project, run:

```bash
make client-linux-create-vcam
```

#### Mac:
Download and install [CamTwist](http://camtwiststudio.com/) to create your virtual camera. You can download it from [here](http://camtwiststudio.com/download).


## How to run
At first you need to download the model weights. Just run

```bash
make download-model-weights
```

from the root folder of the project.

### Server
Just build and run the docker image. From the root filder of the project:

```bash
make server-build
make server-run
```

You can also run a version without GPU support:

```bash
make server-run-nogpu
```

### Client

Given you have activated your _conda_ environment, run:

```bash
make client-run
```

## Use impersonator with your favorite VC app

This software should support any video-conferencing app where video input source can be changed (Zoom, Skype, Hangouts, Slack, ...).

### Mac
**Mac** requires a further configuration to turn [CamTwist](http://camtwiststudio.com/) into a virtual camera:

1. Go to CamTwist.
2. Choose `Desktop+` and press `Select`.
3. In the `Settings` section choose `Confine to Application Window` and select `python (impersonator)` from the drop-down menu.


## Citations

```
@misc{alievk,
  author = {Ali Aliev},
  title = {Avatarify},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/alievk/avatarify}},
}

@InProceedings{Siarohin_2019_NeurIPS,
  author={Siarohin, Aliaksandr and Lathuilière, Stéphane and Tulyakov, Sergey and Ricci, Elisa and Sebe, Nicu},
  title={First Order Motion Model for Image Animation},
  booktitle = {Conference on Neural Information Processing Systems (NeurIPS)},
  month = {December},
  year = {2019}
}
```
