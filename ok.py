import pandas as pd 
from ydata_profiling import ProfileReport


df = pd.read_excel(r"C:\Users\Dell\OneDrive\Desktop\advance web scraping\Nakri_data_set\Skill_Gap_Analysis_Tool\notebooks\result.xlsx")


profile = ProfileReport(df)

profile.to_file(output_file="Eda_Report.html")