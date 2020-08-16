FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

ENV FOMM_CONFIG=fomm/config/vox-adv-256.yaml
ENV FOMM_CKPT=weights/vox-adv-cpk.pth.tar

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qqy install python3.7 python3-pip python3-tk ffmpeg libsm6 libxext6 libxrender-dev libgtk2.0 v4l2loopback-dkms && \
    rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 0 && \
    update-alternatives --set python /usr/bin/python3.7

COPY docker/server/requirements.txt /tmp/server-requirements.txt
COPY src/server /home/app
COPY src/common/*.py /home/app/

WORKDIR /home/app

RUN python -m pip install --upgrade pip
RUN python -m pip install -r /tmp/server-requirements.txt

ENV PYTHONPATH="/home/app/:/home/app/fomm:${PYTHONPATH}"

EXPOSE 5557
EXPOSE 5558

CMD ["python",  "impersonator_server.py", "--config", "${FOMM_CONFIG}", "--checkpoint", "${FOMM_CKPT}", "--relative", "--adapt_scale"]
