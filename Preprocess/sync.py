# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 17:11:29 2017

@author: gonca
"""

import numpy as np
import pandas as pd

def read_sync(syncpath,counterpath):
    """
    Reconstructs ephys and video synchronization indices allowing to map
    individual frame indices into the corresponding ephys sample numbers, and
    vice-versa.
    
    Parameters
    ----------
    syncpath :
        the path to the ephys TTL file containing camera shutter data
        (e.g. 'sync.bin')
    counterpath :
        the path to the CSV file containing camera frame timestamp and embedded
        hardware frame counter data (e.g. 'counter.csv')
    
    Returns
    -------
    ephysidx
        a dataframe mapping the zero-based frame index   value in a string
    frameidx
        a dataframe mapping ephys sample numbers into the corresponding
        zero-based frame index
    frame
        a dataframe containing timestamp, hardware embedded frame counter and
        number of frames dropped for every acquired frame
    """
    
    # Read raw sync camera shutter data (8-bit TTL - 1 is OPEN and 0 is CLOSED)
    # NOTE: Sync data is uint8, but because values are only 0 or 1, we can
    # NOTE: also open it directly as int8 with no loss of information
    sync = np.fromfile(syncpath,dtype=np.int8)
    
    # Find the falling edges of the shutter data (end of frame exposure)
    syncidx = np.flatnonzero(np.diff(sync) < 0)
    
    # Read hardware embedded frame counter data
    frame = pd.read_csv(counterpath,
                        header=None,sep=' ',
                        names=['time','counter'],
                        parse_dates=[0],
                        usecols=[0,1])
    
    # Compute the total number of contiguous frames acquired in the session
    dropframes = frame.counter.diff() - 1
    total_frames = len(frame.counter) + dropframes.sum()

    # Check if all frame exposures have been accounted for
    if len(syncidx) != total_frames:
      print(str.format("WARNING: Number of frames ({0}) ",total_frames) +\
            str.format("does not match number of pulses ({0})!",len(syncidx))+\
            str.format(" Patching..."))
      
      # If there are less exposures in ephys than frames in video, pad data
      if len(syncidx) < total_frames:
          nmissing = total_frames - len(syncidx)
          syncidx = np.insert(syncidx,-1,np.repeat(syncidx[-1],nmissing))

    # Create the frame-to-ephys index (input is frame number)
    ephysidx = pd.DataFrame(syncidx,columns=['sample'])
    
    # Create the ephys-to-frame index (input is ephys sample number)
    frameidx = np.zeros(sync.shape,dtype=np.int)
    frameidx[0] = -1
    frameidx[ephysidx.values] = 1
    frameidx = pd.DataFrame(frameidx,columns=['frame']).cumsum()
    
    # Create a new column for dropped frames
    dropframes.name = 'dropframes'
    frame = pd.concat([frame,dropframes],axis=1)
    
    return ephysidx,frameidx,frame
