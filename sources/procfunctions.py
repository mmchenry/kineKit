""" proFunctions
Used for analysis of DLC data for seastar geotaxis project.
"""

import pandas as pd
import numpy as np
import os.path as ph
import glob

import pltFunctions as pt


def refine_all(raw_coord_path, refine_coord_path, cat_path):
    """ Loops through all raw DLC coord files and generates refined coord files, using refine_data 
    
    raw_coord_path:     Path of raw coord data, as generated by DLC
    refine_coord_path:  Path to refined coord data
    cat_path:           Path to video catalog file
    """

    fr_rate    = 1;
    land_types = ['arm','chip']
    arm_nums   = np.arange(5)+1

    # Load list of DLC raw data files
    if ph.isdir(raw_coord_path):
        d_files = glob.glob(raw_coord_path + ph.sep + '*filtered.h5')
    else:
        raise ValueError('vid_path not recognized')

    # Load video catalog
    cat = pd.read_csv(cat_path)

    # Loop thru all raw coord files in d_files
    for c_path in d_files:

        # Load current DLC raw coord from list
        c_filename = ph.basename(c_path)
        df_raw     = pd.read_hdf(c_path)

        # Define rows of catalog that have useful data
        loc_data = np.arange(np.where(pd.isna(cat.date))[0][0])

        # index of data (loc_cat) from video catalog that matches sequence
        i_start = int(11)
        i_end = int(c_filename.index('DLC'))

        # find location (row) of the catalog that matches the data filename
        trials = cat.trial_num[loc_data]
        dates  = cat.date[loc_data]
        i_cat_seq = (dates==c_filename[0:10]) & (trials.astype('int')==int(c_filename[i_start:i_end]))
        loc_cat = np.where(i_cat_seq)[0]

        # Check that only one match found in catalog spreadsheet
        if len(loc_cat)<1:
            raise ValueError('No matching sequence found in video_catalog')
        elif len(loc_cat)>1:
            raise ValueError('More than one matching sequence found in video_catalog')
        
        # Output filename for the data
        seq_str = '0' + c_filename[i_start:i_end]
        f_name_save = c_filename[0:10] + '_' + seq_str[-2:] + '_refined' + '.pkl.xz'

        # From catalog: Current orientation
        c_orient = int(cat.orientation[loc_cat])

        # Flip y, if 0 orientation
        if c_orient==0:
            y_height = cat.roi_h.values[loc_cat][0]
        else:
            y_height = 0

        # Define refined dataframe from raw dataframe
        df = refine_data(df_raw, land_types, arm_nums, y_height,fr_rate)

        # write to disk
        ref_path = refine_coord_path+ph.sep+f_name_save
        df.to_pickle(ref_path,compression='infer')

        # Update status
        print('   Refined data file saved to disk:' + ref_path)

    print('---------------------------------------------------------')
    print('Completed generating refined data files from raw data')


