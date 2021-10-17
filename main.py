from wiki import WikiSearcher

phrase = input("Zadejte hledaný výraz: ")
if phrase: 
    wiki = WikiSearcher(phrase)
    wiki.search() 
else:
    print("Vyhedávání ukončeno - pro vyhledávání je nutno zadat výraz")
