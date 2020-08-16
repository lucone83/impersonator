SERVER_IMAGE := impersonator-server
SERVER_HOST := 127.0.0.1

WEIGHTS_FOLDER := src/server/weights/
WEIGHTS_URL := https://storage.googleapis.com/impersonator-model-weights/current/vox-adv-cpk.pth.tar


##############################
# Data
##############################
.PHONY: download-model-weights
download-model-weights:
	mkdir -p $(WEIGHTS_FOLDER)
	wget $(WEIGHTS_URL) -P $(WEIGHTS_FOLDER)


##############################
# Build
##############################

.PHONY: server-build
server-build:
	docker build --rm -f docker/server/Dockerfile -t $(SERVER_IMAGE) .

.PHONY: client-linux-create-vcam
client-linux-create-vcam:
	./src/client/bin/create_vistual_camera.sh


##############################
# Run
##############################

.PHONY: server-run
server-run:
	docker run --gpus all --rm -it -p 5557:5557 -p 5558:5558 $(SERVER_IMAGE)

.PHONY: server-run-nogpu
server-run-nogpu:
	docker run --rm -it -p 5557:5557 -p 5558:5558 $(SERVER_IMAGE)

.PHONY: client-run
client-run:
	kill -9 $(ps aux | grep 'impersonator_client.py' | awk '{print $2}') 2> /dev/null
	./src/client/bin/run_client.sh --in-addr tcp://$(SERVER_HOST):5557 --out-addr tcp://$(SERVER_HOST):5558


##############################
# Shell
##############################

.PHONY: server-run-shell
server-run-shell:
	docker run --rm -it \
		-p 5557:5557 \
		-p 5558:5558 \
		$(SERVER_IMAGE) \
		/bin/bash
