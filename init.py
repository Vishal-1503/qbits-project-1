import numpy as np
import pandas as pd

df = pd.read_csv("C:/Users/visha/OneDrive/Desktop/qbits aiml/project 1/v2/support_leads.csv")
print("Data Loaded Successfully!")
print("Shape: ", df.shape)
print("Preprocessing.....", )
df['status'] = 0
df['result'] = 'Unhandled'
print("........")
df.to_csv('data.csv', index=False)
print("Data.csv created successfully!")