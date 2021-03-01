from analysis.service.reddit_analyzer import *
from analysis.service.plot import *


def main():
    vim_analyzer = RedditAnalyzer('data/vim_01-2021_03-2021.csv')
    emacs_analyzer = RedditAnalyzer('data/emacs_01-2021_03-2021.csv')

    # vim_analyzer.fit_distribution('created', 1.0, 0.0)
    # emacs_analyzer.fit_distribution('created', 1.0, 0.0)

    # plot_upvote_ratio(vim_analyzer, emacs_analyzer)
    # plot_awards_number(vim_analyzer, emacs_analyzer)
    # plot_comments_number(vim_analyzer, emacs_analyzer)
    # plot_created(vim_analyzer, emacs_analyzer)
    # plot_score(vim_analyzer, emacs_analyzer)
    # plot_sentiment(vim_analyzer, emacs_analyzer)
if __name__ == "__main__":
    main()
