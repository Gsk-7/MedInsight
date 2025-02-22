import pandas as pd
import os
import requests

# Load the dataset
file_path = 'C:/Users/gowri/OneDrive/Desktop/Movie/Movie.csv'
dataset = pd.read_csv(file_path)

# Display basic information
print(dataset.info())  # Shows data types, non-null counts, etc.
print(dataset.head())  # Displays the first few rows

# Check for missing values in the cleaned dataset
missing_values = dataset.isnull().sum()

# Print the missing values count
print("Missing values in each column:")
print(missing_values)

# Drop rows with missing year values
dataset = dataset.dropna(subset=['year'])

# Check for missing values again
missing_values = dataset.isnull().sum()
print("Missing values in each column:")
print(missing_values)

# Check for duplicate rows
duplicates = dataset.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

# Remove duplicates
dataset = dataset.drop_duplicates()

# Check unique values in key columns
print(dataset['title'].nunique())  # Number of unique movie titles
print(dataset['poster_path'].head())    # Preview the image paths




def download_images(dataset, image_column, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through the dataset to download images
    for _, row in dataset.iterrows():
        image_path = row[image_column]  # Get the poster_path
        if pd.notna(image_path):  # Ensure the image path is not NaN
            # Construct the full image URL
            image_url = f"https://image.tmdb.org/t/p/w500{image_path}"
            
            # Get the image name from the URL (filename)
            image_name = image_url.split("/")[-1]
            image_save_path = os.path.join(output_folder, image_name)
            
            # Download and save the image
            try:
                response = requests.get(image_url)
                if response.status_code == 200:  # Check if the request was successful
                    with open(image_save_path, 'wb') as file:
                        file.write(response.content)
                else:
                    print(f"Failed to download image: {image_url}")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")

# Example usage
download_images(dataset, 'poster_path', 'movie_images')

