import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from keras.preprocessing.image import img_to_array
import pickle
from flask import Flask, render_template, url_for, request
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array, array_to_img
from keras.preprocessing import image
import sqlite3
import shutil




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('userlog.html')



@app.route('/userlog.html')
def userlogg():
    return render_template('userlog.html')



@app.route('/graph.html', methods=['GET', 'POST'])
def graph():
    
    images = ['http://127.0.0.1:5000/static/accuracy_plot.png',
              'http://127.0.0.1:5000/static/loss_plot.png',
              'http://127.0.0.1:5000/static/confusion_matrix.png']
    content=['Accuracy Graph',
             'Loss Graph',
             'Confusion Matrix']

            
    
        
    return render_template('graph.html',images=images,content=content)
    


@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
 
        dirPath = "static/images"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
        fileName=request.form['filename']
        dst = "static/images"
        
        

        shutil.copy("upload/"+fileName, dst)
        image = cv2.imread("upload/"+fileName)
        
        #color conversion
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('static/gray.jpg', gray_image)
        #apply the Canny edge detection
        edges = cv2.Canny(image, 250, 254)
        cv2.imwrite('static/edges.jpg', edges)
        #apply thresholding to segment the image
        retval2,threshold2 = cv2.threshold(gray_image,128,255,cv2.THRESH_BINARY)
        cv2.imwrite('static/threshold.jpg', threshold2)
         # # create the sharpening kernel
        kernel_sharpening = np.array([[-1,-1,-1],
                                     [-1, 9,-1],
                                    [-1,-1,-1]])

        # # apply the sharpening kernel to the image
        sharpened =cv2.filter2D(image, -1, kernel_sharpening)

        # save the sharpened image
        cv2.imwrite('static/sharpened.jpg', sharpened)

       
        
        
        
        model=load_model('poul.h5')
        path='static/images/'+fileName


        # Load the class names
        with open('class_names.pkl', 'rb') as f:
            class_names = pickle.load(f)
        rem=""
        rem1=""
        # Function to preprocess the input image
        def preprocess_input_image(path):
            img = load_img(path, target_size=(150,150))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0  # Normalize the image
            return img_array

        # Function to make predictions on a single image
        def predict_single_image(path):
            input_image = preprocess_input_image(path)
            prediction = model.predict(input_image)
            print(prediction)
            predicted_class_index = np.argmax(prediction)
            predicted_class = class_names[predicted_class_index]
            confidence = prediction[0][predicted_class_index]

            print(f"Predicted Class: {predicted_class}")
            print(f"Confidence: {confidence:.2%}")
                
            return predicted_class, confidence 

        predicted_class, confidence = predict_single_image(path)
        #predicted_class, confidence = predict_single_image(path, model, class_names)
        causes=""
        symptoms=""
        precautions=""
        remedies=""
        print(predicted_class, confidence)
        if predicted_class == 'cocci':
            str_label = "Coccidiosis"
            causes = [
                "Caused by protozoan parasites (Eimeria species) that infect the intestines of poultry.",
                "Spread through contaminated feed, water, or litter."
            ]
            symptoms = [
                "Bloody droppings and diarrhea.",
                "Reduced feed intake and poor weight gain.",
                "Lethargy and ruffled feathers."
            ]
            precautions = [
                "Maintain dry litter and good ventilation.",
                "Avoid overcrowding in poultry houses.",
                "Regularly clean and disinfect drinkers and feeders."
            ]
            remedies = [
                "Add coccidiostats (e.g., Amprolium) in feed or water as prescribed by a vet.",
                "Isolate infected birds immediately.",
                "Provide electrolyte and vitamin supplements to aid recovery."
            ]

        elif predicted_class == 'healthy':
            str_label = "Healthy"
            causes = ["No disease detected."]
            symptoms = ["Birds are active, have bright eyes, and eat normally."]
            precautions = [
                "Maintain a balanced diet and clean water supply.",
                "Ensure proper vaccination and regular health check-ups.",
                "Keep poultry housing clean, dry, and well-ventilated."
            ]
            remedies = ["No specific treatment required. Continue regular care and hygiene."]

        elif predicted_class == 'ncd':
            str_label = "Newcastle Disease (NCD)"
            causes = [
                "Caused by Newcastle disease virus (Paramyxovirus).",
                "Spread through direct contact, contaminated feed, water, and equipment."
            ]
            symptoms = [
                "Coughing, sneezing, and nasal discharge.",
                "Twisting of the neck (torticollis) and paralysis.",
                "Drop in egg production and sudden death."
            ]
            precautions = [
                "Vaccinate chicks and adult birds as per schedule.",
                "Avoid contact with wild birds or new unquarantined flocks.",
                "Disinfect equipment and maintain strict biosecurity."
            ]
            remedies = [
                "There is no specific cure; provide supportive care.",
                "Administer multivitamins and electrolytes.",
                "Consult a veterinarian immediately for outbreak management."
            ]

        elif predicted_class == 'salmo':
            str_label = "Salmonellosis"
            causes = [
                "Caused by Salmonella bacteria (S. pullorum, S. gallinarum).",
                "Spread through contaminated feed, water, or infected eggs."
            ]
            symptoms = [
                "Weakness, drooping wings, and diarrhea.",
                "Poor growth and sudden chick mortality.",
                "Reduced egg production in adults."
            ]
            precautions = [
                "Ensure eggs and feed are from Salmonella-free sources.",
                "Disinfect incubators, waterers, and housing regularly.",
                "Avoid feeding spoiled or contaminated food."
            ]
            remedies = [
                "Use antibiotics like Enrofloxacin or Sulfa drugs as prescribed by a vet.",
                "Provide electrolyte and vitamin supplements.",
                "Cull severely infected birds to prevent spread."
            ]

            try:
                from serial_test import Send
                if predicted_class in ["salmo","ncd","cocci"]:
                    Send("A")

                else:
                    Send("B")
            except:
                print("Hardware not connected")
                    
                    

            
                
       
           
            
        accuracy = f"The predicted image is {str_label} with a confidence of {confidence:.2%}"
       
            

       


        return render_template('results.html', 
                               status=str_label,
                               accuracy=accuracy,
                               causes1=causes,
                               symptoms1=symptoms,
                               Remedies1=remedies,
                               precautions1=precautions,
                              
                               ImageDisplay="http://127.0.0.1:5000/static/images/"+fileName)
        
    return render_template('userlog.html')


