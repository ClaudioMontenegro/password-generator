import pandas as pd

sites = []
emails = []
passwords = []
date = []

my_pass = pd.DataFrame({
        "sites": sites,
        "emails": emails,
        "passwords": passwords,
        "date": date
    })

# Save as .csv file
my_pass.to_csv("my-passwords/my_passwords.csv", sep=',', index=False)

print(my_pass)
