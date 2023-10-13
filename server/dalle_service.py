# server/dalle_service.py
import openai
import base64

def generate_image(koan):
    try:
        enriched_prompt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system", 
                "content": "You will interpret this koan, and generate a prompt for dalle3 for an image that will prompt reflection in the student targeted by this koan. The image will have no text, it will just be heavily stylized, abstract dreamscape. Your response will contain no content other than the prompt to be passed directly to dalle",
            }, {
                "role": "user", 
                "content": koan
            }]
        )
        enriched_prompt = enriched_prompt_response['choices'][0]['message']['content']
        print(enriched_prompt)

        response = openai.Image.create(
            prompt=enriched_prompt,
            n=1,  # Generate 1 image
            size="512x512"
            # ... other parameters as needed
        )

        # Assuming the API returns a list of image data, and that image_data is a bytes object
        image_data = response['data'][0]

        # Convert the image data to a base64-encoded string
        # image_base64 = base64.b64encode(image_data).decode('utf-8')
        image_url = response['data'][0]['url']  # Adjust this line based on the actual structure of the response object
        # Create a Data URL
        # image_data_url = f"data:image/png;base64,{image_base64}"

        return image_url

    except Exception as e:
        print(f"Failed to generate image: {e}")
        return None
