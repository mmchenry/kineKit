# Videotools

<!-- ## Overview -->




## Code catalog

- **video_tools.py**: Series of functions for manipulating and interacting with video. Requires installing ffmpeg and opencv.

    - **vid_from_seq**: Creates a movie from an image sequence.
    - **vid_convert**: Converts a video file, perhaps with cropping and downsampling.
    - **get_frame**: Reads a single frame from a video file.
    - **find_roi**: Reads frame of video and prompts to interactively select a roi.
    - **find_coords**: Reads frame of video and prompts to interactively select coordinates.
    - **click_coords**: Callback function, called by OpenCV when the user interacts
    with the window using the mouse.
    - **get_background**: Computes background of video and outputs as png.
    - **bg_subtract**: Perform background subtraction and image smoothing to video