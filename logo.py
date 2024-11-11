import streamlit as st
from PIL import Image
import imagehash
import os
import numpy as np
import matplotlib.pyplot as plt

# Path to your database of images
DATABASE_PATH = "Logos"
SIMILARITY_THRESHOLD = 5  # Define a threshold for similarity

# Function to load database images and generate hashes
def load_database():
    db_hashes = {}
    for filename in os.listdir(DATABASE_PATH):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(DATABASE_PATH, filename)
            img = Image.open(img_path)
            db_hashes[filename] = imagehash.average_hash(img)
    return db_hashes

# Load database hashes
database_hashes = load_database()

# Streamlit app title and description
st.title("Logo Verification System with Analytics")
st.write("Upload an image to verify if it matches any image in the legitimate database and view model analytics.")

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize counters for legitimacy comparison
legitimate_count = 0
non_legitimate_count = 0

if uploaded_file is not None:
    # Display uploaded image
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Calculate hash for the uploaded image
    uploaded_image_hash = imagehash.average_hash(uploaded_image)

    # Find the closest match in the database
    closest_match = None
    smallest_difference = float('inf')
    for filename, db_hash in database_hashes.items():
        difference = abs(uploaded_image_hash - db_hash)
        if difference < smallest_difference:
            smallest_difference = difference
            closest_match = filename

    # Display result with color-coded legitimacy indicator
    if closest_match:
        st.write(f"Closest match in database: **{closest_match}**")
        st.write(f"Hash difference: **{smallest_difference}**")

        # Set legitimacy based on the threshold
        is_legitimate = smallest_difference <= SIMILARITY_THRESHOLD

        # Color-coded message and counter update
        if is_legitimate:
            st.success("This logo is **legitimate**.", icon="✅")
            legitimate_count += 1
        else:
            st.error("This logo is **not legitimate**.", icon="🚫")
            non_legitimate_count += 1

        # Display the closest matching image
        matched_image = Image.open(os.path.join(DATABASE_PATH, closest_match))
        st.image(matched_image, caption=f"Closest Match: {closest_match}", use_column_width=True)
    else:
        st.write("No match found.")

    # Record similarity score for analytics
    similarity_scores = [abs(uploaded_image_hash - db_hash) for db_hash in database_hashes.values()]

# Sidebar for analytics
st.sidebar.header("Analytics Dashboard")

# Model Performance Analytics (synthetic data for demonstration)
if st.sidebar.checkbox("Show Model Performance Analytics"):
    st.subheader("Model Performance")
    epochs = np.arange(1, 11)
    accuracy = np.random.uniform(0.7, 1.0, len(epochs))
    loss = np.random.uniform(0.1, 0.5, len(epochs))

    fig, ax = plt.subplots()
    ax.plot(epochs, accuracy, label="Accuracy")
    ax.plot(epochs, loss, label="Loss")
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)

# Similarity Distribution Analytics
if st.sidebar.checkbox("Show Similarity Distribution Analytics"):
    st.subheader("Similarity Score Distribution")
    fig, ax = plt.subplots()
    ax.hist(similarity_scores, bins=10, color="skyblue", edgecolor="black")
    ax.set_xlabel("Hash Difference")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Legitimacy Comparison
if st.sidebar.checkbox("Show Legitimacy Comparison"):
    st.subheader("Legitimacy Comparison")
    labels = ["Legitimate", "Not Legitimate"]
    sizes = [legitimate_count, non_legitimate_count]
    colors = ["#4CAF50", "#F44336"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.axis("equal")
    st.pyplot(fig)