def refine_data(df_raw, land_types, arm_nums, y_height,fr_rate):
    """ Accepts raw DLC coordinate datatable (df_raw) and outputs newly-organized datatable
    
    df_raw:     Data frame of raw coordinates (as generated by DLC)
    land_types: Types of landmarks (e.g., 'arm', 'chip') 
    arm_nums:   List of arm numbers (0,1,2,3,4) 
    y_height:   Vertical height of video frame
    fr_rate:    Frame rate of video recording
    """

    # Read data and extract 'scorer' value from DLC
    scorer = list(df_raw)[0][0]

    # Initialize series to receive columns of data
    # df = pd.DataFrame
    fr_num      = pd.Series(dtype='int')
    time_s      = pd.Series(dtype='float')
    body_pos    = pd.Series(dtype='str')
    arm_num     = pd.Series(dtype='int')
    dim         = pd.Series(dtype='str')
    coord_pix   = pd.Series(dtype='float')
    # coord_pix = np.array([],dtype='float')

    # Gather values for writing to new dataframe ---------------------

    # Loop thru types of landmarks
    for c_land in land_types:

        # Loop thru arm numbers
        for c_arm in arm_nums:

                # Define current part number
                part_name = c_land + str(c_arm)

                # Extract coordinates from DLC data for current landmark
                x = df_raw[scorer][part_name]['x']
                y = df_raw[scorer][part_name]['y']

                # Remove outlier points
                x,y = fix_outlier_coord(x,y,0.05)

                # Flip y, if 0 orientation
                y = np.abs(y_height - y)

                # Make list of 'x' and 'y' as strings to designate the dimensions
                x_dim     = pd.Series('x').repeat(len(x))
                y_dim     = pd.Series('y').repeat(len(y))

                c_frame_num = pd.Series(np.concatenate([x.index,y.index]))
                # Cue up the columns of data
                
                dim       = pd.concat([dim, pd.Series(np.concatenate([x_dim,y_dim]))])
                # coord_pix = pd.concat([coord_pix, pd.Series(np.concatenate([x,y]))])
                coord_pix = np.concatenate([coord_pix,x,y])
                fr_num    = pd.concat([fr_num, c_frame_num])
                time_s    = pd.concat([time_s, c_frame_num/fr_rate])
                body_pos  = pd.concat([body_pos, pd.Series(c_land).repeat(len(c_frame_num))])
                arm_num   = pd.concat([arm_num, pd.Series(c_arm).repeat(len(c_frame_num))])

    # Reset indicies
    fr_num    = fr_num.reset_index(drop=True)
    time_s    = time_s.reset_index(drop=True)
    body_pos  = body_pos.reset_index(drop=True)
    arm_num   = arm_num.reset_index(drop=True)
    dim       = dim.reset_index(drop=True)

    # Pile into dataframe
    df = pd.DataFrame(coord_pix,index=[body_pos,arm_num,dim,fr_num],columns=['coord_pix'])
    df.index.names = ['body_pos','arm_num','dim','fr_num']

    return df


def fix_outlier_coord(x,y,quantile=0.25):
    """ Scans through DLC coodinate data, identifies outliers, and replaces them with linearly-interpolated values.
    
    x,y:        Coordinates
    quantile:   Identifies the bounds of the outlier (0.25 = quartile)
    """

    # Displacement btwn points
    disp = np.sqrt(np.power(np.diff(x),2) + np.power(np.diff(y),2))

    # find q1 and q3 values
    q1, q3 = np.percentile(sorted(disp), [100*quantile, 100-100*quantile])
 
    # compute IRQ (Interquartile range)
    iqr = q3 - q1
 
    # find lower and upper bounds
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    
    # Identify outliers
    outliers = [x for x in disp if x <= lower_bound or x >= upper_bound]
    
    # Raise error, if too many outliers
    if len(outliers) > len(x)/10:
        raise ValueError('Too many outlier values here. Try reducing quantile value')

    # Interpolate over outlier values, if they exist
    elif len(outliers)>0:

        # Loop thru outlier values
        for idx in range(len(outliers)):
            
            # Location of outlier value
            i_out = np.where(disp==outliers[idx])[0][0]

            # If it's the first value . . .
            if np.max(i_out==0):
                x[0] = x[1]-(x[2]-x[1])
                y[0] = y[1]-(y[2]-y[1])

            # If it's the last value . . .
            elif np.max(i_out==len(disp)):
                x[len(x)-1] = x[len(x)-2] + (x[len(x)-2]-x[len(x)-3])
                y[len(y)-1] = y[len(y)-2] + (y[len(y)-2]-y[len(y)-3])

            # If it's a value in the middle
            else:
                # Tweak index
                i_out = i_out+1

                # Define values that skip the outlier
                vals        = np.concatenate((x.index[0:i_out],x.index[i_out+1:])) 
                xTmp        = np.concatenate((x[0:i_out],x[i_out+1:]))  
                yTmp        = np.concatenate((y[0:i_out],y[i_out+1:]))   

                # Replace faulty coordinate
                x[i_out]    = np.interp(i_out,vals,xTmp);
                y[i_out]    = np.interp(i_out,vals,yTmp);
    return x, y


