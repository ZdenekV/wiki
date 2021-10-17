import wikipedia
import inquirer
import textwrap
from termcolor import colored

wikipedia.set_lang("cz")

class WikiSearcher:
    """ 
    A class used to search for the meaning of a phrase on wikipedia
    
    Attributes
    -------------------------------
    phrase: str
        searched phrase
    
    __found_articles: list
        contains the last relevant or not relevant article titles
        relative to the last search phrase
    
    already_searched: dictionary
        contains 1: list of already searched articles in form:
                    name of searched phrase: relevant or not relevant articles [list]
        contains 2: boolean value in form:
                    phrasename_relevant: true or false ("info about saved articles(1), 
                                         are relevant or not relevant to the searched phrase")
    __article_titles_relevance: Boolean
        contains information about the relevance of most recently found articles
    
    already_searched: dictionary
          name of article: summary of article

    __search_end: Boolean
        decides when the search ends

    Methods         
    -------------------------------
    search()
        searches for articles based on the phrase attribute

    __check_phrase()
        checks whether articles for the given phrase have already been searched for
        return true or false

    __save_searched_articles(articles, relevant)       
        stores the titles and relevance of articles

    __filter_articles()
        separates relevant and not relevant article search results

    __chose_article(articles)      
        provides the possibility to select a specific article

    __getSummary(article)
        gets a summary of the article 

    __check_summary(self, article):
        checks whether summary for the given article have already been searched for
        return false or article_content

    __save_summary(self, article, content):                
        stores summary of article

    highlight_phrase(txt, phrase)
        used to highlight one-word search phrase in non-relevant article
        return text with highlited word

    __print_first_paragraph(summary)
        prints only the first paragraph of the summary to the screen

    __repeat_or_end(searched)
        provides the possibility to select another program operation (list of last 
                                                  articles, new search, end search)
        or (new search, end search) if not found any articles when last search    
    """

    def __init__(self, phrase):
        self.phrase = phrase.lower()
        self.already_searched = {}
        self.summary = {}
        self.__found_articles = []
        self.__article_titles_relevance = None
        self.__search_end = False
        

    def search(self):
        # before search pharse on wiki check if the phrase is not saved
        phrase_already_searched = self.__check_pharse()
        if not phrase_already_searched:
            self.__found_articles = wikipedia.search(self.phrase)

        if self.__found_articles and not self.__search_end: self.__filter_articles()
        if not self.__found_articles and not self.__search_end: 
            print("Litujeme hledaný výraz nebyl nalezen")    
            self.__repeat_or_end(False)

    def __check_pharse(self):
        articles = self.already_searched.get(self.phrase)

        if articles:
            # get relevance of articles and set to the current relevance 
            self.__article_titles_relevance = self.already_searched.get("{p}_relevant".format(p=self.phrase)) 
            self.__found_articles = articles # sets saved articles as currently found articles
            self.__chose_article(articles)
            return True
        else: return False      

    
    def __save_searched_articles(self, articles, relevant):
        if relevant: 
            self.already_searched[self.phrase] = articles
            # info about saved articles (articles are relevant)
            self.already_searched["{p}_relevant".format(p=self.phrase)] = True  
        else: 
            self.already_searched[self.phrase] = articles
            # info about saved articles (articles are not relevant)
            self.already_searched["{p}_relevant".format(p=self.phrase)] = False
            

    def __filter_articles(self):
        relevant_article_names = [x for x in self.__found_articles if self.phrase in x.lower()] 
        not_relevant_article_names = [x for x in self.__found_articles if self.phrase not in x.lower()]
        if relevant_article_names:
            self.__article_titles_relevance = True # if phrase in article name
            self.__save_searched_articles(relevant_article_names, True)
            self.__found_articles = relevant_article_names # sets articles as currently found articles
            self.__chose_article(relevant_article_names)
        else:
            self.__article_titles_relevance = False # if phrase in article name
            self.__save_searched_articles(not_relevant_article_names, False)
            self.__found_articles = not_relevant_article_names # sets articles as currently found articles
            self.__chose_article(not_relevant_article_names)


    def __chose_article(self, articles):
        if self.__article_titles_relevance: message_text = "Nalezené články - zvolte článek"
        else: message_text = "Článek s názvem {p} nebyl nalezen, ale hledaná fráze je součást těchto článků - zvolte článek".format(p=self.phrase)

        questions = [
        inquirer.List('article',
                message=message_text,
                choices=articles,
            ),
        ]

        selected_article = inquirer.prompt(questions)
        selected_article = selected_article["article"]
        self.__getSummary(selected_article)


    def __getSummary(self, article):
        # before load content data from wiki check if the data is not already saved
        article_content = self.__check_summary(article) 
        if not article_content:
            article_content = wikipedia.summary(article)
            self.__save_summary(article, article_content)

        self.__print_first_paragraph(article_content)


    def __check_summary(self, article):
        article_content = self.summary.get(article)

        if article_content: return article_content
        else: return False      


    def __save_summary(self, article, content):
        self.summary[article] = content

    def highlight_phrase(self, txt, phrase):
        highlighted_text = []
        for t in txt.split(): 
            if phrase in t: 
                highlighted_text.append(colored(t,'magenta', attrs=['bold']))
            else: 
                highlighted_text.append(t)
        highlighted_text = (" ".join(highlighted_text))
        return highlighted_text
        

    def __print_first_paragraph(self, summary):
        paragraphs = summary.split('\n')
        first_paragraph = str(paragraphs[0])
        if not self.__article_titles_relevance:
            first_paragraph = self.highlight_phrase(first_paragraph, self.phrase)

        print(textwrap.fill(first_paragraph, 90))
        self.__repeat_or_end(True)

     # searched (if found any articles when last search)
    def __repeat_or_end(self, searched):
        print("\n")
        if searched: choices = ["Vyhledávání nové fráze", "Vrátit se k výběru článků", "Ukončit vyhledávání"]
        else: choices = ["Vyhledávání nové fráze", "Ukončit vyhledávání"]

        questions = [
        inquirer.List('choice',
                message="Vyberte další operaci",
                choices=choices,
            ),
        ]
        selected_choice = inquirer.prompt(questions)
        selected_choice = selected_choice["choice"]
    
        if selected_choice == "Vyhledávání nové fráze":
            self.phrase = input("Zadejte hledaný výraz: ").lower()
            self.search()
        if selected_choice == "Vrátit se k výběru článků": self.__chose_article(self.__found_articles)
        if selected_choice == "Ukončit vyhledávání": self.__search_end = True