from scholarly import scholarly


def rnvc():

    keywords = 'virtual team awareness'
    print('Looking for >> {} << ..'.format(keywords))
    search_query = scholarly.search_pubs(keywords)
    cnt = 0

    while cnt < 2:
        cnt += 1
        pub = next(search_query).bib
        print('"{}" cited by ({})'.format(pub['title'], pub['cites']))









if __name__ == "__main__":
    rnvc()

