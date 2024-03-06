from Bio import Entrez
import os
from openai import OpenAI
client = OpenAI()

def get_rating(input,hypothesis):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a biochemist, researching how to " + hypothesis + "You will rate this abstract on how relevant it is to the goal of using this phage in phage therapy on multidrug resistant bacteria.  Please also give it a number rating between 0 and 10 based on it's relevance in the form of Rating x/10."},
            {"role": "user", "content": input}
        ]
    )
    return completion.choices[0].message.content



Entrez.email = os.environ['EMAIL']

def search_pubmed(search_term):
    handle = Entrez.esearch(db="pubmed", term=search_term, retmax=10000)
    result = Entrez.read(handle)
    handle.close()
    
    id_list = result['IdList']
    return id_list

def fetch_abstracts(id_list):
    ids = ','.join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    articles = Entrez.read(handle)
    handle.close()
    
    for article in articles['PubmedArticle']:
        try:
            title = article['MedlineCitation']['Article']['ArticleTitle']
            abstract = article['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            print(f"Title: {title}\nAbstract: {abstract}\n")
        except:
            print("Abstract not found.\n")

        rating = get_rating(abstract,hypothesis)
        print(f"Rating: {rating}")
        print("------------------------------", flush=True)
    
if __name__ == "__main__":
#    print("Enter the phage that you want to study")
#    search_term = input() + "AND phage"
#    print("Enter what you want to do with this phage")
#    hypothesis = input()
    search_term = "ms2 AND phage"
    hypothesis = "Modify the MS2 phage lysis protein in order that it does not need to bind DNAJ."    
    id_list = search_pubmed(search_term)
    fetch_abstracts(id_list)
