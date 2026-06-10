"""EfficientNetB0 feature execution framework engine."""

import logging
from typing import Optional
import numpy as np
import tensorflow as tf
from agrivision.config import settings
from agrivision.utils.image_utils import validate_and_parse_image

logger = logging.getLogger("agrivision.models.classifier")


class CropDiseaseClassifier:
    """Encapsulates the computer vision pipeline inside a class model abstraction."""

    def __init__(self) -> None:
        """Initializes the base inference architecture configuration wrapper."""
        self.model: Optional[tf.keras.Model] = None
        self.classes = settings.CLASS_NAMES

    def load_model_weights(self) -> None:
        """Dynamically initializes or pulls local weight binaries into memory."""
        try:
            # Build core graph blueprint foundation layout dynamically
            base_model = tf.keras.applications.EfficientNetB0(
                include_top=False,
                weights=None,
                input_shape=(224, 224, 3)
            )
            base_model.trainable = False
            pooled_layers = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
            classification_heads = tf.keras.layers.Dense(
                len(self.classes), 
                activation='softmax'
            )(pooled_layers)
            
            self.model = tf.keras.Model(inputs=base_model.input, outputs=classification_heads)
            logger.info("EfficientNetB0 neural runtime layer successfully configured.")
        except Exception as err:
            logger.critical(f"Fatal compilation structural sequence halt: {str(err)}")
            raise err

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """Transforms binary streams into standard multi-dimensional tensor representations."""
        parsed_image = validate_and_parse_image(image_bytes)
        resized_target = parsed_image.resize((224, 224))
        raw_float_matrix = np.array(resized_target, dtype=np.float32)
        
        # Apply standard EfficientNet pre-processing equations
        preprocessed_tensor = tf.keras.applications.efficientnet.preprocess_input(raw_float_matrix)
        expanded_batch_tensor = np.expand_dims(preprocessed_tensor, axis=0)
        return expanded_batch_tensor

    def predict(self, image_bytes: bytes) -> dict:
        """Performs optimized statistical classification across model target classes."""
        if self.model is None:
            raise RuntimeError("Inference processing requested on an uninitialized classifier graph model.")
        
        try:
            tensor = self.preprocess(image_bytes)
            raw_predictions = self.model.predict(tensor, verbose=0)[0]
            
            top_index = int(np.argmax(raw_predictions))
            predicted_label = self.classes[top_index]
            confidence_score = float(raw_predictions[top_index])
            
            score_distribution = {
                self.classes[i]: float(raw_predictions[i]) for i in range(len(self.classes))
            }
            
            return {
                "label": predicted_label,
                "confidence": confidence_score,
                "all_scores": score_distribution
            }
        except Exception as err:
            logger.error(f"Pipeline processing execution crash: {str(err)}")
            return {
                "label": "Unknown",
                "confidence": 0.0,
                "all_scores": {c: 0.0 for c in self.classes}
            }