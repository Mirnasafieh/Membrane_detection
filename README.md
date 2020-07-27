----------------------------
Membrane detection project:
----------------------------
By Mirna Safieh and Hila Ben-moshe:


Description: 
------------
This projects allows the user to detect the membrane of the cell utilizing a brightfeild extracted from confocal microscopy image using image processing.
After the detection of the membrane, the flurecence of a protein and the area it coveres are measured in the compatible image (channel), allowing  quanification and analysis 
of membrane-bound protein.

imput:
-------

Class Hierachy:
---------------

		        |-------------------------|             |-----------------------|
                |     brightfeild image   |             |    flurescent image   |
                |-------------------------|             |-----------------------|
                           ^                                ^  ^
                          /                                 |  |
                         /                                  |  |
                        /                                   |  |
             image processing                               |  |
         and membrane detection    --|  |
                     /                         |
                    /                                        is-a 
                   /                                           |
    |-------------------------|                                 |------------|
    | binary image of membrane|--------------------------->| AVLNode    |
    |-------------------------|                                  |------------|





output:
--------