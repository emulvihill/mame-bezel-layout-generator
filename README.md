#What is this?

It generates MAME .lay Layout files for bezel artworks.

# Requirements
Tested with:
Python 3.6.1 :: Anaconda custom (64-bit)
numpy (1.13.1)
opencv-python (3.3.1+contrib)

#How to use
* First edit the "dirName" path variable to your bezel artwork folder. 

* Then run the program. It will pop up an image of each bezel. It will draw a guess as to the rectangle that might work for your game.
If the guess is not good enough, then redraw by clicking in the upper-left and dragging to the botom right, then releasing the mouse button.

* When you are satisfied, then just hit a key (space, or whatever). It will copy the image and generate a .Lay file, then go to the next image in the bezel folder

* All results will be output inside the ./out folder relative to the CWD

#Improvements?

I was planning to use machine learning to figure out the best screen coordinates. But this method works well enough for now.
