import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    TotalPage = len(corpus)
    TotalLink = len(corpus[page])
    new_dict = {}
    for key in corpus:
        if key in corpus[page]:
            new_dict[key] = damping_factor*(1/TotalLink) + (1-damping_factor)*(1/TotalPage)
        else:
            new_dict[key] = (1-damping_factor)*(1/TotalPage)
    return new_dict



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visit = { i : 0 for i in corpus}

    value = random.choice(list(corpus))
    visit[value] += 1

    for i in range(n-1):
        dict = transition_model(corpus,value,damping_factor)

        val = random.random()
        sum = 0
        for key,prob in dict.items():
            sum+=prob
            if val < sum:
                next = key
                break
        visit[next]+=1
        value = next

    PageRank = {page : visit[page]/n for page in corpus}
    return PageRank






def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = {page : 1/len(corpus) for page in corpus}
    UpdatedRank = {}
    estimate = 0.001
    random_prob = (1-damping_factor)/len(corpus)
    maxchange=1
    while maxchange > 0.001:
        maxchange = 0
        for page in corpus:
            sum_prob = 0
            for new_page in corpus:
                if len(corpus[new_page])==0:
                    sum_prob += PageRank[new_page]*(1/len(corpus))
                elif page in corpus[new_page]:
                    sum_prob += PageRank[new_page]*(1/len(corpus[new_page]))
            UpdatedRank[page] = random_prob + damping_factor*sum_prob
        
        sum_rank = sum(UpdatedRank.values())
        UpdatedRank = {Page: (rank)/sum_rank for Page, rank in UpdatedRank.items()}

        for page in corpus:
            change = abs(UpdatedRank[page] - PageRank[page])
            if change > maxchange:
                maxchange = change
        
        PageRank = UpdatedRank.copy()
    return PageRank

if __name__ == "__main__":
    main()
