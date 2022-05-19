# Navigating this GitHub
Welcome to the GitHub of DSE Group 06: EcoSense. This README is a
living document and will be updated regularly.
Files are structured as follows:
- Archive: This folder contains all previous scripts which are
            not actively monitored anymore and can therefore be
            ignored.
- Misc: Here, various scripts are stored which are not directly
        related to design calculations, such as sensitivity analysis
        and the analytical hierarchy process.
- Blimp: This directory comprises everything related to Blimp
         design.
- Sensor: This folder houses everything related to Sensor and Sensor
            Network design.

## Blimp Directory
The main file to consider is BLIMP.py, which houses the Blimp class.
This class allows creating different blimp designs with different parameters.
Moreover, methods are created to simulate e.g. the performance of the 
design. 

The folder Pickle Shelf contains python objects, which were pickled
earlier. Analogous to the method of conserving vegetables in jars, any object
in a python code can be stored in a file. This is especially useful for large
objects like Blimp designs, which are generated using iteration, because then they don't
need to be generated anymore each time the program is run, but only if the design is
modified. This saves a lot of time.

As the name Classes suggests, classes are stored here. For example, the solarcells.py
contains a solar cell class, in which different solar cells can be registered.
In the BLIMP file, different designs can be easily equipped with different solar
cell models.

The file test_calc.py was used for unit testing.


