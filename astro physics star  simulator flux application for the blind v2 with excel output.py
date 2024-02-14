import numpy as np
from scipy.ndimage import gaussian_filter, label, binary_opening
from scipy import fftpack
import pyttsx3  # Text-to-speech library
import keyboard  # For keyboard shortcuts
import pandas as pd  # Import pandas
# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to simulate an image with accessibility features
def imsim():
    try:
        speak("Generating simulated image with size 1024 by 1024 pixels.")
        sx, sy = 1024, 1024
        im = 10. * np.random.randn(sx, sy)

        m_min, m_max = 9., 20.27  # Min and max magnitudes for stars
        N = int((0.25 / 100.) * (2 * (np.exp(0.5 * m_max) - np.exp(0.5 * m_min))))  # Number of stars

        cn = np.random.rand(N)
        m = 2 * np.log(np.exp(0.5 * m_min) + cn * (np.exp(0.5 * m_max) - np.exp(0.5 * m_min)))

        x = 10 + (np.random.rand(N) * (sx - 20)).astype('int16')
        y = 10 + (np.random.rand(N) * (sy - 20)).astype('int16')
        cts = 10 * np.sqrt(1.1e3) * 10 ** (-0.4 * (m - m_max)) * np.sqrt(4 * np.pi) * 2

        im_s = np.zeros((sx, sy), dtype='float32')
        for i in range(N):
            im_s[x[i], y[i]] += cts[i]

        speak("Image simulation complete.")
        return gaussian_filter(im_s, 2.) + np.sqrt(im_s + 1.e3) * np.random.randn(sx, sy)
    except Exception as e:
        speak(f"An error occurred in image simulation: {e}")
        raise

# Function to find stars with accessibility features
def find_stars(image):
    try:
        speak("Finding stars in the image.")
        sigma_value = 1  
        smoothed_image = gaussian_filter(image, sigma=sigma_value)

        local_thresh = 50
        stars = smoothed_image > local_thresh

        struct_elem = np.ones((2, 2))
        stars = binary_opening(stars, structure=struct_elem)

        labeled, num_features = label(stars)
        final_i, final_j = [], []

        for feature in range(1, num_features + 1):
            y, x = np.where(labeled == feature)
            centroid_x = int(np.mean(x))
            centroid_y = int(np.mean(y))

            x_min = max(centroid_x - 1, 0)
            x_max = min(centroid_x + 2, image.shape[1])
            y_min = max(centroid_y - 1, 0)
            y_max = min(centroid_y + 2, image.shape[0])

            local_max = np.max(smoothed_image[y_min:y_max, x_min:x_max])
            if smoothed_image[centroid_y, centroid_x] >= local_max * 0.7:
                final_i.append(centroid_y)
                final_j.append(centroid_x)

        speak(f"Found {len(final_i)} stars.")
        return np.array(final_i), np.array(final_j)
    except Exception as e:
        speak(f"An error occurred in finding stars: {e}")
        raise


def measure_stars(image, i, j, filter_sigma=2.5):
    try:
        speak("Measuring stars in the image.")
        smoothed_image = gaussian_filter(image, sigma=filter_sigma)

        # Measuring the flux of each star
        fluxes = []
        for x, y in zip(i, j):
            # Define a small window around the star's coordinates to measure the flux
            window_size = 3  # Example: 3x3 window
            x_min = max(x - window_size // 2, 0)
            x_max = min(x + window_size // 2 + 1, image.shape[1])
            y_min = max(y - window_size // 2, 0)
            y_max = min(y + window_size // 2 + 1, image.shape[0])

            # Sum the pixel values in the window to get the flux
            star_flux = np.sum(smoothed_image[y_min:y_max, x_min:x_max])
            fluxes.append(star_flux)

        speak(f"Measured the fluxes of {len(fluxes)} stars.")
        return np.array(fluxes)
    except Exception as e:
        speak(f"An error occurred in measuring stars: {e}")
        raise

# Main function with audio feedback
if __name__ == "__main__":
    try:
        speak("Starting the image processing script.")
        image = imsim()
        i, j = find_stars(image)
        fluxes = measure_stars(image, i, j)

        # Create a DataFrame to hold the results with units
        df = pd.DataFrame({
            'Star_Y_Coordinate (pixels)': i, 
            'Star_X_Coordinate (pixels)': j, 
            'Flux (a.u.)': fluxes  # Assuming arbitrary units for flux
        })

        # Save the DataFrame to an Excel file
        excel_filename = "star_measurements.xlsx"
        df.to_excel(excel_filename, index=False)
        speak(f"I measured {fluxes} and saved the data with units in {excel_filename}")

        # Output the measured fluxes using text-to-speech
        speak(f"I measured {fluxes}")
    except Exception as e:
        speak(f"An error occurred in the main script: {e}")
    finally:
        # Wait for a keyboard shortcut to exit, e.g., pressing 'q'
        speak("Press Q to quit.")
        keyboard.wait('q')
        speak("Exiting script.")

