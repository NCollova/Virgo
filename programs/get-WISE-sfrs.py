from astropy.io import fits
import sys
sys.path.append('./CharyElbaz/')
import chary_elbaz_24um as chary
import numpy as np
import os

mypath=os.getcwd()
if mypath.find('rfinn') > -1:
    catpath='/Users/rfinn/github/Virgo/tables'
elif mypath.find('kelly') > -1:
    print "Running on Kellys's computer"
    catpath='/Users/kellywhalen/Github/Virgo/tables/'


wise = fits.getdata(catpath+'WISE_virgo.fits')
nsa = fits.getdata(catpath+'VirgoCatalog.fits')

# galaxies with reliable W4 flux
wflag =  (wise.W4MPRO > 0.1) & (wise.W4SNR > 3.)

# set up arrays to hold flux, sfr, Lir
w4_flux_Jy = np.zeros(len(wise),'f')
ce_sfr = np.zeros(len(wise),'f')
ce_lir = np.zeros(len(wise),'f')

# zeropoint of magnitude scale from
# http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html#Summary
F0 = 8.363

# calculate flux in Jy for galaxies with W4 detections
w4_flux_Jy[wflag] = F0*10**(-1*wise.W4MPRO[wflag]/2.5)

# calculate chary & elbaz sfr and Lir

ce_lir[wflag],ce_sfr[wflag]=chary.chary_elbaz_24um(nsa.Z[wflag],w4_flux_Jy[wflag]*1.e6)

# write out sfr and Lir to a fits table
wdat = fits.open(catpath + 'WISE_virgo.fits')[1].data
sfrcol = np.zeros(len(wdat))
sfrcol[wflag] = ce_sfr[wflag]
sfrcol_new = fits.Column(name = 'SFR', format = 'D', array = sfrcol)

lircol = np.zeros(len(wdat))
lircol[wflag] = ce_lir[wflag]
lircol_new = fits.Column(name = 'Lir', format = 'D', array = lircol)

origcols = wdat.columns
hdu = fits.BinTableHDU.from_columns(origcols + sfrcol_new + lircol_new)
outfile = catpath + 'WISE_virgo.fits'
hdu.writeto(outfile, clobber = 'True')
