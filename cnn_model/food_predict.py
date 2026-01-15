# import numpy as np
# from keras.models import load_model
# from keras.preprocessing import image

# MODEL_PATH = "cnn_model/food_model.h5"
# LABEL_PATH = "cnn_model/food_labels.txt"

# model = load_model(MODEL_PATH)

# with open(LABEL_PATH, "r") as f:
#     labels = [line.strip() for line in f.readlines()]

# def predict_food(image_path):
#     img = image.load_img(image_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = img_array / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     preds = model.predict(img_array)
#     class_index = np.argmax(preds)
#     confidence = float(np.max(preds))

#     return labels[class_index], round(confidence * 100, 2)
