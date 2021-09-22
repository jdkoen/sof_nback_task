"""
This script makes the stimulus lists for the crit task.
"""

# Import libraries
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Handle directories
os.chdir(os.path.split(__file__)[0])
stim_dir = Path('')
stim_dir.mkdir(exist_ok=True, parents=True)

# Number of lists to make
n_lists = 200

# Number of blocks per lists
n_blocks = 3
n_repeat_per_cat_block = 6

# Make the stimulus lists
for i in np.arange(n_lists):

    # Print info
    print(f'stim list {i+1:03} creation')
    # Load the the stimulus files
    faces_f = pd.read_csv(stim_dir / 'crit_faces_female.csv').sample(frac=1)
    faces_m = pd.read_csv(stim_dir / 'crit_faces_male.csv').sample(frac=1)
    objects_m = pd.read_csv(stim_dir / 'crit_objects_man.csv').sample(frac=1)
    objects_n = pd.read_csv(stim_dir / 'crit_objects_nat.csv').sample(frac=1)
    scenes_m = pd.read_csv(stim_dir / 'crit_scenes_man.csv').sample(frac=1)
    scenes_n = pd.read_csv(stim_dir / 'crit_scenes_nat.csv').sample(frac=1)

    # Make 1-back and 2-back data frames (split each in half)
    faces_m_1b, faces_m_2b = np.array_split(faces_m, 2)
    faces_f_1b, faces_f_2b = np.array_split(faces_f, 2)
    objects_m_1b, objects_m_2b = np.array_split(objects_m, 2)
    objects_n_1b, objects_n_2b = np.array_split(objects_n, 2)
    scenes_m_1b, scenes_m_2b = np.array_split(scenes_m, 2)
    scenes_n_1b, scenes_n_2b = np.array_split(scenes_n, 2)

    # 1-BACK TASK STIMULI
    # Make list of lists
    faces_m_1b_list = np.array_split(faces_m_1b, n_blocks)
    faces_f_1b_list = np.array_split(faces_f_1b, n_blocks)
    objects_m_1b_list = np.array_split(objects_m_1b, n_blocks)
    objects_n_1b_list = np.array_split(objects_n_1b, n_blocks)
    scenes_m_1b_list = np.array_split(scenes_m_1b, n_blocks)
    scenes_n_1b_list = np.array_split(scenes_n_1b, n_blocks)

    # Make 1-back critical list
    back1_blocks_list = []
    for bi in np.arange(n_blocks):

        # Get temporary lists
        tmp_faces_f = faces_f_1b_list[bi].reset_index(drop=True)
        tmp_faces_m = faces_m_1b_list[bi].reset_index(drop=True)
        tmp_objects_m = objects_m_1b_list[bi].reset_index(drop=True)
        tmp_objects_n = objects_n_1b_list[bi].reset_index(drop=True)
        tmp_scenes_m = scenes_m_1b_list[bi].reset_index(drop=True)
        tmp_scenes_n = scenes_n_1b_list[bi].reset_index(drop=True)

        # Add repeat column and randomly assign repeat trials
        tmp_faces_f['repeat'] = 0
        tmp_faces_f.at[tmp_faces_f.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_faces_m['repeat'] = 0
        tmp_faces_m.at[tmp_faces_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_objects_m['repeat'] = 0
        tmp_objects_m.at[tmp_objects_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_objects_n['repeat'] = 0
        tmp_objects_n.at[tmp_objects_n.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_scenes_m['repeat'] = 0
        tmp_scenes_m.at[tmp_scenes_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_scenes_n['repeat'] = 0
        tmp_scenes_n.at[tmp_scenes_n.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1

        # Combine the stimulus list
        tmp_stim_list = [tmp_faces_f, tmp_faces_m, tmp_objects_m, tmp_objects_n,
                         tmp_scenes_m, tmp_scenes_n]
        tmp_block = pd.concat(tmp_stim_list).sample(frac=1)
        tmp_block['task'] = '1back'
        tmp_block['block'] = i + 1
        tmp_block['presentation'] = 1

        # Make a pandas dataframe with no rows
        out_list = pd.DataFrame(columns=tmp_block.columns)

        # Loop through the rows to build out_list
        for ri, row in tmp_block.iterrows():

            # Append current row to
            out_list = out_list.append(row)

            # Determine if repeat is needed
            if row['repeat'] == 1:
                row['presentation'] = 2
                out_list = out_list.append(row)
        out_list.reset_index(drop=True, inplace=True)
        back1_blocks_list.append(out_list)

    # Make and save the stim list
    back1_file = stim_dir / f'set-{i+1:03}_task-1back.csv'
    pd.concat(back1_blocks_list).to_csv(back1_file, index=False)

    # 2-BACK TASK STIMULI
    # Make list of lists
    faces_m_2b_list = np.array_split(faces_m_2b, n_blocks)
    faces_f_2b_list = np.array_split(faces_f_2b, n_blocks)
    objects_m_2b_list = np.array_split(objects_m_2b, n_blocks)
    objects_n_2b_list = np.array_split(objects_n_2b, n_blocks)
    scenes_m_2b_list = np.array_split(scenes_m_2b, n_blocks)
    scenes_n_2b_list = np.array_split(scenes_n_2b, n_blocks)

    # Make 2-back critical list
    back2_blocks_list = []
    for bi in np.arange(n_blocks):

        # Get temporary lists
        tmp_faces_f = faces_f_2b_list[bi].reset_index(drop=True)
        tmp_faces_m = faces_m_2b_list[bi].reset_index(drop=True)
        tmp_objects_m = objects_m_2b_list[bi].reset_index(drop=True)
        tmp_objects_n = objects_n_2b_list[bi].reset_index(drop=True)
        tmp_scenes_m = scenes_m_2b_list[bi].reset_index(drop=True)
        tmp_scenes_n = scenes_n_2b_list[bi].reset_index(drop=True)

        # Add repeat column and randomly assign repeat trials
        tmp_faces_f['repeat'] = 0
        tmp_faces_f.at[tmp_faces_f.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_faces_m['repeat'] = 0
        tmp_faces_m.at[tmp_faces_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_objects_m['repeat'] = 0
        tmp_objects_m.at[tmp_objects_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_objects_n['repeat'] = 0
        tmp_objects_n.at[tmp_objects_n.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_scenes_m['repeat'] = 0
        tmp_scenes_m.at[tmp_scenes_m.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1
        tmp_scenes_n['repeat'] = 0
        tmp_scenes_n.at[tmp_scenes_n.sample(n=n_repeat_per_cat_block).index, 'repeat'] = 1

        # Combine the stimulus list
        tmp_stim_list = [tmp_faces_f, tmp_faces_m, tmp_objects_m, tmp_objects_n,
                         tmp_scenes_m, tmp_scenes_n]
        while True:
            tmp_block = pd.concat(tmp_stim_list).sample(frac=1)
            if tmp_block.iloc[-1]['repeat'] != 1:
                break
        tmp_block['task'] = '2back'
        tmp_block['block'] = i + 1
        tmp_block['presentation'] = 1

        # Make a pandas dataframe with no rows
        out_list = pd.DataFrame(columns=tmp_block.columns)

        # This works only in a while loop
        ri = 0 
        while True:

            # Break while loop if needed
            if ri == tmp_block.shape[0]:
                break

            # Get the current row
            row = tmp_block.iloc[ri]

            # Append current row to
            out_list = out_list.append(row)
            ri += 1

            # Determine if repeat is needed
            if row['repeat'] == 1:
                row.at['presentation'] = 2
                next_row = tmp_block.iloc[ri]
                out_list = out_list.append(next_row)
                out_list = out_list.append(row)
                ri += 1
                if next_row['repeat'] == 1:
                    next_row.at['presentation'] = 2
                    out_list = out_list.append(next_row)
        out_list.reset_index(drop=True, inplace=True)
        back2_blocks_list.append(out_list)

    # Make and save the stim list
    back2_file = stim_dir / f'set-{i+1:03}_task-2back.csv'
    pd.concat(back2_blocks_list).to_csv(back2_file, index=False)
