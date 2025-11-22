import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
import os

# ABSOLUTE PATH – EXACT FROM YOUR SYSTEM
DATA_DIR = r"C:/Users/RonakB/Desktop/agriguard/data/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 1   # Only 1 epoch for fast model saving

# Data augmentation + validation split
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.2
)

# Training generator
train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

# Validation generator
val_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# Load MobileNetV2 model pretrained on ImageNet
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)
base_model.trainable = False  # Freeze backbone

# Build classification model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# ABSOLUTE SAVE PATH — WILL 100% WORK
SAVE_PATH = r"C:/Users/RonakB/Desktop/agriguard/model/mobilenet_v2.h5"
model.save(SAVE_PATH)

print(f"\nTraining complete. Model saved to: {SAVE_PATH}")
