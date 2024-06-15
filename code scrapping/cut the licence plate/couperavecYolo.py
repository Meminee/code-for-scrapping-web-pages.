import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

# Charger les labels
labels = open('/home/memine/Téléchargements/archive (1)/classes.names').read().strip().split('\n')
print(labels)

# Chemins des poids et de la configuration
weights_path = '/home/memine/Téléchargements/archive (1)/lapi.weights'
configuration_path = '/home/memine/Téléchargements/archive (1)/darknet-yolov3.cfg'

# Seuils de probabilité et de suppression non maximale (NMS)
probability_minimum = 0.5
threshold = 0.3

# Charger le réseau YOLO
network = cv2.dnn.readNetFromDarknet(configuration_path, weights_path)
layers_names_all = network.getLayerNames()

# Correction pour obtenir les noms des couches de sortie
layers_names_output = [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]

# Fonction pour détecter et couper les plaques d'immatriculation
def detect_and_crop_plate(image_path, output_folder):
    # Charger l'image
    image_input = cv2.imread(image_path)
    if image_input is None:
        print(f"Erreur de chargement de l'image: {image_path}")
        return

    h, w = image_input.shape[:2]

    # Prétraiter l'image pour YOLO
    blob = cv2.dnn.blobFromImage(image_input, 1/255.0, (416, 416), swapRB=True, crop=False)
    network.setInput(blob)
    output_from_network = network.forward(layers_names_output)

    # Initialiser les listes pour les boîtes englobantes, les confidences et les classes détectées
    bounding_boxes = []
    confidences = []
    class_numbers = []

    # Traiter chaque résultat du réseau
    for result in output_from_network:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]

            if confidence_current > probability_minimum:
                box_current = detection[0:4] * np.array([w, h, w, h])
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                class_numbers.append(class_current)

    # Appliquer la suppression non maximale pour éliminer les boîtes redondantes
    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)

    if len(results) > 0:
        for i in results.flatten():
            x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
            box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

            # Découper la plaque détectée
            plate = image_input[y_min:y_min + box_height, x_min:x_min + box_width]

            # Sauvegarder la plaque découpée
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            plate_filename = os.path.join(output_folder, f"{image_name}_plate_{i}.jpg")
            cv2.imwrite(plate_filename, plate)
            print(f"Plaque sauvegardée à: {plate_filename}")
    else:
        print(f"Aucune plaque détectée pour l'image: {image_path}")

# Dossier de sortie pour les plaques découpées
output_folder = '/home/memine/Bureau/RimAi scrap/Done clinning/MarketPlaceAftercouper'
os.makedirs(output_folder, exist_ok=True)

# Dossier d'entrée pour les images
input_folder = '/home/memine/Bureau/RimAi scrap/Done clinning/MarketPlace'

# Traiter toutes les images du dossier d'entrée
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)
        detect_and_crop_plate(image_path, output_folder)
