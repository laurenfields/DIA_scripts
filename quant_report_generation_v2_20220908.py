# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 09:28:22 2022

@author: lawashburn
"""

import csv
import pandas as pd
import os
import numpy as np

quant_results_dir = r"D:\DIA\20220824\Quant_Results\LogP30"
exp_prefix = 'Exp_'
search_query = '_total.csv'
non_dilute_name = 'Opt'

def get_file_names_with_strings(str_list):
    full_list = os.listdir(quant_results_dir)
    final_list = [nm for ps in str_list for nm in full_list if ps in nm]
    return final_list

file_search = (get_file_names_with_strings([search_query]))

merged_areas = pd.DataFrame()
sample_types = []

exp_name_storage = []
pre_filter_IDs = []
post_filter_IDs = []

for a in file_search:
    
    unique_ID_storage = []
    area_column_storage = []
    file_source_storage = []
    
    file_path = quant_results_dir + '\\' + a
    peaks_out = pd.read_csv(file_path)
    peaks_out['Unique ID'] = ((peaks_out['Protein Group'].astype(str)) + '_' + 
                                  (peaks_out['Peptide'].astype(str)))
    pre_filter_IDs.append(len(peaks_out))
    peaks_out['ID count'] = peaks_out.groupby('Unique ID')['Unique ID'].transform('count')
    peaks_out =  peaks_out[peaks_out['ID count'] == 1]
    post_filter_IDs.append(len(peaks_out))
    area_cols = [col for col in peaks_out.columns if 'Area' in col]
    area_column = area_cols[0]
    
    area_values = peaks_out[area_column].values.tolist()
    unique_IDs = peaks_out['Unique ID'].values.tolist()
    
    for b in unique_IDs:
        index = unique_IDs.index(b)
        
        unique_ID_storage.append(b)
        area_column_storage.append(area_values[index])
        file_source_storage.append(a)

    exp_name = a.replace('Exp_','')
    exp_name = exp_name.replace('_total.csv','')
    exp_name_storage.append(exp_name)
    sample_name = exp_name[:-3]
    sample_types.append(sample_name)
    area_storage_table = pd.DataFrame()
    area_storage_table['Unique ID'] = unique_ID_storage
    area_storage_table['Area' + exp_name] = area_column_storage
    area_storage_table.drop_duplicates()
    area_storage_table_filtered =  area_storage_table[area_storage_table['Area' + exp_name] != 0.0]
    
    if len(merged_areas) == 0:
        merged_areas = merged_areas.append(area_storage_table_filtered)
    else:
        merged_areas = merged_areas.merge(area_storage_table_filtered, on='Unique ID',how='outer')

out_path = quant_results_dir + '\\area_report.csv'
with open(out_path,'w',newline='') as filec:
                       writerc = csv.writer(filec)
                       merged_areas.to_csv(filec,index=False) 

sample_types_no_dups = []
for b in sample_types:
    if b not in sample_types_no_dups:
        sample_types_no_dups.append(b)

ctrl_column = non_dilute_name + ' average area'

for c in sample_types_no_dups:
    rep_1_name = 'Area' + c + '_01'
    rep_2_name = 'Area' + c + '_02'
    rep_3_name = 'Area' + c + '_03'
    
    temp_df = pd.DataFrame()
    temp_df['Unique ID'] = merged_areas['Unique ID']
    temp_df[rep_1_name] = merged_areas[rep_1_name]
    temp_df[rep_2_name] = merged_areas[rep_2_name]
    temp_df[rep_3_name] = merged_areas[rep_3_name]
    
    temp_df[c + ' average area'] = temp_df[[rep_1_name,rep_2_name,rep_3_name]].mean(axis=1)
    merged_areas = merged_areas.merge(temp_df, on=['Unique ID',rep_1_name,rep_2_name,rep_3_name],how='outer')

    if ctrl_column in merged_areas.columns:
        merged_areas['Opti:'+ 'Ratio ' + c + 'value'] =  merged_areas[ctrl_column] / merged_areas[c + ' average area']
        merged_areas['Log2(Opti:'+ 'Ratio ' + c + ')'] = np.log2(merged_areas['Opti:'+ 'Ratio ' + c + 'value'])
    else:
        pass

column_order = ['Unique ID']

normal_area = [col for col in merged_areas.columns if 'Area' in col]
for e in normal_area:
    column_order.append(e)

average_area = [col for col in merged_areas.columns if 'average area' in col]
for f in average_area:
    column_order.append(f)
    
ratio_value = [col for col in merged_areas.columns if 'value' in col]
for g in ratio_value:
    column_order.append(g)

log2_ratio = [col for col in merged_areas.columns if 'Log2' in col]
for h in log2_ratio:
    column_order.append(h)

merged_areas = merged_areas[column_order]
print(merged_areas)

out_path = quant_results_dir + '\\quant_report.csv'
with open(out_path,'w',newline='') as filec:
                       writerc = csv.writer(filec)
                       merged_areas.to_csv(filec,index=False) 

quant_counts = pd.DataFrame()
quant_counts['Experiment'] = exp_name_storage
quant_counts['Total IDs'] = pre_filter_IDs
quant_counts['Total Quantifiable IDs'] = post_filter_IDs

out_path = quant_results_dir + '\\quant_counts_report.csv'
with open(out_path,'w',newline='') as filec:
                       writerc = csv.writer(filec)
                       quant_counts.to_csv(filec,index=False) 