from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
from tranco import Tranco
from termcolor import colored

t=Tranco()
websites=t.list().top(1000)

chrome_options = ChromeOptions()
# chrome_options.add_extension('0.7.7_0.crx')
chrome_options.add_extension('./fpmon-fingerprinting-monitor-5f0748f/FPMON_extension.crx')
d = DesiredCapabilities.CHROME

d['goog:loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options, desired_capabilities=d)
driver.minimize_window()

results=[]
i = 0
for id, url in enumerate(websites):
    i = i+1
    try:
        driver.get("https://"+url)

        time.sleep(5)
        logs=driver.get_log('browser')
            # print(i)
        req=logs[-1]['message']
        id=req.find('url')
        final=eval(req.replace('\\','').replace('false','False')[id-3:-1])

        res={
            'url': final['url'],
            'date': final['date'],
            'JS Attributes Tracked': final['coverage_entities'].split()[-1].split('/')[0][1:],
            'Fingerprinting Features': final['coverage_categories'].split()[-1].split('/')[0][1:],
            'Aggressive Features': final['aggressive_coverage'].split()[-1].split('/')[0][1:],
            'Aggresive Categories': final['aggressive_categories'].split()[-1].split('/')[0][1:],
            'Sensitive': final['fingerprint_categories'],
            'loadtime': final['loadtime']
        }

        results.append(res)
        print(i, colored(url, 'green'))
        
    except Exception as e:
        print(i, colored(url, 'red'))
    
    if(id%10==0):
        df=pd.DataFrame(results)
        df.to_csv('res.csv', index=False)

df=pd.DataFrame(results)
df.to_csv('res.csv', index=False)

driver.quit()
