import face_alignment
import numpy as np
import torch
import yaml

from scipy.spatial import ConvexHull
# FOMM modules
from animate import normalize_kp
from modules.keypoint_detector import KPDetector
from modules.generator_optim import OcclusionAwareGenerator
from sync_batchnorm import DataParallelWithCallback


def to_tensor(arr):
    return torch.tensor(arr[np.newaxis].astype(np.float32)).permute(0, 3, 1, 2) / 255


class PredictorLocal:
    def __init__(self, config_path, checkpoint_path, relative=False, adapt_movement_scale=False, device=None, enc_downscale=1):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.relative = relative
        self.adapt_movement_scale = adapt_movement_scale
        self.start_frame = None
        self.start_frame_kp = None
        self.kp_driving_initial = None
        self.config_path = config_path
        self.checkpoint_path = checkpoint_path
        self.generator, self.kp_detector = self.load_generator_and_keypoint_detector()
        self.fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=True, device=self.device)
        self.source = None
        self.kp_source = None
        self.enc_downscale = enc_downscale

    def get_start_frame(self):
        return self.start_frame

    def get_start_frame_kp(self):
        return self.start_frame_kp

    def reset_frames(self):
        self.kp_driving_initial = None

    def load_config(self):
        with open(self.config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return config

    def load_checkpoints(self):
        return torch.load(self.checkpoint_path, map_location=self.device)

    def load_generator_and_keypoint_detector(self):
        config = self.load_config()
        generator = OcclusionAwareGenerator(
            **config['model_params']['generator_params'],
            **config['model_params']['common_params']
        )
        generator.to(self.device)
        kp_detector = KPDetector(
            **config['model_params']['kp_detector_params'],
            **config['model_params']['common_params']
        )
        kp_detector.to(self.device)

        checkpoints = self.load_checkpoints()
        generator.load_state_dict(checkpoints['generator'])
        kp_detector.load_state_dict(checkpoints['kp_detector'])

        generator.eval()
        kp_detector.eval()

        return generator, kp_detector

    def set_source_image(self, source_image):
        self.source = to_tensor(source_image).to(self.device)
        self.kp_source = self.kp_detector(self.source)

        if self.enc_downscale > 1:
            h, w = int(self.source.shape[2] / self.enc_downscale), int(self.source.shape[3] / self.enc_downscale)
            source_enc = torch.nn.functional.interpolate(self.source, size=(h, w), mode='bilinear')
        else:
            source_enc = self.source

        self.generator.encode_source(source_enc)

    def predict(self, driving_frame):
        assert self.kp_source is not None, "call set_source_image()"

        with torch.no_grad():
            driving = to_tensor(driving_frame).to(self.device)

            if self.kp_driving_initial is None:
                self.kp_driving_initial = self.kp_detector(driving)
                self.start_frame = driving_frame.copy()
                self.start_frame_kp = self.get_normalized_frame_kp(driving_frame)

            kp_driving = self.kp_detector(driving)
            kp_norm = normalize_kp(
                kp_source=self.kp_source,
                kp_driving=kp_driving,
                kp_driving_initial=self.kp_driving_initial,
                use_relative_movement=self.relative,
                use_relative_jacobian=self.relative,
                adapt_movement_scale=self.adapt_movement_scale
            )

            prediction = self.generator(self.source, kp_source=self.kp_source, kp_driving=kp_norm)

            output = np.transpose(prediction['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0]
            output = (np.clip(output, 0, 1) * 255).astype(np.uint8)

            return output

    def get_normalized_frame_kp(self, image):
        kp_landmarks = self.fa.get_landmarks(image)

        if kp_landmarks:
            kp = kp_landmarks[0] - kp_landmarks[0].mean(axis=0, keepdims=True)
            area = np.sqrt(ConvexHull(kp[:, :2]).volume)
            kp[:, :2] = kp[:, :2] / area
            return kp
        else:
            return None
