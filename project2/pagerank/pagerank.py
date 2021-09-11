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
    dist = dict()
    for p in corpus:
        if len(corpus[page])==0:
            dist[p]=1/len(corpus)
        elif p in corpus[page]:
            dist[p]=damping_factor/len(corpus[page])
        else:
            dist[p]=(1-damping_factor)/(len(corpus)-len(corpus[page]))
    return dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks=dict()
    for p in corpus:
        ranks[p]=0
    random.seed()
    page = random.choice(list(corpus))
    page_list=list(corpus)
    for m in range(n):
        ranks[page]+=1/n
        random.seed()
        dart = random.random()
        i=0
        dist=transition_model(corpus, page, damping_factor)
        for p in page_list:
            if i<dart:
                page=p
                i+=dist[p]
            else:
                break
    return ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks=dict()
    for p in corpus:
        ranks[p]=1/len(corpus)
    converged=0
    while not converged:
        ranks0=ranks.copy()
        converged=1
        for p in ranks:
            ranks0[p]=(1-damping_factor)/len(corpus)
            for i in ranks:
                if p in corpus[i]:
                    ranks0[p]+=damping_factor*ranks[i]/len(corpus[i])
            if ranks[p]!=ranks0[p]:
                converged=0
        ranks=ranks0.copy()
    return ranks

if __name__ == "__main__":
    main()
