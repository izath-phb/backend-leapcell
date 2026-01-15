# import numpy as np
# from keras.models import load_model
# from keras.preprocessing import image

# MODEL_PATH = "cnn_model/model.h5"

# model = load_model(MODEL_PATH)

# def predict_body(image_path):
#     img = image.load_img(image_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = img_array / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     prediction = model.predict(img_array)

#     # contoh output softmax 4 kelas
#     classes = ['underweight', 'normal', 'overweight', 'obese']
#     predicted_class = classes[np.argmax(prediction)]

#     return predicted_class