# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 19:27:11 2022

@author: lawashburn
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:55:55 2022

@author: lawashburn
"""

import csv
import pandas as pd
import os

working_directory =r"H:\DDA_files"
output_dir = r"H:\DDA_results"

def get_folder_names_with_strings(str_list):
    full_list = os.listdir(working_directory)
    final_list = [nm for ps in str_list for nm in full_list if ps in nm]
    return final_list

def get_file_names_with_strings(str_list):
    full_list = os.listdir(directory_path)
    final_list = [nm for ps in str_list for nm in full_list if ps in nm]
    return final_list

file_type2 = 'Exp'
file_query2 = file_type2 #search query
folder_search = (get_folder_names_with_strings([file_query2]))
name_storage = []
q1_id_count = []
q2_id_count = []
total_id_count = []
for w in folder_search:
    print(w)
    exp_name = w
    directory_path = working_directory + '\\' + w
    file_query = 'protein-peptides.csv'
    file_search = (get_file_names_with_strings([file_query]))
    #file_path = r"C:\Users\lawashburn\Documents\DIA\20220711_dsdopti_PeaksXExports\Reformatted\DIA\exp_20220711_cNP_DSD21_1\protein-peptides.csv"
    file_path = directory_path + '\\' + file_search[0] 
    prot_pept = pd.read_csv(file_path)
    prot_pept2 =  prot_pept[prot_pept['ppm'] < 10]
    prot_pept3 =  prot_pept2[prot_pept2['ppm'] > -10]
    prot_pept4 =  prot_pept3[prot_pept3['Unique'] != 'N']
    index_append = []
    for bb in range(1,len(prot_pept4)+1):
        index_append.append(bb)

    prot_pept4['Artificial index']=index_append
    prot_pept4['PTM']=prot_pept4['PTM'].str.replace(';',',')

    ptm_list = prot_pept4['PTM'].values.tolist()
    formatted_PTMs = []
    for a in ptm_list:
        a = str(a)
        num_entries = a.count(',')
        if  num_entries == 0:
            formatted_PTMs.append(a)
        if num_entries > 0:
            chunks = a.split(',')
            formatted_PTMs.append(chunks)
    prot_pept4['PTMs formatted'] = formatted_PTMs
    prot_pept4['AScore']=prot_pept4['AScore'].str.replace(';',',')
    ascore_list = prot_pept4['AScore'].values.tolist()
    formatted_AScore = []
    for a in ascore_list:
        a = str(a)
        num_entries = a.count(',')
        if  num_entries == 0:
            formatted_AScore.append(a)
        if num_entries > 0:
            chunks = a.split(',')
            formatted_AScore.append(chunks)
    prot_pept4['AScore formatted'] = formatted_AScore

    prot_pept4 = prot_pept4.explode(['PTMs formatted','AScore formatted'])

    #prot_pept4['PTMs formatted']=prot_pept4['PTMs formatted'].replace({'Oxidation (M)':'nan',' Oxidation (M)':'nan'})
    ascore_filtered  = []
    ptms_report = prot_pept4['PTMs formatted'].values.tolist()
    score_report = prot_pept4['AScore formatted'].values.tolist()

    for c in range(0,len(prot_pept4)):
        if ptms_report[c] == 'nan':
            ascore_filtered.append('nan')
        else:
            ascore_filtered.append(score_report[c])
    
    prot_pept4['AScore formatted'] = ascore_filtered
    prot_pept4['AScore formatted'] = prot_pept4['AScore formatted'].str[:-8]
    prot_pept4['AScore formatted'] = prot_pept4['AScore formatted'].str.extract('(\d+)', expand=False)
    prot_pept4['Absolute Mod Location'] = 'nan'
    no_ptm_table = prot_pept4[prot_pept4['PTMs formatted'] == 'nan']
    no_ptm_table = no_ptm_table.drop_duplicates(subset=['Protein Group'])

    ptm_table = prot_pept4[prot_pept4['PTMs formatted'] != 'nan']
    ptm_table['Absolute Mod Location'] = ptm_table['AScore formatted'].astype(int) + ptm_table['Start'].astype(int)
    ptm_table = ptm_table.drop_duplicates(subset=['Protein Group','Absolute Mod Location','PTMs formatted','Fraction'])

    implode_index = ptm_table['Artificial index'].values.tolist()
    implode_index_no_dups = []
    for l in implode_index:
        if l not in implode_index_no_dups:
            implode_index_no_dups.append(l)

    grouped_ptm_df = pd.DataFrame()

    for k in implode_index_no_dups:
        ptm_table_single = ptm_table[ptm_table['Artificial index'] == k]
        if len(ptm_table_single)>1:
            ptm_single = ptm_table_single['PTMs formatted'].values.tolist()
            ptm_string = ','.join(ptm_single)
            loc_single = ptm_table_single['Absolute Mod Location'].values.tolist()
            loc_string = ','.join(map(str, loc_single))
            ptm_table_single['PTMs formatted'] = ptm_string
            ptm_table_single['Absolute Mod Location'] = loc_string
            
            grouped_ptm_df = grouped_ptm_df.append(ptm_table_single)
        else:
            grouped_ptm_df = grouped_ptm_df.append(ptm_table_single)
   
    final_results = grouped_ptm_df.append(no_ptm_table)
    final_results = final_results.drop_duplicates(subset=['Protein Group','Absolute Mod Location','PTMs formatted','Fraction'])
    implode_index2 = final_results['Artificial index'].values.tolist()
    implode_index2_no_dups = []
    for j in implode_index2:
        if j not in implode_index2_no_dups:
            implode_index2_no_dups.append(j)

    grouped_final_results = pd.DataFrame()
    for m in implode_index2_no_dups:
        results_table_single = final_results[final_results['Artificial index'] == m]
        if len(results_table_single)>1:
            results_table_single = results_table_single[results_table_single['PTMs formatted'] != 'nan']
            grouped_final_results = grouped_final_results.append(results_table_single)
        else:
            grouped_final_results = grouped_final_results.append(results_table_single)


    total_filtered_final = grouped_final_results.drop_duplicates(subset=('Protein Group','Absolute Mod Location','PTMs formatted'))

    out_path = output_dir + '\\' + w + '_total.csv'
    with open(out_path,'w',newline='') as filec:
                           writerc = csv.writer(filec)
                           total_filtered_final.to_csv(filec,index=False)                         

    total_ids = len(total_filtered_final)
    
    name_storage.append(exp_name)

    total_id_count.append(total_ids)
    
total_results = pd.DataFrame()
total_results['Exp Name'] = name_storage

total_results['# Total IDs'] = total_id_count

out_path = output_dir + '\\DDA_IDs.csv'
with open(out_path,'w',newline='') as filec:
                       writerc = csv.writer(filec)
                       total_results.to_csv(filec,index=False)    