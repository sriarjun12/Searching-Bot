from fuzzywuzzy import fuzz
import bs4, requests
import numpy as np
import pandas as pd
FinalResult=[]
def SearchResults():
    f = open("Input", "r")
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
    StabUrl = "https://www.google.com/search?hl=en&q="
    midUrl = "&oq="
    EndUrl = "&gs_lcp=CgZwc3ktYWIQAzoECAAQR1C11AxYtdQMYJXcDGgAcAF4AIABpQKIAaUCkgEDMi0xmAEAoAECoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwiY5YDjnu7rAhU6yjgGHf7QA_AQ4dUDCA0&uact=5"
    for i in f:
        singleLink=[]
        singleRatio=[]
        singleWrite=[]
        linkList=[]
        contentList=[]
        singleWrite.append(i.strip("\n"))
        checkString=i.replace("+","")
        searchString=i.replace("+","%2B")
        searchString=searchString.replace(" ","+")
        searchString=StabUrl+searchString
        r = requests.get(searchString, headers=headers)
        soup = bs4.BeautifulSoup(r.text, features="html.parser")
        elementLink = soup.select(".g a")
        elements = soup.select(".st")
        for k in elementLink:
            k = k.get("href")
            if k.startswith('#') or \
                    k.startswith('https://webcache.googleusercontent.com') or \
                    k.startswith('/search?') or \
                    k.startswith('/url') or \
                    k.startswith('http://webcache.googleusercontent.com'):
                continue
            lin = str(k)
            linkList.append(lin)
        for j in elements:
            contentList.append(str(j.text))
        for link, content in zip(linkList, contentList):
            ratio = fuzz.token_set_ratio(checkString, content)
            if (ratio > 40):
                singleLink.append(link)
                singleRatio.append(ratio)
        if (len(singleLink) >= 4):
            singleLink = np.array(singleLink)
            singleRatio = np.array(singleRatio)
            inds = singleRatio.argsort()
            sortedLink = singleLink[inds]
            sortedFinalList = list(sortedLink[::-1])
            sortedFinalList = sortedFinalList[:4]
            FinalResult.append(singleWrite + sortedFinalList)
        if (len(singleLink) < 4) and (len(singleLink) > 0):
            singleLink = np.array(singleLink)
            singleRatio = np.array(singleRatio)
            inds = singleRatio.argsort()
            sortedLink = singleLink[inds]
            sortedFinalList = list(sortedLink[::-1])
            sortedFinalList = sortedFinalList + (4 - len(sortedFinalList)) * [[" "]]
            FinalResult.append(singleWrite + sortedFinalList)
        if(len(singleLink)==0):
            sortedFinalList = [[" "]] * 4
            FinalResult.append(singleWrite + sortedFinalList)
SearchResults()
FinalResult=np.array(FinalResult,dtype=object)
df=pd.DataFrame(FinalResult)
df.columns=["Input","Link A","Link B","Link C","Link D"]
df=df.replace(" ",np.nan)
df.to_csv("Output.csv",index=False)
print("Completed !")