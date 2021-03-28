# infrared-images-noise-removal

The project aims in the analysis of infrared Sample Up The Ramp images.
The project aims to minimize high background noise from the infrared FITS image data to view the clearer infrared image of densely distributed stars and distinguish faint low mass stars which are not clear due to disturbances in the earth’s atmosphere.

Also, clearer image of the faint low mass stars helps the astronomers to carry out multiple inferences related to the M53’s star as they are very far away.

Installation
```
pip install astropy
pip install numpy
pip install natsort
pip install numexpr
```

Values to change
```
path : path of fits images
xmin : minimum x-cordinate value
xmax : maximum x-cordinate value
ymin : minimum y-cordinate value
ymax : maximum y-cordinate value

FullTile : Full Tile is the total size of image 
sec:Section of cube you want to load into data cube (xmin,xmax,ymin,ymax)

time : No of files 
timethresh : Files left after subtracting from other files from first file(which is taken as threshold): usually(time-1) 
```

Use the [sed fitting](https://sedfitter.readthedocs.io/) tool to see proper infrared visualisations.