def derive_all(refine_coord_path, f_suffix='*refined.pkl.xz', heading_win=10):
    """ Loops through all refined sequences to calculate derived variables (e.g., centroid, heading) from refined data.

    refine_coord_path:  Path to refined data
    f_suffix:           File suffix for data files
    heading_win:        Number of points skipped to calculate heading from displacement
    """

    #  Load list of DLC raw data files
    if ph.isdir(refine_coord_path):
        d_files = glob.glob(refine_coord_path + ph.sep + f_suffix)
    else:
        raise ValueError('vid_path not recognized')

    # Loop thru data files
    for c_path in d_files:

        # Load dataframe from current path
        df = pd.read_pickle(c_path)

        # Calculate derived data
        df_der = derive_data(df, heading_win=heading_win)

        # write to disk
        f_name_save = ph.basename(c_path)[:13] + '_derived.pkl.xz'
        ref_path = refine_coord_path+ph.sep+f_name_save
        df_der.to_pickle(ref_path,compression='infer')

        # Update status
        print('Derived data file saved to disk:')
        print('     ' + ref_path)

    print('---------------------------------------------------------')
    print('Completed generating derived data files from refined data')


def derive_data(df,heading_win=10):
    """ Calculate derived variables (e.g., centroid, heading) from refined data.

    df: dataframe of refined version of the data.
    heading_win:        Number of points skipped to calculate heading from displacement
    """

    import numpy.matlib

    # For calculating a running average (smoothing)
    def running_mean(x, N=10):
        out = np.zeros_like(x, dtype=np.float64)
        dim_len = x.shape[0]
        for i in range(dim_len):
            if N%2 == 0:
                a, b = i - (N-1)//2, i + (N-1)//2 + 2
            else:
                a, b = i - (N-1)//2, i + (N-1)//2 + 1

            #cap indices to min and max indices
            a = max(0, a)
            b = min(dim_len, b)
            out[i] = np.mean(x[a:b])
        return out

    # Parameters
    arm_nums   = np.arange(5)+1
    fr_rate    = 1

    # List of sorted unique frame numbers
    fr_nums = df.loc[('arm',1,'x'),:].index.unique()
    fr_nums.sort_values()

    # Initialize series for columns of data
    fr_num      = pd.Series(dtype='int')
    time_s      = pd.Series(dtype='float')
    x_cntr_pix  = pd.Series(dtype='float')
    y_cntr_pix  = pd.Series(dtype='float')
    x_arm1_pix  = pd.Series(dtype='float')
    y_arm1_pix  = pd.Series(dtype='float')
    x_arm2_pix  = pd.Series(dtype='float')
    y_arm2_pix  = pd.Series(dtype='float')
    x_arm3_pix  = pd.Series(dtype='float')
    y_arm3_pix  = pd.Series(dtype='float')
    x_arm4_pix  = pd.Series(dtype='float')
    y_arm4_pix  = pd.Series(dtype='float')
    x_arm5_pix  = pd.Series(dtype='float')
    y_arm5_pix  = pd.Series(dtype='float')

    # Arrays for tracking previous coords and radial position
    last_coord = np.empty((1,5,))[0]*np.nan
    last_rad   = np.nan

    # Loop through time
    for frame in fr_nums:

        # Coordinate containers
        c_x = np.array([],dtype='float')
        c_y = np.array([],dtype='float')
        a_x = np.array([],dtype='float')
        a_y = np.array([],dtype='float')

        # Loop thru arms, extract coords for current frame
        for c_arm in arm_nums:             
            c_loc  = np.where(df.loc[('chip',c_arm,'x'),:].index==frame)[0]
            c_x    = np.append(c_x,
                    df.loc[('chip',c_arm,'x'),:].coord_pix[c_loc])
            c_y    = np.append(c_y,
                    df.loc[('chip',c_arm,'y'),:].coord_pix[c_loc])
            a_x    = np.append(a_x,
                    df.loc[('arm',c_arm,'x'),:].coord_pix[c_loc])
            a_y    = np.append(a_y,
                    df.loc[('arm',c_arm,'y'),:].coord_pix[c_loc])
            
        # Store time
        c_time      = df.loc[('chip',c_arm,'x'),:].index[c_loc][0]/fr_rate
        fr_num      = pd.concat([fr_num, pd.Series(frame)])
        time_s      = pd.concat([time_s, pd.Series(c_time)])

        # Store center position
        x_cntr_pix = pd.concat([x_cntr_pix, pd.Series(np.mean(c_x))])
        y_cntr_pix = pd.concat([y_cntr_pix, pd.Series(np.mean(c_y))])

        # Find radial positions of the arms
        c_rad = np.arctan2(a_y-np.mean(c_y),a_x-np.mean(c_x))

        # On first frame, identify lead arm as the one pointing up
        if np.max(np.isnan(last_coord)):
            vert_diff = abs(np.pi/2-np.arctan2(a_y-np.mean(c_y),a_x-np.mean(c_x)))
            loc_arm_up = np.where(vert_diff==np.min(vert_diff))
            # loc_arm_up = np.where(a_y==np.max(a_y))[0]
  
        # Identify the lead arm as the one closest to the previous
        else:
            rad_c = np.abs(c_rad-np.matlib.repmat(last_rad,1,5))[0]
            loc_arm_up = np.where(rad_c==np.min(rad_c))
            # disp = np.hypot(a_x-last_coord[0],a_y-last_coord[1])
            # loc_arm_up = np.where(disp==np.min(disp))
            
        # Order the other arms by radial position CCW wrt arm1
        arm_order = np.argsort(np.unwrap(c_rad-c_rad[loc_arm_up]))

        # Store arm coords in order
        x_arm1_pix = pd.concat([x_arm1_pix, pd.Series(a_x[arm_order[0]])])
        y_arm1_pix = pd.concat([y_arm1_pix, pd.Series(a_y[arm_order[0]])])
        x_arm2_pix = pd.concat([x_arm2_pix, pd.Series(a_x[arm_order[1]])])
        y_arm2_pix = pd.concat([y_arm2_pix, pd.Series(a_y[arm_order[1]])])
        x_arm3_pix = pd.concat([x_arm3_pix, pd.Series(a_x[arm_order[2]])])
        y_arm3_pix = pd.concat([y_arm3_pix, pd.Series(a_y[arm_order[2]])])
        x_arm4_pix = pd.concat([x_arm4_pix, pd.Series(a_x[arm_order[3]])])
        y_arm4_pix = pd.concat([y_arm4_pix, pd.Series(a_y[arm_order[3]])])
        x_arm5_pix = pd.concat([x_arm5_pix, pd.Series(a_x[arm_order[4]])])
        y_arm5_pix = pd.concat([y_arm5_pix, pd.Series(a_y[arm_order[4]])])

        # Store coord as last
        last_coord = np.array([a_x[loc_arm_up],a_y[loc_arm_up]])

        # Store radial position as last
        last_rad = c_rad[loc_arm_up]

    # Smooth x and y coordinates
    x_cntr_sm  = running_mean(x_cntr_pix, 20)
    y_cntr_sm  = running_mean(y_cntr_pix, 20)
    x_arm_sm   = running_mean(x_arm1_pix, 20)
    y_arm_sm   = running_mean(y_arm1_pix, 20)

    # Calculate heading from body orientation
    head_rad = pd.Series(
                np.arctan2(y_arm_sm-y_cntr_sm,x_arm_sm-x_cntr_sm),
                dtype='float')

    head_disp_rad  = pd.Series(dtype='float')
    x_last = x_cntr_sm[0]; y_last = y_cntr_sm[0]
    # Calculate heading from displacement
    for c_pt in range(len(x_cntr_sm)-heading_win+1):

        # Current angle value
        c_ang = np.arctan2(y_cntr_sm[c_pt]-y_last,
                         x_cntr_sm[c_pt]-x_last)

        # Store value
        head_disp_rad = pd.concat([head_disp_rad, 
                        pd.Series(c_ang)])

        x_last = x_cntr_sm[c_pt]; y_last = y_cntr_sm[c_pt]

    # Calculate speed (add redundant value at end)
    spd = pd.Series(
            np.hypot(np.diff(x_cntr_sm),np.diff(y_cntr_sm)),
            dtype='float') / np.diff(time_s)
    spd = np.append(spd,spd[-1:])

    # Displacement
    displ = pd.Series(
                np.cumsum(np.hypot(np.diff(x_cntr_sm),np.diff(y_cntr_sm))),
                dtype='float'
            )

    # Plot smoothing on body center (diagnostic)
    if False:
        pt.timeseries(df.time_s,df.x_cntr_pix,running_mean(df.x_cntr_pix,20))
        pt.timeseries(df.time_s,df.y_cntr_pix,running_mean(df.y_cntr_pix,20))
    # Example of extracting values
    # tmp = df.loc[('arm',1,'x'),:].coord_pix

    # reset indices
    new_idx             = np.arange(len(fr_num))
    fr_num.index        = new_idx
    time_s.index        = new_idx
    x_cntr_pix.index    = new_idx
    y_cntr_pix.index    = new_idx
    x_arm1_pix.index    = new_idx
    y_arm1_pix.index    = new_idx
    x_arm2_pix.index    = new_idx
    y_arm2_pix.index    = new_idx
    x_arm3_pix.index    = new_idx
    y_arm3_pix.index    = new_idx
    x_arm4_pix.index    = new_idx
    y_arm4_pix.index    = new_idx
    x_arm5_pix.index    = new_idx
    y_arm5_pix.index    = new_idx
    head_rad.index      = new_idx

    # Set for displacement heading, add time vector
    head_disp_rad.index = np.arange(len(head_disp_rad))
    t_head_disp         = time_s[:len(head_disp_rad)]

    # dataframe for derived values
    d_frame = {'fr_num': fr_num,
            'time_s': time_s,
            'x_cntr_pix': x_cntr_sm,
            'y_cntr_pix': y_cntr_sm,
            'x_arm1_pix': x_arm_sm,
            'y_arm1_pix': y_arm_sm,
            'x_arm2_pix': x_arm_sm,
            'y_arm2_pix': y_arm_sm,
            'x_arm3_pix': x_arm_sm,
            'y_arm3_pix': y_arm_sm,
            'x_arm4_pix': x_arm_sm,
            'y_arm4_pix': y_arm_sm,
            'x_arm5_pix': x_arm_sm,
            'y_arm5_pix': y_arm_sm,
            'head_rad': head_rad,
            'spd_pixs': spd,
            'displ_pix': displ,
            't_head_disp': t_head_disp,
            'head_disp_rad': head_disp_rad
            }  
    df_der = pd.DataFrame(d_frame)

    return df_der


