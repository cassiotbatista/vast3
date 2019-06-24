# How to vectorize a png?

1. Open `in-colour.png` with gimp
2. Follow the steps to binarize the image:
    - apply sobel edge detector
    - invert colours
    - erode 3x to thicken lines
    - add alpha channel to make the bg transparent
    - apply threshold with pixel value of 1 to discard white colours
    - export as `in-edges.png`
3. Load both `in-*.png` on ImageMagick 
    - sum them up with the `-coalesce` option 
    - save the output image as `map.png` 
4. Open `map.png` with inkscape
5. Follow the steps to vectorize the image:
    - apply bitmap tracing with multi scana in 8 colours scans with no smoothness
    - save as `map.svg`
