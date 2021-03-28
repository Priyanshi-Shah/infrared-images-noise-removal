#This code is written for Windows OS. Only changes directory paths for linux

#importing the libraries
from astropy.io import fits 
import glob
import numpy as np
import natsort
import numexpr as ne
from astropy.table import Table


def LoadDataCube(tile =FullTile, NoofNDRs=None):
    NDRfilesT=glob.glob(path)  
    NDRfiles=natsort.natsorted(NDRfilesT,reverse=False)
    if NoofNDRs==None : NoofNDRs=len(NDRfiles)

    #print(NDRfiles)
    datacube=np.empty((NoofNDRs,tile[1]-tile[0],tile[3]-tile[2]),dtype=np.float32)
    for i,img in enumerate((fits.getdata(NDR).astype(np.float32)[tile[0]:tile[1],tile[2]:tile[3]] for NDR in NDRfiles[:NoofNDRs])) : datacube[i,:,:]=img
    return datacube



def FitSlope(imgcube,time):
    time=np.arange(newcube.shape[0],dtype=np.float64)+1 #adding 1 because it took time values(number of images) from 0 .We need  from 1
    tshape=tuple(np.roll(newcube.shape,-1)) #unrolling in the form of (x,y,no_of_ima0ges (or Time))
 
    #Parameters used in the formula
    Sx=np.ma.array(np.transpose(np.resize(time,tshape),(2,0,1)),mask=np.ma.getmaskarray(newcube)).sum(axis=0,dtype=np.int64)
    Sxx=np.ma.array(np.transpose(np.resize(np.square(time),tshape),(2,0,1)),mask=np.ma.getmaskarray(newcube)).sum(axis=0,dtype=np.float64)
    Sy=np.mean(newcube, axis=0,dtype=np.int64) #directly calculate mean to Sy
    #Sy=imgcube.sum(axis=0,dtype=np.float64) for sum of sy
    Sxsx=(Sx*Sx)
    Syy=(np.square(newcube)).sum(axis=0,dtype=np.float64)
    Sxy=(newcube*time[:,np.newaxis,np.newaxis]).sum(axis=0,dtype=np.float64)
    n=np.ma.count(imgcube,axis=0)   #number of points used in fitting slope of a pixel   
     
    """
    Formula used 
    beta= (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    alpha = mean(ys) - beta*mean(xs)
    """
    beta= ne.evaluate("(( (Sx)/n *Sy)-(Sxy/n))/(  (Sxsx /(n*n))  -(Sxx/n))")
    alpha= ne.evaluate("Sy - (beta*(Sx/n)) ")
    
    return beta, alpha

    
if __name__ == '__main__':
    ### Values to change ###
    path='D:\\Sample Fits\\\M53*.fits' #path of images
    xmin=0
    xmax=416
    ymin=0
    ymax=480
    FullTile=(xmin,xmax,ymin,ymax)#Full Tile is the total size of image 
    sec=(xmin,xmax,ymin,ymax) #Section of cube you want to load into data cube

    time=105 #No of files 
    timethresh=104 #Files left after subtracting from other files from first file(which is taken as threshold) 
    ### Values to change END ###


    #Loading data as an Image Cube with 3 dimensions
    imgcube=LoadDataCube(tile=sec)
    
    #Making New cube by subtracting all other image pixel values from first image values
    newcube=np.zeros((timethresh,xmax,ymax))          
    for i in range(time):
            for j in range(xmax) :
                for k in range(ymax):
                    newcube[i-1,j,k]=imgcube[0,j,k]-imgcube[i,j,k]  #First image values - all other image values
                
                
    #print(imgcube.shape) #Check shape of imgcube
    #print(newcube.shape) #Check shape of new cube(should be 1 less in dimension as all images have been subtracted from the first one)
    time=np.arange(newcube.shape[0],dtype=np.int) #counting number of images i.e.0th dimension
    beta,alpha=FitSlope(newcube,time)#, CRcorr=True)
    #here beta and alpha can be related m and b of the equation y=mx+b
    m = beta.flatten() 
    m=m.tolist()

    #Writing into  text file......Use only if required
    """with open('Storeslopenewval.txt', 'w+') as f:
        for item in m:
            f.write("%s\n" % round(item,4))
    """
    #Reading from  text file to list.......Use only if required
    """linelist=[]
    with open('Storeslopenewval.txt', 'r') as f:
            linelist = f.read().splitlines()
            #print(len(linelist))
    """
    
    a=[]
    b=[]
    #Change size here to your maximum x and y pixel coordinates
    for p in range(0,xmax):
        for q in range(0,ymax):
            a.append(p)
            b.append(q)                
                    
    #Change the paths of your directory according to Windows or linux   
    #Writing data to table file Making a table fits file which will contain data as a table
    #This table's content cannot be viewed in IRAF dircectly.Continue below to make IRAF readable file below
    t = Table([a,b, m], names=('x', 'y', 'slope'))
    t.write('Slopetable.fits', format='fits',overwrite=True) 
    
    #Reading data from  table file
    
    table = Table.read('Slopetable.fits')   # see path
    #Too see information of table using terminal in python uncomment the code below
    """
    hdu_list1 = fits.open('Slopetable.fits')
    hdu_list1.info()
    print(table)
    hdu_list1.info()
    image_data1 = hdu_list1[0].data
    print(type(image_data1))
    print(image_data1)
    hdu_list1.close()"""
    
    #Writing table data to another fits file to View in IRAF softare directly
    intensity = table[::2]
    img = np.zeros((xmax,ymax)) #change size here to your maximum x and y pixel coordinates
    for x, y, intensity in table:
        img[x, y] = float(intensity) 

    fits.writeto('Slopetable_final.fits', img) #Put path here where image is to be stored
    
    
    """
    #To visualise data image using python(just like in IRAF) uncomment the section below
    import matplotlib.pyplot as plt
    hdu_list = fits.open('D:\\Slopetable_final.fits')
    #hdu_list.info()
    image_data = hdu_list[0].data
    #print(type(image_data))
    #print(image_data.shape)
    hdu_list.close()
    from matplotlib.colors import LogNorm
    plt.imshow(image_data, cmap='gray', norm=LogNorm())
    plt.colorbar()
    """


    
    
    
    
    
    
    
    
    
    