def plt_all_traj(refine_coord_path, cat_path, f_suffix='*derived.pkl.xz', save_path=None):
    """ Steps through sequences to plot all trajectories
    
    refine_coord_path:      Path to refined coordinate data
    cat_path:               Path to video catalog file
    f_suffix:               Suffix for derived data files
    save_path:              Directory path for saving files
    """

    import matplotlib.pyplot as plt 

    # Enhance resolution
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['savefig.dpi'] = 300

    # Buffer for ticks
    t_buff = 0.05

    # Numbr of rows and columns per figure
    num_cols = 3
    num_rows = 3

    # Load list of DLC raw data files
    if ph.isdir(refine_coord_path):
        d_files = glob.glob(refine_coord_path + ph.sep + f_suffix)
    else:
        raise ValueError('path not recognized')

    # List of figures to make
    num_figs = int(np.ceil(len(d_files)/(num_cols*num_rows)))

    # plot indicies
    # fi_num = 1
    row_num = 0
    col_num = 0

    # Initialize range of values
    min_x     = np.array([],dtype=float)
    min_y     = np.array([],dtype=float)
    max_x     = np.array([],dtype=float)
    max_y     = np.array([],dtype=float)
    ang_deg   = np.array([],dtype=int)

    # Get the range of values among all data (for setting plot axes and ticks)
    for c_file in d_files:

        # Read dataframe
        df = pd.read_pickle(c_file)

        # Add min/max values
        min_x = np.append(min_x,np.min(df.x_cntr_pix))
        min_y = np.append(min_y,np.min(df.y_cntr_pix))
        max_x = np.append(max_x,np.max(df.x_cntr_pix))
        max_y = np.append(max_y,np.max(df.y_cntr_pix))

        # Sequence information to extract from catalog
        ex_date   = ph.basename(c_file)[:10]
        ex_seq    = ph.basename(c_file)[11:13]
        col_name  = 'angle_deg'

        # Extract angle for current sequence
        ang_deg = np.append(ang_deg,int(get_cat_value(cat_path, ex_date, ex_seq, 
                    col_name  = 'angle_deg')))

    # Index for order of figures, in order of angle of slopes
    loc_fig = np.argsort(ang_deg)

    # Range along x and y
    rng_y   = max_y-min_y
    rng_x   = max_x-min_x

    # Find overall range values
    min_x   = np.min(min_x)
    max_x   = np.max(max_x)
    # mean_x  = np.mean([min_x,max_x])
    min_y   = np.min(min_y)
    max_y   = np.max(max_y)

    # Largest range
    rng = np.max([np.max(rng_y),np.max(rng_x)])*(1+2*t_buff)

    # Index of current file, plot number
    n_plt     = 0
    breakAll  = False

    # Loop thru figures
    for c_fig in range(num_figs):

        # Create figure
        fig, axs = plt.subplots(num_rows, num_cols)
        fig.set_size_inches(12,12)
        # fig.set_facecolor='w'

        # Loop thru rows
        for row_num in range(num_rows):
            # Loop thru columns of subplots
            for col_num in range(num_cols):

                if n_plt<len(d_files)-1:
                    
                    # Current file
                    c_file = d_files[loc_fig[n_plt]]

                    # Load dataframe from current path
                    df = pd.read_pickle(c_file)

                    # Sequence name
                    seq_name = str(ang_deg[loc_fig[n_plt]])+' deg '+ph.basename(c_file)[0:13]

                    # Adjust range of axes
                    mean_x = np.mean(df.x_cntr_pix)
                    x_tick = [mean_x-rng/2, mean_x+rng/2]
                    y_tick = [np.min(df.y_cntr_pix)-(rng*t_buff), 
                              np.min(df.y_cntr_pix)+rng-(rng*t_buff)]

                    # Plot data
                    axs[row_num,col_num].plot(df.x_cntr_pix,df.y_cntr_pix)
                    axs[row_num,col_num].plot(df.x_cntr_pix[0],df.y_cntr_pix[0],'o',color='blue')                    
                    
                # Empty plot, if no data
                else:
                    axs[row_num,col_num].plot([],[])
                
                axs[row_num,col_num].set_title(seq_name,fontsize=16,color='k')
                axs[row_num,col_num].set_aspect('equal')
                axs[row_num,col_num].set_xlim(x_tick)
                axs[row_num,col_num].set_ylim(y_tick)
                axs[row_num,col_num].set_xticks(x_tick)
                axs[row_num,col_num].set_yticks(y_tick)
                axs[row_num,col_num].tick_params(axis='both', which='both', right=False, left=False, top=False, bottom=False,labelbottom=False, labelleft=False)

                # Advance plot 
                seq_name = ' '
                n_plt = n_plt + 1

            if breakAll:
                break

        if not (save_path is None):
            save_file = save_path+ph.sep+'trajplot_'+str(c_fig)+'.jpg'
            fig.savefig(save_file, bbox_inches='tight')
    # fig.show()

