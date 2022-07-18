
## `bctWrapper`

- This is my wrapper code that takes a list of feature names as the
  input, along with the path to your connectomes folder and a list 
  of subject names for which the features will get calculated. 
- It then calculates the graph theory features and saves them in 
  spearate text files for each graph theory measure. 
- The .zip file continas example script, which should make it easy to 
  understand how it works.


## `QA` 

- folder contains python scripts along with a bash script that I used for
  the quality assessment of connectomes. The code might be a little
  messy. 
- I didn't have enough time to prepare a test folder that would work on 
  your computer without issues. So, you might need to put some effort 
  to make it to work.


## `helpers.py`

- python script includes multiple functions that I used for doing basic 
  statistical tests and plotting their results, such as:
  - drawing histograms, 
  - calculating group differences, 
  - making box plots etc. 
- Put this script file under the same folder as your python code and 
  import the functions that you'd like to call from your code.