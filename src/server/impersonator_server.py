import os
import sys
import predictor_worker

from arguments import opt
from utils import Tee


log = Tee('./logs/impersonator_server.log')


if __name__ == "__main__":
    log('Loading Predictor')
    predictor_args = {
        'config_path': opt.config,
        'checkpoint_path': opt.checkpoint,
        'relative': opt.relative,
        'adapt_movement_scale': opt.adapt_scale,
        'enc_downscale': opt.enc_downscale
    }

    predictor_worker.run_worker(opt.in_port, opt.out_port)
    sys.exit(0)