def get_cat_value(cat_path,ex_date,ex_seq,col_name):
    """ Return the value from the catalog data for the requested experiments and column name.
    
    cat_path:   Path to video catalog file
    ex_date:    Date of experiment
    ex_seq:     Sequence number of experiment
    col_name:   Name of column in video catalog to be extracted
    """

    # Load video catalog
    cat = pd.read_csv(cat_path)

    # Define rows of catalog that have useful data
    loc_data = np.arange(np.where(pd.isna(cat.date))[0][0])

    # find location (row) of the catalog that matches the data filename
    trials = cat.trial_num[loc_data]
    dates  = cat.date[loc_data]
    i_cat_seq = (dates==ex_date) & (trials.astype('int')==int(ex_seq))
    loc_cat = np.where(i_cat_seq)[0]

    cat_value = eval('cat.'+col_name+'[loc_cat]')

    return cat_value


def plt_all_timeseries(refine_coord_path, cat_path, f_suffix='*derived.pkl.xz', save_path=None):
    """ Steps through sequences to plot all trajectories
    
    refine_coord_path:      Path to refined coordinate data
    cat_path:               Path to video catalog file
    f_suffix:               Suffix for derived data files
    save_path:              Directory path for saving files
    """

    import matplotlib.pyplot as plt 

    # Enhance resolution
    plt.rcParams['figure.dpi'] = 500
    plt.rcParams['savefig.dpi'] = 500

    # Buffer for ticks
    t_buff = 0.05

    # Number of rows per figure
    num_rows = 5

    # Load list of DLC raw data files
    if ph.isdir(refine_coord_path):
        d_files = glob.glob(refine_coord_path + ph.sep + f_suffix)
    else:
        raise ValueError('path not recognized')

    # List of figures to make
    num_figs = int(np.ceil(len(d_files)/(num_rows)))

    # plot indicies
    # fi_num = 1
    row_num = 0

    # Initialize range of values
    min_t     = np.array([],dtype=float)
    max_t     = np.array([],dtype=float)
    min_spd   = np.array([],dtype=float)
    max_spd   = np.array([],dtype=float)
    min_head  = np.array([],dtype=float)
    max_head  = np.array([],dtype=float)
    ang_deg   = np.array([],dtype=int)

    # Get the range of values among all data (for setting plot axes and ticks)
    for c_file in d_files:

        # Read dataframe
        df = pd.read_pickle(c_file)

        # Add min/max values
        min_t     = np.append(min_t,    np.min(df.time_s))
        max_t     = np.append(max_t,    np.max(df.time_s))
        min_spd   = np.append(min_spd,  np.min(df.spd_pixs))
        max_spd   = np.append(max_spd,  np.max(df.spd_pixs))
        min_head  = np.append(min_head, np.min(df.head_rad))
        max_head  = np.append(max_head, np.max(df.head_rad))

        # Sequence information to extract from catalog
        ex_date   = ph.basename(c_file)[:10]
        ex_seq    = ph.basename(c_file)[11:13]
        col_name  = 'angle_deg'

        # Extract angle for current sequence
        ang_deg = np.append(ang_deg,int(get_cat_value(cat_path, ex_date,    
                    ex_seq, col_name  = 'angle_deg')))

    # Index for order of figures, in order of angle of slopes
    loc_fig = np.argsort(ang_deg)

    # Range along x and y
    rng_head = max_head-min_head
    rng_spd  = max_spd-min_spd
    rng_x    = max_t-min_t

    # Find overall range values
    min_t     = np.min(min_t)
    max_t     = np.max(max_t)
    min_spd   = np.min(min_spd)
    max_spd   = np.max(max_spd)
    min_head  = np.min(min_head)
    max_head  = np.max(max_head)

    # Largest range
    # rng = np.max([np.max(rng_y),np.max(rng_x)])*(1+2*t_buff)

    # Index of current file, plot number
    n_plt     = 0
    breakAll  = False

    # Loop thru figures
    for c_fig in range(num_figs):

        # Create figure
        fig, axs = plt.subplots(num_rows, 1)
        fig.set_size_inches(8,24)

        # Loop thru rows
        for row_num in range(num_rows):

            # If we are within limits of current plot
            if n_plt<len(d_files)-1:
                
                # Current file
                c_file = d_files[loc_fig[n_plt]]

                # Load dataframe from current path
                df = pd.read_pickle(c_file)

                # Sequence name
                seq_name = str(ang_deg[loc_fig[n_plt]]) + ' deg ' + ph.basename(c_file)[0:13]


                # Plot data
                axs[row_num].plot(df.time_s,df.spd_pixs,color='b')
                axs[row_num].set_ylabel('Spd (pix/s)')

                head_deg = np.unwrap(df.head_rad)*180/np.pi
                ax_sub = axs[row_num].twinx()
                ax_sub.plot(df.time_s,head_deg,color='r')
                ax_sub.set_ylabel('heading')
                
                # Adjust range of axes
                x_tick  = np.linspace(min_t,max_t,5)
                y_tick1 = np.linspace(min_spd,max_spd,3)
                y_tick2 = np.linspace(np.min(head_deg),np.max(head_deg),3)

                ttt=3
                # axs[row_num,col_num].axis('equal')
                
                # axs[row_num,col_num].grid(axis='x', color='0.75')
                # axs[row_num,col_num].grid(axis='y', color='0.75')
                
            else:
                axs[row_num].plot([],[])
            
            axs[row_num].set_title(seq_name,fontsize=16,color='k')
            axs[row_num].set_xlim([np.min(x_tick), np.max(x_tick)])
            axs[row_num].set_xticks(x_tick)
            axs[row_num].set_ylim([np.min(y_tick1),np.max(y_tick1)])
            axs[row_num].set_yticks(y_tick1)
            ax_sub.set_ylim([np.min(y_tick2), np.max(y_tick2)])
            ax_sub.set_yticks(y_tick2)
            # axs[row_num].tick_params(axis='both', which='both', right=False, left=False, top=False, bottom=False,labelbottom=False, labelleft=False)

            seq_name = ' '
            n_plt = n_plt + 1

            if not (save_path is None):
                save_file = save_path+ph.sep+'timeseries_'+str(c_fig)+'.jpg'
                fig.savefig(save_file, bbox_inches='tight')

        if breakAll:
            break