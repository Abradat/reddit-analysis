import pandas as pd
import scipy.stats
from scipy.stats import *
from sklearn.preprocessing import StandardScaler
import numpy as np
import math
import matplotlib.pyplot as plt


class RedditAnalyzer():
    # Main class responsible for reading csv files and finding the fittest distribution to the metrics

    def __init__(self, csv_addr):
        self.df = pd.read_csv(csv_addr)

    def standarise(self, column, pct, pct_lower):
        # This method is for sorting the column data and removing the extreme outliers.
        sc = StandardScaler()
        y = self.df[column][self.df[column].notnull()].to_list()
        y.sort()
        len_y = len(y)
        y = y[int(pct_lower * len_y):int(len_y * pct)]
        len_y = len(y)
        yy = ([[x] for x in y])
        sc.fit(yy)
        y_std = sc.transform(yy)
        y_std = y_std.flatten()
        return y_std, len_y, y

    def fit_distribution(self, column, pct, pct_lower):
        # Set up list of candidate distributions to use
        y_std, size, y_org = self.standarise(column, pct, pct_lower)
        dist_names = ['weibull_min', 'norm', 'weibull_max', 'beta',
                      'invgauss', 'uniform', 'gamma', 'expon', 'lognorm', 'pearson3', 'triang']

        chi_square_statistics = []
        # 11 bins
        percentile_bins = np.linspace(0, 100, 11)
        percentile_cutoffs = np.percentile(y_std, percentile_bins)
        observed_frequency, bins = (np.histogram(y_std, bins=percentile_cutoffs))
        cum_observed_frequency = np.cumsum(observed_frequency)

        # Loop through candidate distributions

        for distribution in dist_names:
            # Set up distribution and get fitted distribution parameters
            dist = getattr(scipy.stats, distribution)
            param = dist.fit(y_std)
            print("{}\n{}\n".format(dist, param))

            # Get expected counts in percentile bins
            # cdf of fitted sistrinution across bins
            cdf_fitted = dist.cdf(percentile_cutoffs, *param)
            expected_frequency = []
            for bin in range(len(percentile_bins) - 1):
                expected_cdf_area = cdf_fitted[bin + 1] - cdf_fitted[bin]
                expected_frequency.append(expected_cdf_area)

            # Chi-square Statistics
            expected_frequency = np.array(expected_frequency) * size
            cum_expected_frequency = np.cumsum(expected_frequency)
            ss = round(sum(((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency), 0)
            chi_square_statistics.append(ss)

        # Sort by minimum ch-square statistics
        results = pd.DataFrame()
        results['Distribution'] = dist_names
        results['chi_square'] = chi_square_statistics
        results.sort_values(['chi_square'], inplace=True)

        print('\nDistributions listed by Betterment of fit:')
        print('............................................')
        print(results)
        print()

    def calculate_sentiment(self):
        # Calculation for total number of sentiments in each of the five categories.
        # Sentiment categories with 0 value are removed to have a clearer plot.
        sentiment_labels = []
        sentiment_values = []
        very_negative = self.df[self.df.titleSentiment == 0].shape[0]
        negative = self.df[self.df.titleSentiment == 1].shape[0]
        neutral = self.df[self.df.titleSentiment == 2].shape[0]
        positive = self.df[self.df.titleSentiment == 3].shape[0]
        very_positive = self.df[self.df.titleSentiment == 4].shape[0]

        if very_negative > 0:
            sentiment_values.append(very_negative)
            sentiment_labels.append('Very Negative')

        if negative > 0:
            sentiment_values.append(negative)
            sentiment_labels.append('Negative')

        if neutral > 0:
            sentiment_values.append(neutral)
            sentiment_labels.append('Neutral')

        if positive > 0:
            sentiment_values.append(positive)
            sentiment_labels.append('Positive')

        if very_positive > 0:
            sentiment_values.append(very_positive)
            sentiment_labels.append('Very Positive')

        return sentiment_values, sentiment_labels
