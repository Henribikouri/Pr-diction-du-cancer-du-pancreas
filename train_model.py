import os
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Définir le chemin vers le dossier contenant les images
data_dir = 'datasets'

# Fonction pour charger les images
def load_images(image_dir):
    images = []
    labels = []
    for file_name in os.listdir(image_dir):
        if file_name.endswith('.png'):  # Filtrer uniquement les fichiers PNG
            label = "cancer" if "cancer" in file_name.lower() else "non_cancer"
            img_path = os.path.join(image_dir, file_name)
            image = load_img(img_path, target_size=(224, 224))  # Redimensionner
            image_array = img_to_array(image) / 255.0  # Normalisation
            images.append(image_array)
            labels.append(label)
    return np.array(images), np.array(labels)

# Charger les images et leurs étiquettes
x_train_dir = os.path.join(data_dir, 'x_train')
x_test_dir = os.path.join(data_dir, 'x_test')
y_train_dir = os.path.join(data_dir, 'y_train')
y_test_dir = os.path.join(data_dir, 'y_test')

X_train, Y_train = load_images(x_train_dir)
X_test, Y_test = load_images(x_test_dir)

# Encodage des étiquettes
encoder = LabelEncoder()
Y_train = encoder.fit_transform(Y_train)
Y_test = encoder.transform(Y_test)

# Convertir les étiquettes en format catégoriel
Y_train = to_categorical(Y_train, num_classes=2)
Y_test = to_categorical(Y_test, num_classes=2)

# Charger un modèle pré-entraîné (EfficientNetB0)
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Geler les couches du modèle pré-entraîné

# Ajouter des couches personnalisées
x = Flatten()(base_model.output)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(2, activation='softmax')(x)  # Deux classes : cancer et non_cancer

model = Model(inputs=base_model.input, outputs=output)

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Afficher le résumé du modèle
model.summary()

# Entraîner le modèle
history = model.fit(
    X_train,
    Y_train,
    validation_data=(X_test, Y_test),
    epochs=20,
    batch_size=32
)

# Sauvegarder le modèle
model_path = "cancer_detection_model.h5"
model.save(model_path)
print(f"Modèle sauvegardé à {model_path}")

# Évaluation
test_loss, test_accuracy = model.evaluate(X_test, Y_test)
print(f"Test Accuracy: {test_accuracy:.2f}")
