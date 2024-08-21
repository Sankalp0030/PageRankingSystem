# PageRankingSystem
This script implements a PageRank system, which is a method for ranking web pages based on the number and quality of links between them. The program simulates how a user might randomly browse the web and uses this behavior to determine the importance of each page in a given corpus of web pages.

# Key Features:
1) Crawling Pages: The crawl() function parses a directory of HTML files and extracts the links between pages, building a representation of the network of web pages.

2) Transition Model: The transition_model() function generates a probability distribution over which page to visit next, based on a damping factor. It simulates the behavior of a web surfer who either follows a link from the current page or randomly jumps to another page.

3) Sampling Method: The sample_pagerank() function estimates PageRank values by simulating multiple random browsing sessions (using the transition model) and counting the frequency with which each page is visited. It uses a large number of samples (n) to produce accurate rankings.

4) Iterative Method: The iterate_pagerank() function computes PageRank by iteratively updating each page's rank until the values converge, based on a formula that accounts for the links between pages. This method avoids randomness and focuses purely on the link structure.
