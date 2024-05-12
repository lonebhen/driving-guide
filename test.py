
# def image_processing(img_path):
#     try:
#         # Load the pre-trained model
#         model = load_model('./model/TSR.h5')

#         # Load and preprocess the image
#         image = Image.open(img_path)
#         image = image.resize((30, 30))  # Resize the image to match model input size
#         image_array = np.array(image)   # Convert image to numpy array
#         X_test = np.expand_dims(image_array, axis=0)  # Add batch dimension

#         # Normalize the input (if required based on model training)
#         # Example: X_test = X_test / 255.0  # Normalize pixel values to [0, 1]

#         # Make predictions
#         predict_x = model.predict(X_test)
#         classes_x = np.argmax(predict_x, axis=1)

#         return classes_x[0]  # Return the predicted class (assuming single image input)

#     except Exception as e:
#         print(f"Error during image processing: {e}")
#         return None