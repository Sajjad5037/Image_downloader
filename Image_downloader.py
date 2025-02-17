import requests 
from bs4 import BeautifulSoup
import os
import sys

def download_image(search_query,output_dir):
    # create the output directory if it does not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    #populate your required search url
    search_url= f"https://example.com/search?query= {search_query.replace(' ','+')}"
    
    #send a request to the page 
    response= requests.get(search_url)
    if response.status_code!=200:
        print(f"failed to retrieved images at {search_url} because of the error number: {response.status_code}")
        return
    
    #parse the HTML content
    soup=BeautifulSoup(response.text,'html.parser')
    
    #find all image elements
    image_elements= soup.find_all('img') # adjust the tag and the attributes based on the real website
    
    #download each image 
    for i,img in enumerate(image_elements): # the counter i is not used to break the loop but to save the downloaded file with the correct image number
        img_url=img.get('src') #get image url 
        if not img_url:
            continue # it means that the loop is not ending because of an counter value but on the logic that if img_url receive a non value the loop breaks
        
        #handle relative URL if necessary
        if not img_url.startswith('http'):
            img_url= f'https://example.com{img_url}'
            
        try:
            img_response=requests.get(img_url)
            img_response.raise_for_status()
            
            #save the image to the output directory
            img_path=os.path.join(output_dir,f"image_{i+1}.jpg")
            with open(img_path,'w') as fileW:
                fileW.write(img_response.content)
                
                print(f"downloaded image {i+1}: {img_url}")
        except requests.RequestException as e:
            print(f"failed to download image {i+1}: {e}")

#example usage 
if len(sys.argv)!=3:
    print("Usage: python download_images.py <search_qurry><output_directory>")
else:
    query=sys.argv[1]
    directory=sys.argv[2]
    download_image(query,directory)           
        