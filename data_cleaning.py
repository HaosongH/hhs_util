from file_util import *
from image_transform_util import *

# given RGB or gray image, only include pixel value above certain thresh and output the result gray image with 255 and 0
# The binary image will be stored in the output directory, where the file name is the same as input filename
def threshold_convert(image_path, thresh_value, output_dir, output_ext = "tiff"):
    # Read the image (as grayscale)
    img = cv_read(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Invalid image path or the image could not be loaded.")
    # Apply threshold: pixels above 'thresh_value' -> 255, others -> 0
    _, binary_img = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
    image_name = get_base_name_withoutext(image_path)
    # Save the binary image to the specified path
    cv_write(os.path.join(output_dir, image_name+"." + output_ext), binary_img)
    return binary_img

def threshold_convert_dir(input_dir, output_dir, thresh_value, input_ext, output_ext="tiff"):
    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)
    fileList = generate_file_list(input_dir, input_ext)
    for file in fileList:
        threshold_convert(file, thresh_value, output_dir, output_ext)


# Rename one file or files in the directory to another place
def rename_file(source_path, new_name, destination_dir):
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)
    # Extract the original file extension
    _, ext = os.path.splitext(source_path)
    # Construct the new file path with the same extension
    new_file_path = os.path.join(destination_dir, new_name + ext)
    # Copy the file to the new location with the new name
    shutil.copy2(source_path, new_file_path)
    print("Rename File ", source_path, " to ", new_file_path)
    return new_file_path

# rename_func should receive the full path of the inputfile for better variability, and the return value should not include ext
def rename_files_in_folders(input_dir, input_ext, output_dir, rename_func, *argv):
    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)
    fileList = generate_file_list(input_dir, input_ext)
    for file in fileList:
        rename_file(file, rename_func(file, *argv), output_dir)
        
# Change single image to npy based on function f
def imageFileToNpyFile2D(imagePath, mode, npyPath, f, *argv):
    img = cv_read(imagePath, mode)
    array = f(img,*argv)
    np.save(npyPath, array)
    
# Change single image to npy based on function f
def imageFileToNpy2D(imagePath, mode, f, *argv):
    img = cv_read(imagePath, mode)
    array = f(img,*argv)
    return array

def npyFileToImageFile2D(npyPath, imagePath, f, *argv):
    array = np.load(npyPath,allow_pickle=True)
    image = f(array, *argv)
    cv_write(imagePath,image)
    
def imageByMaskFolder(image_dir, mask_dir, output_dir, mask_ext, image_ext, output_ext):
    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)
    files = generate_file_list(mask_dir, mask_ext)
    for file in files:
        file_basename = get_base_name_withoutext(file)
        imagePath = os.path.join(image_dir, file_basename + "." + image_ext)
        outputPath = os.path.join(output_dir, file_basename + "." + output_ext)
        maskArray = cv_read(file, cv2.IMREAD_GRAYSCALE, 0)
        imageArray = cv_read(imagePath, cv2.IMREAD_COLOR, 0)
        resultArray = get_image_by_mask(imageArray, maskArray)
        cv_write(outputPath, resultArray)