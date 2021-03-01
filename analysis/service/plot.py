from scipy.stats import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_upvote_ratio(vim_analyzer, emacs_analyzer):
    # Upvote Ratio Plotting
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))

    y_std, len_y, y = vim_analyzer.standarise('upvoteRatio', 1.0, 0.0)
    axes[0].hist(y, label='vim', edgecolor='black')
    axes[2].plot(y, lognorm.pdf(y_std, 0.002, -441.55, 441.56), label='vim')

    y_std, len_y, y = emacs_analyzer.standarise('upvoteRatio', 1.0, 0.0)
    axes[1].hist(y, color='brown', edgecolor='black', label='emacs')
    axes[2].plot(y, lognorm.pdf(y_std, 0.002, -474.671, 474.67), label='emacs', color='brown')

    axes[0].set_xlabel('upvoteRatio')
    axes[0].set_ylabel('frequency')
    axes[1].set_xlabel('upvoteRatio')
    axes[1].set_ylabel('frequency')
    axes[2].set_xlabel('upvoteRatio\nvim(LogNorm)\nemacs(LogNorm)')
    axes[2].set_ylabel('pdf')

    fig.tight_layout()
    axes[0].legend()
    axes[1].legend()
    axes[2].legend()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/upvote_ratio.png')
    plt.show()


def plot_comments_number(vim_analyzer, emacs_analyzer):
    # Comments Number Plotting

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))

    y_std, len_y, y = vim_analyzer.standarise('numComments', 1.0, 0.02)
    axes[0].hist(y, edgecolor='black', label='vim')
    axes[2].plot(y, lognorm.pdf(y_std, 0.97, -0.64, 0.383), label='vim')

    y_std, len_y, y = emacs_analyzer.standarise('numComments', 1.0, 0.02)
    axes[1].hist(y, color='brown', edgecolor='black', label='emacs')
    axes[2].plot(y, expon.pdf(y_std, -0.72, 0.72), label='emacs', color='brown')

    axes[0].set_xlabel('Number of Comments')
    axes[0].set_ylabel('frequency')
    axes[1].set_xlabel('Number of Comments')
    axes[1].set_ylabel('frequency')
    axes[2].set_xlabel('Number of Comments\nvim(LogNorm)\nemacs(Expon)')
    axes[2].set_ylabel('pdf')
    axes[0].legend()
    axes[1].legend()
    axes[2].legend()
    fig.tight_layout()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/num_comments.png')
    plt.show()


def plot_score(vim_analyzer, emacs_analyzer):
    ### Score Plotting
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))
    y_std, len_y, y = vim_analyzer.standarise('score', 1.0, 0.08)
    axes[0].hist(y, edgecolor='black', label='vim')
    axes[2].plot(y, invgauss.pdf(y_std, 14.58, -0.32, 0.02), label='vim')

    y_std, len_y, y = emacs_analyzer.standarise('score', 1.0, 0.0)
    axes[1].hist(y, color='brown', edgecolor='black', label='emacs')
    axes[2].plot(y, invgauss.pdf(y_std, 4.32, -0.53, 0.12), label='emacs', color='brown')

    axes[0].set_xlabel('Score')
    axes[0].set_ylabel('frequency')
    axes[1].set_xlabel('Score')
    axes[1].set_ylabel('frequency')
    axes[2].set_xlabel('Score\nvim(InvGauss)\nemacs(InvGauss)')
    axes[2].set_ylabel('pdf')

    axes[0].legend()
    axes[1].legend()
    axes[2].legend()

    fig.tight_layout()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/score.png')
    plt.show()


def plot_awards_number(vim_analyzer, emacs_analyzer):
    ### Number of Awards Plotting
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))
    y_std, len_y, y = vim_analyzer.standarise('numAwards', 1.0, 0.00)
    axes[0].hist(y, edgecolor='black', label='vim')
    # axes[1].plot(y, invgauss.pdf(y_std, 14.58, -0.32, 0.02))

    y_std, len_y, y = emacs_analyzer.standarise('numAwards', 1.0, 0.0)
    axes[1].hist(y, color='brown', edgecolor='black', label='emacs')
    # axes[1].plot(y, invgauss.pdf(y_std, 4.32, -0.53, 0.12))

    axes[0].set_xlabel('Number Awards')
    axes[0].set_ylabel('frequency')
    axes[1].set_xlabel('Number Awards')
    axes[1].set_ylabel('frequency')
    axes[2].set_xlabel('Number Awards')
    axes[2].set_ylabel('pdf')
    axes[0].legend()
    axes[1].legend()
    axes[2].legend()
    fig.tight_layout()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/num_awards.png')
    plt.show()


def plot_created(vim_analyzer, emacs_analyzer):
    ### Created Plotting
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 5))

    y_std, len_y, y = vim_analyzer.standarise('created', 1.0, 0.0)
    mpl_data = mdates.epoch2num(y)
    axes[0].hist(mpl_data, edgecolor='black', label='Vim')
    axes[2].plot(mpl_data, beta.pdf(y_std, 1.07, 1.05, -1.78, 3.53), label='vim')

    y_std, len_y, y = emacs_analyzer.standarise('created', 1.0, 0.0)
    mpl_data = mdates.epoch2num(y)
    axes[1].hist(mpl_data, edgecolor='black', color='brown', label='Emacs')
    axes[2].plot(mpl_data, uniform.pdf(y_std, -1.71, 3.45), label='Emacs', color='brown')

    axes[0].xaxis.set_major_locator(mdates.MonthLocator())
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    axes[1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    axes[2].xaxis.set_major_locator(mdates.MonthLocator())
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))

    axes[0].set_xlabel('Created')
    axes[0].set_ylabel('frequency')
    axes[1].set_xlabel('Created')
    axes[1].set_ylabel('frequency')
    axes[2].set_xlabel('Created\nvim(Beta)\nemacs(Uniform)')
    axes[2].set_ylabel('pdf')
    axes[0].legend()
    axes[1].legend()
    axes[2].legend()
    fig.tight_layout()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/created.png')
    plt.show()


def plot_sentiment(vim_analyzer, emacs_analyzer):
    # Pie Chart Plotting
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    vim_sentiments = vim_analyzer.calculate_sentiment()
    emacs_sentiments = emacs_analyzer.calculate_sentiment()
    my_explode = (0, 0.1, 0)
    axes[0].pie(vim_sentiments[0], autopct='%1.1f%%', startangle=90)
    axes[1].pie(emacs_sentiments[0], autopct='%1.1f%%', startangle=90)
    axes[0].axis('equal')
    axes[1].axis('equal')
    axes[0].legend(vim_sentiments[1])
    axes[1].legend(emacs_sentiments[1])
    plt.tight_layout()
    plt.savefig('./result/vim_emacs_01-2021_03-2021/sentiment_pie.png')
    plt.show()