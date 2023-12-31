
import numpy as np
import pandas as pd
import pickle

from collections import defaultdict

def pickle_load(file_path):
    with open(file_path, 'rb') as handle:
        b = pickle.load(handle)
    return b


# dict url
hpo_disease_dict_path = './pickled_dictonaries/hpo_disease_dict.pickle'

disease_hpo_dict_path = './pickled_dictonaries/disease_hpo_dict.pickle'

disease_name_dict_path = './pickled_dictonaries/disease_name_dict.pickle'

hpid_vpk_label_dict_path = './pickled_dictonaries/hpid_vpk_label_dict.pickle'

hpid_descriptions_dict_path = './pickled_dictonaries/hpid_descriptions_dict.pickle'

disease_vpk_count_dict_path =  './pickled_dictonaries/disease_vpk_count_dict.pickle'

# loading dicts
disease_hpo_dict = pickle_load(disease_hpo_dict_path)
disease_name_dict =  pickle_load(disease_name_dict_path)
hpid_descriptions_dict =  pickle_load(hpid_descriptions_dict_path)
hpid_vpk_label_dict =  pickle_load(hpid_vpk_label_dict_path)
hpo_disease_dict =  pickle_load(hpo_disease_dict_path)
disease_vpk_count_dict = pickle_load(disease_vpk_count_dict_path)

def fetch_hpids(disease_id):
  temp_hpid_name_dict = defaultdict(list)
  hpid_list = disease_hpo_dict[disease_id]
  for i in hpid_list:
    # print(i, '\t', hpid_descriptions_dict[i], '\n')
    # print(hpid_descriptions_dict[i], '\n')
    temp_hpid_name_dict[i].append(hpid_descriptions_dict[i])
  # print(temp_hpid_name_dict)
  hpid_name_df = pd.DataFrame.from_dict(temp_hpid_name_dict).T
  return hpid_name_df

#test
# type(fetch_hpids('OMIM:301040'))

def fetch_disease_name(disease_id):
  disease_name = disease_name_dict[disease_id]
  return disease_name

# test
# type(fetch_disease_name('OMIM:301040'))

def fetch_hpid_descriptions(hpid):
  hpid_description = hpid_descriptions_dict[hpid]
  return hpid_description

def fetch_hpid_vpk_label(hpid):
  hpid_vpk_label_list = hpid_vpk_label_dict[hpid]
  return hpid_vpk_label_list

# test
# type(fetch_hpid_vpk_label("HP:0004840"))

def fetch_corresp_diseases(hpid):
  disease_list = hpo_disease_dict[hpid]
  temp_disease_name_dict = defaultdict(list)
  for i in disease_list:
    temp_disease_name_dict[i].append(disease_name_dict[i])
  disease_name_df = pd.DataFrame.from_dict(temp_disease_name_dict).T
  return disease_name_df

# test
# fetch_corresp_diseases("HP:0004840")

def fetch_disease_vpk_count(disease_id):
  disease_vpk_count_list = disease_vpk_count_dict[disease_id]
  return disease_vpk_count_list

def disease_details(disease_id):
  a = disease_id
  hpid_list = fetch_hpids(a) # dict id to name mapping
  disease_name = fetch_disease_name(a)
  disease_vpk_count_list = fetch_disease_vpk_count(a)
  return hpid_list, disease_name, disease_vpk_count_list



def hpid_details(hpid):
  a = hpid
  disease_list = fetch_corresp_diseases(a) # dict disease id to name mapping
  hpid_description = fetch_hpid_descriptions(a)
  hpid_vpk_label = fetch_hpid_vpk_label(a)
  return disease_list, hpid_description, hpid_vpk_label


import streamlit as st

def main():
  # Define the dropdown options
  function_options = ["Enter Value", "Disease Info", "Phenotype Info"]


  # Set page title
  st.set_page_config(page_title="Function Dashboard")

  # Create dashboard layout
  st.title("Function Dashboard")

  # User inputs
  selected_function = st.selectbox("Select a function:", function_options)
  input_data = st.text_input("Input data:")

  # Compute outputs based on selected function
  if selected_function == "Enter Value":
        output1, output2, output3 = "Enter the correct value", "Enter the correct value", "Enter the correct value"
  elif selected_function == "Disease Info":
      output1, output2, output3 = disease_details(input_data)
  elif selected_function == "Phenotype Info":
      output1, output2, output3 = hpid_details(input_data)

  # if function == "Disease Info":
  #     output1, output2, output3 = disease_details(input_data)
  # elif function == "Phenotype Info":
  #     output1, output2, output3 = hpid_details(input_data)

  # Display outputs
  st.subheader("Output 1")
  st.write(output1)

  st.subheader("Output 2")
  st.write(output2)

  st.subheader("Output 3")
  st.write(output3)

if __name__ == '__main__':
    main()



