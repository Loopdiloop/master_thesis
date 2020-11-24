# usersort_186W
Sorting of data from the 186W with 30MeV alphas at OCL with usersort without fission.

Usersort code modified from 
https://github.com/cecgresonant/186W-a-30MeV-sort
and 
https://github.com/oslocyclotronlab/usersort

Sorting.cpp based on cecgresonant, as the OCL-version has PPAC-support for fission events.



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Edited excerpt from original readme (from OCL):

**Files**:
* `user_sort.cpp` - the sorting routine

* `/lib` - libraries

* `<Yourfile>.batch` - the file in which all parameters are listed. Before you start using it for your experiment, go through all parameters and set them according to your experiment!
At some point of time you will also want to change:
 * data files
 * the gainshifts file
 * output file name (with the root matrices)
 * the export of "alfna" matrix to mama matrices
I tried to create a rather plain file called `Pu239_dp_rather_default.batch` which you can use as a start. Please remember to fill in the kinematics from rkinz/qkinz of your reaction (see the file).


* `gainshifts_plain.dat` - gains and shifts for the detectors. Change the values to align and calibrate the detectors. It can be a little cumbersome, as the read-out is very sensitive to additional lines/spaces and so on. Always cross-check the parameters that are used by sorting.

* `Makefile` - the makefile. Assumes that the sorting routine is called `user_sort.cpp`

* `.gitignore` - ignore most files that are not listed here (e.g. the output files)


**Basic usage**:

* First, fork your own copy of this repository! Then you can use git as a version controll of changes/adoptions for your experiment
(you might *watch* the original repository to get updates on changes - or even keep the fork synced:
https://help.github.com/articles/fork-a-repo/ )

* Clone your repository
`git clone https://github.com/YOUR-USERNAME/usersort`

* Usage:

make very-clean
make
./sorting <Yourfile>.batch


