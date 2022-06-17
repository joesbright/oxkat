#!/usr/bin/env python
# ian.heywood@physics.ox.ac.uk


import glob
import os
import random 
import string

from astropy.io import fits
from astropy.time import Time
from multiprocessing import Pool
from PIL import Image,ImageDraw,ImageFont

fontPath = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
sans18  =  ImageFont.truetype ( fontPath, 18 )



def generate_temp(k=16):
	tmpfits = 'temp_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=k))+'.fits'
	return tmpfits


def make_png(ff)

	tmpfits = generate_temp()

	os.system('mShrink '+ff+' '+tmpfits+' 2')

	input_hdu = fits.open(ff)[0]
	hdr = input_hdu.header
	map_date = hdr.get('DATE-OBS')
	t_mjd = Time(map_date, format='isot', scale='utc').mjd
	tt = map_date+' | '+str(t_mjd)
#	pp = str(i).zfill(4)+'_'+ff.replace('.fits','.png')
	pp = 'pic_'+str(i).zfill(4)+'.png'
#	syscall = 'mViewer -ct 0 -gray '+ff+' -0.0004 0.0008 -out '+pp
	syscall = 'mViewer -ct 0 -gray '+tmpfits+' -0.0004 0.0008 -out '+pp
	os.system(syscall)
	print(syscall)
	img = Image.open(pp)
	xx,yy = img.size
	draw = ImageDraw.Draw(img)
	draw.text((0.03*xx,0.90*yy),'Frame : '+str(i).zfill(len(str(nframes)))+' / '+str(nframes),fill=('white'),font=sans18)
	draw.text((0.03*xx,0.93*yy),'Time  : '+tt,fill=('white'),font=sans18)
	draw.text((0.03*xx,0.96*yy),'Image : '+ff,fill=('white'),font=sans18)
	img.save(pp)
	i+=1
	os.system('rm '+tmpfits)

if __name__ == '__main__':

	fitslist = sorted(glob.glob('*-t*-image-restored.fits'))
	nframes = len(fitslist)
	i = 1
	j = 8

    pool = Pool(processes=j)
    pool.map(make_png,fitslist)

	frame = '2340x2340'
	fps = 10
	opmovie = fitslist[0].split('-t')[0]+'.mp4'
	os.system('ffmpeg -r '+str(fps)+' -f image2 -s '+frame+' -i pic_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p '+opmovie)
