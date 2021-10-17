from wiki import WikiSearcher

phrase = input("Zadejte hledaný výraz: ")
if phrase: 
    wiki = WikiSearcher(phrase)
    wiki.search() 
else:
    print("Vyhledávání ukončeno - pro vyhledávání je nutno zadat výraz")
