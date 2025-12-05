"""Image processing functions for PDF comparison."""
import gc
import cv2
import numpy as np
from PIL import Image
from typing import Optional

from config import ProcessingConfig


def clean_noise_mask(
    mask: np.ndarray,
    min_area: int = ProcessingConfig.min_area_noise,
) -> np.ndarray:
    """Remove noise from binary mask by filtering small contours.

    Args:
        mask: Binary mask image.
        min_area: Minimum contour area to keep.

    Returns:
        Cleaned binary mask.
    """
    if mask is None or mask.size == 0:
        return mask

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_clean = np.zeros_like(mask)

    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            cv2.drawContours(mask_clean, [contour], -1, 255, -1)

    del contours  # Free memory explicitly
    return mask_clean


def align_image(
    base_img: np.ndarray,
    img_to_align: np.ndarray,
    config: ProcessingConfig = ProcessingConfig(),
) -> np.ndarray:
    """Align an image to a base image using feature matching.

    Args:
        base_img: Reference image (RGB or grayscale).
        img_to_align: Image to align (RGB or grayscale).
        config: Processing configuration.

    Returns:
        Aligned image with same dimensions as base_img.
    """
    if base_img is None or img_to_align is None:
        raise ValueError("Both images must be provided")

    # Convert to grayscale if needed
    gray_base = (
        cv2.cvtColor(base_img, cv2.COLOR_RGB2GRAY)
        if len(base_img.shape) == 3
        else base_img
    )
    gray_align = (
        cv2.cvtColor(img_to_align, cv2.COLOR_RGB2GRAY)
        if len(img_to_align.shape) == 3
        else img_to_align
    )

    # Feature detection
    orb = cv2.ORB_create(config.orb_features)
    keypoints1, descriptors1 = orb.detectAndCompute(gray_align, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray_base, None)

    if descriptors1 is None or descriptors2 is None:
        result = cv2.resize(
            img_to_align, (base_img.shape[1], base_img.shape[0])
        )
        del gray_base, gray_align, orb, keypoints1, keypoints2, descriptors1, descriptors2
        return result

    # Feature matching
    matcher = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    bf = cv2.BFMatcher(matcher, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = matches[:int(len(matches) * config.match_percentage)]

    if len(good_matches) < config.min_matches:
        result = cv2.resize(
            img_to_align, (base_img.shape[1], base_img.shape[0])
        )
        del gray_base, gray_align, orb, keypoints1, keypoints2, descriptors1, descriptors2, matches, good_matches, bf
        return result

    # Extract matching points
    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

    for i, match in enumerate(good_matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    homography, _ = cv2.findHomography(
        points1, points2, cv2.RANSAC
    )

    if homography is None:
        result = cv2.resize(
            img_to_align, (base_img.shape[1], base_img.shape[0])
        )
        del gray_base, gray_align, orb, keypoints1, keypoints2, descriptors1, descriptors2, matches, good_matches, bf, points1, points2
        return result

    # Warp image
    height, width = base_img.shape[:2]
    img_aligned = cv2.warpPerspective(
        img_to_align, homography, (width, height)
    )

    # Clean up intermediate variables
    del gray_base, gray_align, orb, keypoints1, keypoints2, descriptors1, descriptors2, matches, good_matches, bf, points1, points2, homography

    return img_aligned


def process_page(
    base_page: Optional[Image.Image],
    modified_page: Optional[Image.Image],
    config: ProcessingConfig = ProcessingConfig(),
) -> Optional[Image.Image]:
    """Process a single page comparison with aggressive memory cleanup.

    Args:
        base_page: Original page image (PIL Image).
        modified_page: Modified page image (PIL Image).
        config: Processing configuration.

    Returns:
        Comparison result image or None if both pages are None.
    """
    # Handle missing pages
    if base_page is None and modified_page is None:
        return None

    # Convert PIL to numpy arrays
    if base_page is None and modified_page is not None:
        width, height = modified_page.size
        base_array = np.full((height, width, 3), 255, dtype=np.uint8)
        modified_array = np.array(modified_page)
    elif modified_page is None and base_page is not None:
        width, height = base_page.size
        base_array = np.array(base_page)
        modified_array = np.full((height, width, 3), 255, dtype=np.uint8)
    else:
        base_array = np.array(base_page)
        modified_array = np.array(modified_page)

    # Align images
    try:
        if base_page is not None and modified_page is not None:
            aligned_array = align_image(base_array, modified_array, config)
        else:
            aligned_array = cv2.resize(
                modified_array,
                (base_array.shape[1], base_array.shape[0])
            )
    except Exception:
        aligned_array = cv2.resize(
            modified_array,
            (base_array.shape[1], base_array.shape[0])
        )

    # Free original images after alignment
    del base_page, modified_page

    # Convert to grayscale
    gray_base = (
        cv2.cvtColor(base_array, cv2.COLOR_RGB2GRAY)
        if len(base_array.shape) == 3
        else base_array
    )
    gray_aligned = (
        cv2.cvtColor(aligned_array, cv2.COLOR_RGB2GRAY)
        if len(aligned_array.shape) == 3
        else aligned_array
    )

    # Free RGB arrays
    del base_array, aligned_array

    # Invert and threshold
    inv_base = cv2.bitwise_not(gray_base)
    inv_aligned = cv2.bitwise_not(gray_aligned)

    _, bin_base = cv2.threshold(
        inv_base, config.threshold_value, 255, cv2.THRESH_TOZERO
    )
    _, bin_aligned = cv2.threshold(
        inv_aligned, config.threshold_value, 255, cv2.THRESH_TOZERO
    )

    # Free inverted images
    del inv_base, inv_aligned

    # Apply tolerance (dilate) BEFORE deleting bin_base and bin_aligned
    kernel = np.ones(config.tolerance_kernel_size, np.uint8)
    base_dilated = cv2.dilate(
        bin_base, kernel, iterations=config.tolerance_iterations
    )
    aligned_dilated = cv2.dilate(
        bin_aligned, kernel, iterations=config.tolerance_iterations
    )

    # Find differences BEFORE deleting bin_base and bin_aligned
    raw_green = cv2.subtract(bin_aligned, base_dilated)
    raw_magenta = cv2.subtract(bin_base, aligned_dilated)

    # Free binary images AFTER using them
    del bin_base, bin_aligned, kernel, base_dilated, aligned_dilated

    # Clean noise
    _, mask_green_bin = cv2.threshold(raw_green, 1, 255, cv2.THRESH_BINARY)
    _, mask_magenta_bin = cv2.threshold(
        raw_magenta, 1, 255, cv2.THRESH_BINARY
    )

    # Free raw differences
    del raw_green, raw_magenta

    clean_green = clean_noise_mask(
        mask_green_bin, min_area=config.min_area_noise
    )
    clean_magenta = clean_noise_mask(
        mask_magenta_bin, min_area=config.min_area_noise
    )

    # Free unclean masks
    del mask_green_bin, mask_magenta_bin

    # Create ghost effect background - KEEP gray_base until here
    ghost_bg = cv2.addWeighted(
        gray_base,
        config.ghost_base_weight,
        np.full_like(gray_base, 255),
        config.ghost_bg_weight,
        0,
    )
    
    # Now we can free gray_base
    del gray_base, gray_aligned
    
    final_img = cv2.cvtColor(ghost_bg, cv2.COLOR_GRAY2RGB)
    del ghost_bg

    # Apply color highlights
    final_img[clean_green > 0] = config.green_color
    final_img[clean_magenta > 0] = config.magenta_color

    # Free masks
    del clean_green, clean_magenta

    result = Image.fromarray(final_img)
    del final_img

    return result