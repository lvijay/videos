import cv2
import numpy as np

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to create a binary image
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh

def find_contours(binary_image):
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def draw_contours(image, contours):
    # Draw contours on the original image
    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    return result

def main(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Find contours
    contours = find_contours(preprocessed_image)

    # Draw contours on the original image
    original_image = cv2.imread(image_path)
    image_with_contours = draw_contours(original_image, contours)

    # Display the results
    cv2.imshow('Original Image with Contours', image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    imagename = sys.argv[1]
    main(imagename)
