from django.test import TestCase

# # Create your tests here.
# from datetime import datetime 
# from openpyxl import load_workbook
# import json

# # Load the workbook
# workbook = load_workbook('allusers.xlsx')

# # Select a worksheet
# sheet = workbook['LIST']  # Specify the sheet name

# # Extract data from the sheet
# data = []
# headers = [cell.value for cell in sheet[1]]  # Assuming the first row contains headers
# i = 0
# for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row
#     if row[0] is None:  # Skip empty rows
#         continue
#     # Create a dictionary for each row
#     row_data = {headers[i]: str(row[i]) for i in range(len(headers))}
#     data.append(row_data)
#     qn = 'QA111220001EM0'+str(1+i) if (i+1)<10 else 'QA111220001EM'+str(1+i)
#     with open('NEWQns/'+qn+'.json', 'w') as json_file:
#         row_data = [row_data]
#         json_file.write(json.dumps(row_data, indent=4))
#     i= i+1