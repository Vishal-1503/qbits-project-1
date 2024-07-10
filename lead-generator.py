import numpy as np
import pandas as pd

np.random.seed(24)

phoneNumbers = [ ''.join(np.random.choice(list('0123456789'), 10)) for _ in range(50)]

alphabets = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
names = [ ''.join(np.random.choice(alphabets, 10)) for _ in range(50)]

df = pd.DataFrame({
    "Names": names,
    "Phone Numbers": phoneNumbers
})

df.to_csv('support_leads.csv', index=False)