@app.route('/live')
def live():
    dirPath = "static/images"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath + "/" + fileName)

    vs = cv2.VideoCapture(0)
    while True:
        ret, image = vs.read()
        if not ret:
            break
        cv2.imshow('Leaf Disease', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('result.png', image)
            break
    vs.release()
    cv2.destroyAllWindows()
    
    dst = "static/images"

    shutil.copy('result.png', dst)
    image = cv2.imread("result.png")
        
    #color conversion
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('static/gray.jpg', gray_image)
    #apply the Canny edge detection
    edges = cv2.Canny(image, 250, 254)
    cv2.imwrite('static/edges.jpg', edges)
    #apply thresholding to segment the image
    retval2,threshold2 = cv2.threshold(gray_image,128,255,cv2.THRESH_BINARY)
    cv2.imwrite('static/threshold.jpg', threshold2)
        # # create the sharpening kernel
    kernel_sharpening = np.array([[-1,-1,-1],
                                    [-1, 9,-1],
                                [-1,-1,-1]])

    # # apply the sharpening kernel to the image
    sharpened =cv2.filter2D(image, -1, kernel_sharpening)

    # save the sharpened image
    cv2.imwrite('static/sharpened.jpg', sharpened)

    
    
    
    
    model=load_model('poul.h5')
    path='static/images/'+fileName


    # Load the class names
    with open('class_names.pkl', 'rb') as f:
        class_names = pickle.load(f)
    rem=""
    rem1=""
    # Function to preprocess the input image
    def preprocess_input_image(path):
        img = load_img(path, target_size=(150,150))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image
        return img_array

    # Function to make predictions on a single image
    def predict_single_image(path):
        input_image = preprocess_input_image(path)
        prediction = model.predict(input_image)
        print(prediction)
        predicted_class_index = np.argmax(prediction)
        predicted_class = class_names[predicted_class_index]
        confidence = prediction[0][predicted_class_index]

        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence: {confidence:.2%}")
            
        return predicted_class, confidence 

    predicted_class, confidence = predict_single_image(path)
    #predicted_class, confidence = predict_single_image(path, model, class_names)
    causes=""
    symptoms=""
    precautions=""
    remedies=""
    print(predicted_class, confidence)
    if predicted_class == 'cocci':
        str_label = "Coccidiosis"
        causes = [
            "Caused by protozoan parasites (Eimeria species) that infect the intestines of poultry.",
            "Spread through contaminated feed, water, or litter."
        ]
        symptoms = [
            "Bloody droppings and diarrhea.",
            "Reduced feed intake and poor weight gain.",
            "Lethargy and ruffled feathers."
        ]
        precautions = [
            "Maintain dry litter and good ventilation.",
            "Avoid overcrowding in poultry houses.",
            "Regularly clean and disinfect drinkers and feeders."
        ]
        remedies = [
            "Add coccidiostats (e.g., Amprolium) in feed or water as prescribed by a vet.",
            "Isolate infected birds immediately.",
            "Provide electrolyte and vitamin supplements to aid recovery."
        ]

    elif predicted_class == 'healthy':
        str_label = "Healthy"
        causes = ["No disease detected."]
        symptoms = ["Birds are active, have bright eyes, and eat normally."]
        precautions = [
            "Maintain a balanced diet and clean water supply.",
            "Ensure proper vaccination and regular health check-ups.",
            "Keep poultry housing clean, dry, and well-ventilated."
        ]
        remedies = ["No specific treatment required. Continue regular care and hygiene."]

    elif predicted_class == 'ncd':
        str_label = "Newcastle Disease (NCD)"
        causes = [
            "Caused by Newcastle disease virus (Paramyxovirus).",
            "Spread through direct contact, contaminated feed, water, and equipment."
        ]
        symptoms = [
            "Coughing, sneezing, and nasal discharge.",
            "Twisting of the neck (torticollis) and paralysis.",
            "Drop in egg production and sudden death."
        ]
        precautions = [
            "Vaccinate chicks and adult birds as per schedule.",
            "Avoid contact with wild birds or new unquarantined flocks.",
            "Disinfect equipment and maintain strict biosecurity."
        ]
        remedies = [
            "There is no specific cure; provide supportive care.",
            "Administer multivitamins and electrolytes.",
            "Consult a veterinarian immediately for outbreak management."
        ]

    elif predicted_class == 'salmo':
        str_label = "Salmonellosis"
        causes = [
            "Caused by Salmonella bacteria (S. pullorum, S. gallinarum).",
            "Spread through contaminated feed, water, or infected eggs."
        ]
        symptoms = [
            "Weakness, drooping wings, and diarrhea.",
            "Poor growth and sudden chick mortality.",
            "Reduced egg production in adults."
        ]
        precautions = [
            "Ensure eggs and feed are from Salmonella-free sources.",
            "Disinfect incubators, waterers, and housing regularly.",
            "Avoid feeding spoiled or contaminated food."
        ]
        remedies = [
            "Use antibiotics like Enrofloxacin or Sulfa drugs as prescribed by a vet.",
            "Provide electrolyte and vitamin supplements.",
            "Cull severely infected birds to prevent spread."
        ]

        try:
            from serial_test import Send
            if predicted_class in ["salmo","ncd","cocci"]:
                Send("A")

            else:
                Send("B")
        except:
            print("Hardware not connected")
                
                

        
            
    
        
        
    accuracy = f"The predicted image is {str_label} with a confidence of {confidence:.2%}"
    
        

    


    return render_template('results.html', 
                            status1=str_label,
                            accuracy1=accuracy,
                            causes11=causes,
                            symptoms11=symptoms,
                            Remedies11=remedies,
                            precautions11=precautions,
                            
                            ImageDisplay1="http://127.0.0.1:5000/static/images/result.png")


@app.route('/logout')
def logout():
    return render_template('userlog.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
