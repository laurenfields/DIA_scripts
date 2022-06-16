# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:16:38 2022

@author: lawashburn
"""

import csv
import pandas as pd
import os

working_directory =r"C:\Users\lawashburn\Documents\DIA\20220602_analysis\PEAKS_output"
output_dir = r"C:\Users\lawashburn\Documents\DIA\20220602_analysis\PEAKS_output\formatted"

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

for a in folder_search:
    exp_name = a
    directory_path = working_directory + '\\' + a
    file_query = 'protein-peptides'
    file_search = (get_file_names_with_strings([file_query]))
    file_path = directory_path + '\\' + file_search[0] 
    prot_pep = pd.read_csv(file_path)
    prot_pep_ppm_filter_a =  prot_pep[prot_pep['Unique'] == 'Y']
    prot_pep_ppm_filter1 =  prot_pep_ppm_filter_a[prot_pep_ppm_filter_a['ppm'] < 10]
    prot_pep_ppm_filter2 =  prot_pep_ppm_filter1[prot_pep_ppm_filter1['ppm'] > -10]
    prot_pep_ppm_filter3 = prot_pep_ppm_filter2.drop_duplicates(subset=('Protein Group','Fraction'))
    fractions_w_dups = prot_pep_ppm_filter3['Fraction'].values.tolist()
    fractions = []
    for b in fractions_w_dups:
        if b not in fractions:
            fractions.append(b)
    frac_1 = fractions[0]
    frac_2 = fractions[1]
    frac_1_filtered = prot_pep_ppm_filter3[prot_pep_ppm_filter3['Fraction'] == frac_1]
    frac_1_filtered_final = frac_1_filtered.drop_duplicates(subset=('Protein Accession'))
    frac_2_filtered = prot_pep_ppm_filter3[prot_pep_ppm_filter3['Fraction'] == frac_2]
    frac_2_filtered_final = frac_2_filtered.drop_duplicates(subset=('Protein Accession'))
    total_filtered_final = prot_pep_ppm_filter3.drop_duplicates(subset=('Protein Accession'))
    
    out_path = output_dir + '\\' + a + '_Q1.csv'
    with open(out_path,'w',newline='') as filec:
                            writerc = csv.writer(filec)
                            frac_1_filtered_final.to_csv(filec,index=False)
    
    out_path = output_dir + '\\' + a + '_Q2.csv'
    with open(out_path,'w',newline='') as filec:
                            writerc = csv.writer(filec)
                            frac_2_filtered_final.to_csv(filec,index=False)
                            
    out_path = output_dir + '\\' + a + '_total.csv'
    with open(out_path,'w',newline='') as filec:
                           writerc = csv.writer(filec)
                           total_filtered_final.to_csv(filec,index=False)                         
                           
    q1_ids = len(frac_1_filtered_final)
    q2_ids = len(frac_2_filtered_final)
    total_ids = len(total_filtered_final)
    
    name_storage.append(exp_name)
    q1_id_count.append(q1_ids)
    q2_id_count.append(q2_ids)
    total_id_count.append(total_ids)
    
total_results = pd.DataFrame()
total_results['Exp Name'] = name_storage
total_results['# Q1 IDs'] = q1_id_count
total_results['# Q2 IDs'] = q2_id_count
total_results['# Total IDs'] = total_id_count

out_path = output_dir + '\\all_IDs.csv'
with open(out_path,'w',newline='') as filec:
                       writerc = csv.writer(filec)
                       total_results.to_csv(filec,index=False)    