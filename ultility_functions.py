from os.path import exists

from cv2 import \
    imread, imwrite, \
    IMWRITE_JPEG_QUALITY, \
    IMWRITE_JPEG_OPTIMIZE, \
    IMWRITE_JPEG_PROGRESSIVE, \
    IMWRITE_JPEG_CHROMA_QUALITY, \
    IMWRITE_JPEG_LUMA_QUALITY

from numpy import ndarray, full


def add_padding(
        image: "ndarray",
        left_padding: "int",
        top_padding: "int",
        right_padding: "int",
        bottom_padding: "int") \
        -> "ndarray":

    # border_color: "tuple" = (0, 0, 0)) \ (later)

    """
    **PARAMS**:
        **image**: An image needs to add padding - type is "numpy.ndarray".\n
        **left_padding**: Size of the left padding (pixels) - type is "int".\n
        **top_padding**: Size of the top padding (pixels) - type is "int".\n
        **right_padding**: Size of the right padding (pixels) - type is "int".\n
        **bottom_padding**: Size of the bottom padding (pixels) - type is "int".\n

    **REMINDER**:
        - New width is (<input image width> + <left padding> + <right padding>).\n
        - New height is (<input image height> + <top padding> + <bottom padding>).\n
        - Left, top, right, bottom does not necessarily equal.\n
        - Image can either be colored or grayscale.
    """

    # check whether if input image is a colored image:
    try:
        height, width, color_channel = image.shape

    # if not, python will raise a ValueError exception, then this will run:
    except ValueError:
        height, width = image.shape
        color_channel = None

    # calculate new width and height for the new padded image
    new_height = height + top_padding + bottom_padding
    new_width = width + left_padding + right_padding

    # check to see if the image is colored or not
    if color_channel is None:  # as exception raised - no B, G, R, only one number per pixel
        pad_img = full((new_height, new_width), 0, dtype='uint8')
    else:
        # colored image - read numpy.full() for better understanding
        pad_img = full((new_height, new_width, color_channel), (0, 0, 0), dtype='uint8')

    # make a numpy slicing - basically, set whole area which is in the four specific positions of the newly created
    # numpy array of which is filled with 0 (grayscale) or (0, 0, 0) (colored) as same as the input image - search
    # "numpy slicing" on Google for better understanding
    pad_img[0 + top_padding:new_height - bottom_padding, 0 + left_padding: new_width - right_padding] = image

    return pad_img


# some code to try out by yourself:
# img = imread(<your_input_image_here>)
# from cv2 import cvtColor, COLOR_BGR2GRAY
# img = cvtColor(img, COLOR_BGR2GRAY)
#
# padding = add_padding(img, <left>, <top>, <right>, <bottom>)
#
# imwrite(<your_output_image_here>, padding)


def compress_image_jpeg(
        image_url: "str",
        output_name: "str",
        quality: "int" = 90,
        optimize: "bool" = True,
        progressive: "bool" = True,
        chroma_quality: "int" = 75,
        luma_quality: "int" = 75):
    """
       **PARAMS**:
           **image_url**: An URL of the input image (source) - type is "string".\n
           **output_name**: Name of the output image - type is "string".\n
           **quality**: Quality of the output image, compares to the orignal (range from 0 - 100) - type is "int".
           Default value is 90.\n
           **optimize**: OpenCV JPEG feature (IMWRITE_JPEG_OPTIMIZE), change this if you're know what you're doing
           - type is "bool". Default value is True.\n
           **progressive**: OpenCV JPEG feature (IMWRITE_JPEG_PROGRESSIVE), change this if you're know what you're doing
           - type is "bool". Default value is True.\n
           **chroma_quality**: Chroma quality of the output image (color quality), compares to the original
           (range from 0 - 100) - type is "int". Default value is 75.\n
           **luma_quality**: Luminance quality of the output image (light quality), compares to the original
           (range from 0 - 100) - type is "int". Default value is 75.\n

       **REMINDER**:
           - This function does not return any specific value.\n
           - Output doesn't have to had ".jpg", ".jpeg", or ".jpe" extension, the codes will handle that (default is ".jpg").\n
           - The default parameters is considered to give the best balance between quality and output compression size, by the author.\n
           - Input image format is accepted the as currently supporting image formats of OpenCV (current version is 4.5.2).\n
           - Output image will be saved at the same destination as the input image, and will be an JPEG image (".jpg" extension by default).
       """

    # check to see whether if the input image URL contains the following extensions:
    if exists(image_url):
        if image_url.lower().endswith(('.jpg', '.jpeg', '.png', ".bmp", ".dib",
                                       ".jpe", ".jp2", ".webp", ".pbm", ".pgm",
                                       ".ppm", ".pxm", ".pnm", ".sr", ".ras",
                                       ".tiff", ".tif", ".exr", ".hdr", ".pic")):
            image = imread(image_url)

    # if not, raise a ValueError exception
    else:
        raise ValueError("Image does not exists - please check the URL and the file again")

    # check to see if the input image URL use "\" or "/" for image URL path
    if "\\" in image_url:
        split_name = image_url.split("\\")

        # handling the output image extension - default is ".jpg"
        if output_name.lower().endswith(('.jpg', '.jpeg', ".jpe")):
            split_name[-1] = output_name
            new_url = "\\".join(split_name)
        else:
            split_name[-1] = output_name + ".jpg"
            new_url = "\\".join(split_name)

    # same as above
    if "/" in image_url:
        split_name = image_url.split("/")
        if output_name.lower().endswith(('.jpg', '.jpeg', ".jpe")):
            split_name[-1] = output_name
            new_url = "\\".join(split_name)
        else:
            split_name[-1] = output_name + ".jpg"
            new_url = "\\".join(split_name)

    # check the optimize and progressive flag
    if optimize is True:
        is_optimize = 1
    elif optimize is False:
        is_optimize = 0

    if progressive is True:
        is_progressive = 1
    elif progressive is False:
        is_progressive = 0

    try:
        # join all above flags and parameters then execute cv2.imwrite
        imwrite(new_url, image, [int(IMWRITE_JPEG_QUALITY), quality,
                                 int(IMWRITE_JPEG_OPTIMIZE), is_optimize,
                                 int(IMWRITE_JPEG_PROGRESSIVE), is_progressive,
                                 int(IMWRITE_JPEG_CHROMA_QUALITY), chroma_quality,
                                 int(IMWRITE_JPEG_LUMA_QUALITY), luma_quality])
        print(f"Image compressed successfully: {new_url}")

    # just in case something weird happens
    except Exception as e:
        print(f"An error occurred when trying to compress the image.\nLog: {e}")


# try it yourself:
# compress_image_jpeg(<image-url>, <output-image-name>)

# or

# compress_image_jpeg(<image-url>, <output-image-name>, <quality>, <optimize>,
#                     <progressive>, <chroma-quality>, <luminance-quality>)

