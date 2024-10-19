import numpy as np
import cv2


    
def log_transform(image):
    # Convert the image to float32 for more precision
    img_float = np.float32(image)

    # Apply log transformation
    c = 255 / np.log(1 + np.max(img_float))  # Compute scaling constant
    log_image = c * np.log(1 + img_float)
    print(max(log_image))
    # Normalize the result to fit the range [0, 255]
    log_image = np.uint8(cv2.normalize(log_image, None, 0, 255, cv2.NORM_MINMAX))

    return log_image

def envi_log_stretch(image, scale_min=0, scale_max=255):
    """Apply ENVI-style logarithmic stretch to an image."""
    # Ensure the input is in float32 format for precision
    img_float = np.float32(image)

    # Compute the logarithm of the image + 1 to avoid log(0)
    log_image = np.log1p(img_float)
    
    # Normalize the result to [scale_min, scale_max]
    log_image_normalized = cv2.normalize(log_image, None, scale_min, scale_max, cv2.NORM_MINMAX)
    log_image_normalized = np.clip(log_image_normalized, 0.001, 244.9)
    # Convert back to uint8 for proper visualization
    stretched_image = np.uint8(log_image_normalized)

    # Add addittional hist equalization
    return stretched_image


def increase_brightness_hsv(image, value):
    """Increase brightness of an RGB image by modifying the HSV value channel.

    Parameters:
        image (numpy.ndarray): Input RGB image as a NumPy array.
        value (int): Amount to increase brightness; should be between -255 and 255.
    
    Returns:
        numpy.ndarray: Brightened RGB image as a NumPy array.
    """
    # Check if the input image is in the correct format
    if not isinstance(image, np.ndarray):
        raise ValueError("Input must be a NumPy array.")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be an RGB image with three channels.")
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Use a larger datatype to avoid overflow
    hsv = hsv.astype(np.int16)

    # Increase the V (value) channel
    hsv[:, :, 2] += value
    
    # Clip values to ensure they stay within the valid range [0, 255]
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)

    # Convert back to uint8
    hsv = hsv.astype(np.uint8)

    # Convert back to RGB color space
    brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return brightened_image

def mask_red_like_regions(image):
    """Mask red-like regions in an RGB image."""
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Define the range for red-like colors in HSV
    # Red can be represented in two ranges due to the circular nature of the hue
    lower_red1 = np.array([0, 43, 46])    # Lower bound for light red
    upper_red1 = np.array([10, 255, 255])  # Upper bound for light red
    lower_red2 = np.array([156, 43, 46])   # Lower bound for dark red
    upper_red2 = np.array([180, 255, 255]) # Upper bound for dark red

    # Create masks for both ranges
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the masks
    red_mask = cv2.bitwise_or(mask1, mask2)
    # Apply the mask to the original image
    masked_image = cv2.bitwise_and(image, image, mask=red_mask)
    return masked_image, red_mask

def get_image_by_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)

# https://zhuanlan.zhihu.com/p/620247699#:~:text=%E7%94%A8Python%E5%AE%9E%E7%8E%B0ENVI%E4%B8%AD%E7%9A%84%E2%80%9C%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%E2%80%9D%201%201%20%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%20%E9%BB%98%E8%AE%A4%E6%8B%89%E4%BC%B8%E5%88%B00-255%E8%BF%99%E4%B8%AA%E8%8C%83%E5%9B%B4%E5%86%85%EF%BC%8C%E4%B8%8B%E5%90%8C%E3%80%82%20def%20linear%28arr%29%3A%20arr_min%2C,3%20%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%20%E4%BC%98%E5%8C%96%E7%9A%84%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%E7%B1%BB%E4%BC%BC%E4%BA%8E%E7%BA%BF%E6%80%A7%E6%8B%89%E4%BC%B8%EF%BC%8C%E4%BD%86%E6%8F%90%E4%BE%9B%E4%BA%86%E6%9B%B4%E5%A4%9A%E8%AE%BE%E7%BD%AE%E6%9D%A5%E6%8E%A7%E5%88%B6%E5%9B%BE%E5%83%8F%E4%B8%AD%E7%9A%84%E4%B8%AD%E9%97%B4%E8%B0%83%E3%80%81%E9%98%B4%E5%BD%B1%E5%92%8C%E9%AB%98%E5%85%89%E3%80%82%20%E5%AE%83%E6%A0%B9%E6%8D%AE%E5%9B%9B%E4%B8%AA%E5%80%BC%E8%AE%A1%E7%AE%97%E6%8B%89%E4%BC%B8%E6%9C%80%E5%B0%8F%E5%80%BC%E5%92%8C%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%9A%20%E6%9C%80%E5%B0%8F%E7%99%BE%E5%88%86%E6%AF%94%20%EF%BC%9A%E9%BB%98%E8%AE%A4%E5%80%BC%E4%B8%BA%200.025%E3%80%82%20
def optimized_linear(arr):
    a, b = np.percentile(arr, (2.5, 99))
    c = a - 0.1 * (b - a)
    d = b + 0.5 * (b - a)
    arr = (arr - c) / (d - c) * 255
    arr = np.clip(arr, 0, 255)
    return np.uint8(arr)

def percent_linear(arr, percent=2):
    arr_min, arr_max = np.percentile(arr, (percent, 100-percent))
    arr = (arr - arr_min) / (arr_max - arr_min) * 255
    arr = np.clip(arr, 0, 255)
    return np.uint8(arr)

# assume 3D
def percent_linear_per_band(arr,percent=2):
    h,w,d = arr.shape
    result = np.empty((h,w,d),np.uint8)
    for i in range(d):
        band = arr[:,:,i]
        arr_min, arr_max = np.percentile(band, (percent, 100-percent))
        band = (band - arr_min) / (arr_max - arr_min) * 255
        band = np.clip(band, 0, 255)
        result[:,:,i] = np.uint8(band)
    return result

def percent_linear_float(arr,percent=2):
    arr_min, arr_max = np.percentile(arr, (percent, 100-percent))
    arr = (arr - arr_min) / (arr_max - arr_min)
    return arr
    
# https://nirpyresearch.com/two-scatter-correction-techniques-nir-spectroscopy-python/
# Assume h x w x band shape
def snv(input_data):
    # Define a new array and populate it with the corrected data  
    output_data = np.zeros_like(input_data)
    output_data= (input_data - np.mean(input_data)) / np.std(input_data)
    return output_data

def clip_image(arr):
    arr = np.clip(arr, 0.01, 254.99)
    return np.uint8(arr)

def map_darray_by_dict(arr, dict):
    color_lookup = np.array([dict[i] for i in range(len(dict))], dtype=np.uint8)
    return color_lookup[arr]