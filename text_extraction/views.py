import os
import shutil
import easyocr
from django.shortcuts import redirect, render
from django.contrib import messages
import cv2

def home(request):
    empty_directories("media/uploaded_images/", "media/processed_images/")
    context = {
        'title' : "Home Page",
    }
    return render(request, 'home.html', context=context)


def text_extraction(request):
    image_path = ''
    if request.method == 'POST':
        image_path = 'media/uploaded_images/'
        os.makedirs(image_path, exist_ok=True)
        
        processed_images_path = 'media/processed_images/'
        os.makedirs(processed_images_path, exist_ok=True)
        
        image_file = request.FILES.get('image')
        selected_languages = request.POST.getlist('languages')
        
        if 'ar' or 'hi' in selected_languages:
            # Append 'en' to the list
            selected_languages.append('en')
        print("Selected Languages:", selected_languages)

        if image_file:
            image_path = os.path.join(image_path, image_file.name)

            with open(image_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
                    
            print("Image Path", image_path)
            if 'ur' in selected_languages and 'hi' in selected_languages:
                # Process Urdu and Hindi separately
                reader_urdu = easyocr.Reader(['ur'])
                urdu_text = reader_urdu.readtext(image_path)

                reader_hindi = easyocr.Reader(['hi'])
                hindi_text = reader_hindi.readtext(image_path)

                # Combine results
                result = urdu_text + hindi_text 
            else:
                # Process other language combinations directly
                reader = easyocr.Reader(selected_languages, gpu=False)
                result = reader.readtext(image_path)
            print("Result: ", result)
            
            # Getting Text Coordinates from the image
            top_left = tuple(result[0][0][0])
            bottom_right = tuple(result[0][0][2])
            text = result[0][1]
            font = cv2.FONT_HERSHEY_COMPLEX

            # Reading image using OpenCV
            img = cv2.imread(image_path)
            
            for detection in result:
                top_left = tuple([int(val) for val in detection[0][0]])
                bottom_right = tuple([int(val) for val in detection[0][2]])
                text = detection[1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
                
            processed_image_path = os.path.join(processed_images_path, image_file.name)
            cv2.imwrite(processed_image_path, img)
            
            print(processed_image_path)
            context = {
                'image_path' : image_path,
                'result' : result,
                'processed_image_path': processed_image_path,  
            }
            return render(request, 'text-extraction.html', context=context)
        
        else:
            pass
    context = {
        'title' : "Text Extraction",
        'image_path' : image_path,
    }
    return render(request, 'text-extraction.html', context=context)


# Method to Empty Upload Image and Process Image Directory
def empty_directories(uploaded_images_path, processed_images_path):
    shutil.rmtree(uploaded_images_path, ignore_errors=True)
    shutil.rmtree(processed_images_path, ignore_errors=True)
    
    os.makedirs(uploaded_images_path, exist_ok=True)
    os.makedirs(processed_images_path, exist_ok=True)
    
    return True