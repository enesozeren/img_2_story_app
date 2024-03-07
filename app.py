import streamlit as st
from utils.util_funcs import image_2_text, generate_story, text_2_speech

st.set_page_config(page_title='Image to Story')
st.title("Image to Story")
st.caption("""Disclaimer: Use at Your Own Risk! 
           This Streamlit app comes with no guarantees or warranties. \
           I am not responsible for any damages, data breaches, \
           or issues that may arise from its use. No support is provided, \
           and the app may not be regularly updated. By using it, you agree \
           to release me from any liabilities. If you don't agree, please \
           refrain from using the app."""
           )

# Get the image from user
st.header("Upload your image to get your story!")
image_file = st.file_uploader(label="Upload your image here", type="jpg")

if image_file is not None:
    # Display the input Image
    st.image(image_file, caption="Your Image", use_column_width=True)

    # Convert image to bytes
    bytes_data = image_file.getvalue()
    with open(image_file.name, 'wb') as file:
        file.write(bytes_data)
    
    # Get the caption & story & sound
    caption = image_2_text(image_file.name)

    story = generate_story(caption)

    text_2_speech(story)
    st.subheader("Listen to your story!")
    st.audio("story_audio.mp3")

    with st.expander(label="See the text"):
        st.write(story)