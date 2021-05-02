# A2-Projective-Transformation-and-Stereo-Matching

## Part 1: Putting Happy Minions Faces on Empty Billboards of Times Square

### Work Split

- Emma: OpenCV annotation  
- Cody: Rest of program

### How to Use

python homography.py [city_image] [image_to_put_on_billboard] [output_name]

1. A window will pop-up with the image with blank billboards
2. Double click the corners of the empty billboard
3. Type 'Enter' when you have clicked exactly 4 corners. (If you click more or less points, the program will terminate)
4. The billboard image with your new image will be displayed to the screen as well as saved to the /output folder.

### Examples

python homography.py input_images/part1/input/target/empty_bilboard4.jpg input_images/part1/input/source/gcat.jpg grumpycat

![example1](/examples/grumpycat.png)

python homography.py input_images/part1/input/target/empty_bilboard1.jpg input_images/part1/input/source/happy_minions1.png minion1 

![example2](/examples/minion1.png)

python homography.py input_images/part1/input/target/empty_bilboard2.jpg input_images/part1/input/source/happy_minions2.png minion2 

![example3](/examples/minion2.png)

### Implementation Details

OpenCV was used to annotate the image to have the 4 corners of an empty billboard marked.

The four points were then ordered so that they would match the following pattern, where the number shown is the index of the point.

0 > 1  
4 < 2

This was neccessary so that the top left corner was always mapped to the top left corner of the billboard image. The points for the corners of the image being put on the billboard were just built using the following method using the width and height of the image:

((0, 0), (bb_width, 0), (bb_width, bb_height), (0, bb_height))

### Putting Pixels on the Board

Instead of grabbing each pixel from the image that is being pasted on the billboard and translating it to the target image, we take the inverse of the H matrix and loop through the target image to find what pixels map to the billboard image. If we do not do this, then there will be white pixels if the image we are putting on the billboard is smaller than the actual area it is being applied to.

## Part 2: Stereo Matching

### Work Split
- Emma: Evaluation functions
- Neelan: Rest of program

### How to Use

python3 stereo_matching.py [left_image] [right_image] [ground_truth_image] [output_file]

### Implementaion Details
The first step was to create two helper functions. One that calculate the sum of squared distances between two arrays, and another that builds an array of pixel values around a given pixel with subject to a particular window size. 

The main function then loops through each pixel in a row, builds a comparison array around that pixel and then checks similar arrays for every other pixel in that row. The distance between the target pixel and the best match is then recorded as the disparity value. Once this is done for each pixel in the image, the final disparity map is returned. 

The disparity map is then standardized to be between 0 and 255 and saved to the output file as a grayscale image. 

Finally, the two evaluation metrics are computed between the standardized disparity map and the ground truth image. 

### Struggles
The first iteration of the code was incredible slow. Each individual function was relatively quick - on the order of a milisecond- but there were simply so many comparisons that had to be completed. Since each pixel in every row needs to be compared to every other pixel in the row the number of comparisons would be width^2. Then, this needs to be repeated for every row so the total number of comparisons that need to be performed is width^2 * height. The test images provided were 960 * 540 so there would be 497,664,000 comparisons. Even if you could complete one comparison in a millisecond, it would take nearly a year to run through the entire image. This is obviously waaaaaaay too long. 

To try to address this issue, we downsampled the two images. We kept the aspect ratio the same but set the height to 100. At this size, with a window size of 5 we are able to process an image in just a few minutes. As the window size increases though, so does the computation time. 

We also had to downsize the ground truth image so that we could do a fair comparison.

While this method deos help speed up the process, the results admittedly are not very good. There are a few times where you can start to make out outlines of objects in a few of the test images, but they do not compare well to the ground truth. If there were more time, perhaps we could have tried to implement an MRF and use loopy belief propogation to imporve the disparity calculation. 