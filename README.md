# A2-Projective-Transformation-and-Stereo-Matching

## Part 1: Putting Happy Minions Faces on Empty Billboards of Times Square

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
