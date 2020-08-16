from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("--config", help="path to config")
parser.add_argument("--checkpoint", default='vox-cpk.pth.tar', help="path to checkpoint to restore")
parser.add_argument("--relative", dest="relative", action="store_true", help="use relative or absolute keypoint coordinates")
parser.add_argument("--adapt_scale", dest="adapt_scale", action="store_true", help="adapt movement scale based on convex hull of keypoints")
parser.add_argument("--enc_downscale", default=1, type=float, help="Downscale factor for encoder input. Improves performance with cost of quality.")
parser.add_argument("--verbose", action="store_true", help="Print additional information")
parser.add_argument("--in-port", type=int, default=5557, help="Remote worker input port")
parser.add_argument("--out-port", type=int, default=5558, help="Remote worker output port")
parser.add_argument("--jpg_quality", type=int, default=95, help="Jpeg copression quality for image transmission")

parser.set_defaults(relative=False)
parser.set_defaults(adapt_scale=False)
parser.set_defaults(no_pad=False)

opt = parser.parse_args()
