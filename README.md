#What is this?

It generates MAME .lay Layout files for bezel artworks.

#How to use
* First edit the "dirName" path variable to your bezel artwork folder. 

* Then run the program. It will pop up an image of each bezel. It will draw a guess as to the rectangle that might work for your game.
If the guess is not good enough, then redraw by clicking in the upper-left and dragging to the botom right, then releasing the mouse button.

* When you are satisfied, then just hit a key (space, or whatever). It will copy the image and generate a .Lay file, 

* All results will be output inside the /out folder relative to the CWD

#Improvements?

I was planning to use machine learning to figure out the best screen coordinates. But this method works well enough for now.