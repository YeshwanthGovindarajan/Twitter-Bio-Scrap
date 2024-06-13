import time
import pandas as pd
import random
from helium import start_chrome, write, click, go_to, scroll_down, find_all, Text, S

# Ask user for login credentials
email = input("Enter your email: ")
password = input("Enter your password: ")

# Start Chrome and log in to Twitter
browser = start_chrome("https://twitter.com/i/flow/login")
write(email, into='Phone, email, or username')
click('Next')
write(password, into='Password')  
click('Log in')
time.sleep(10)

# Navigate to the search page
search_query = "blockchain developer"
go_to(f'https://twitter.com/search?q={search_query}&src=typed_query&f=user')
time.sleep(10)

# Initialize list to store links
href = []

# Xpath for finding links
xpath = '//div[@data-testid="UserCell"]//a'

# Collect links
for i in range(200):
    scroll_down(1500)
    print(i)
    if (i % 10 == 0) and (i != 0):
        print("waiting")
        time.sleep(random.randint(5, 10) * 60)
    time.sleep(5)
    linkelements = find_all(S(xpath))
    if Text("Retry").exists():
        break
    print(linkelements)
    for linkelement in linkelements:
        link = linkelement.web_element.get_attribute('href')
        if link not in href:
            href.append(link)

# Save the links to a CSV file
df2 = pd.DataFrame({'links': href})
df2.to_csv('nlinks.csv')

print(len(href))
bios = []
c = 0

# Collect bios
for l in href:
    c += 1
    if c % 10 == 0:
        print("waiting")
        time.sleep(10)
    print(l)
    time.sleep(7)
    go_to(l)
    try:
        xp = '//div[@data-testid="UserDescription"]'
        element = S(xp)
        text = element.web_element.text.strip()
        text = text + "\n"
        bios.append(text)
    except Exception as e:
        print(f"Couldn't find the bio for {l}. Error: {str(e)} Skipping...")
        bios.append(" ")

# Clean up bios and save to another CSV file
cleanedbios = [s.replace('\n', ' ') for s in bios]
df = pd.DataFrame({'bio': cleanedbios})
df.to_csv('bios.csv')

print("Done collecting data.")
