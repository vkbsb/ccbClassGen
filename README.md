# ccbClassGen
simple python script for generating .cpp and .h files for CocosBuilder files with custom classes.

# USAGE
MainMenu.ccb is a sample ccb file that you can test the script on, here is how you run it:

`python ccbClassGen.py MainMenu.ccb`

The above will generate the custom class defined for the MainMenu.ccb.
In this example the custom class defined for MainMenu.ccb is  "WordRushMain".
The script will generate WordRushMain.cpp and WordRushMain.h files with all the
member variables and member functions defined / required for the class.


#TODO

1) Makesure you do not add duplicate member variables.
2) MakeSure that duplicate method access do not create multiple functions.
3) Code merging instead of replacing, for incremental updates on ccb files.
