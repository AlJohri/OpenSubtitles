#!/usr/bin/env python

from __future__ import print_function

import logging, sys, random
from time import time

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cross_validation import cross_val_score
from sklearn import metrics

import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins

print ("loading data... ")

from load import movies
movies = np.array(movies)

print ("loaded data")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# http://scikit-learn.org/0.14/auto_examples/document_clustering.html#example-document-clustering-py
# http://scikit-learn.org/stable/auto_examples/document_clustering.html

N_CLUSTERS = 5
PLOT = True

naive_bayes = MultinomialNB(alpha=0.1,fit_prior=True)
k_means = KMeans(n_clusters=N_CLUSTERS, init='k-means++', max_iter=100, n_init=1, verbose=True)
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

# vectorize
text = [movie['script'] for movie in movies]
X = vectorizer.fit_transform(text)

print(X.shape)

if PLOT==True:
    # reduce dimensionality
    svd = TruncatedSVD(2)
    # lsa = make_pipeline(svd, Normalizer(copy=False))
    lsa = svd
    X = lsa.fit_transform(X)

# cluster
km = k_means.fit(X)

k_means_labels = k_means.labels_
k_means_cluster_centers = k_means.cluster_centers_
k_means_labels_unique = np.unique(k_means_labels)

if PLOT==True:
    # fig = plt.figure(figsize=(8, 3))
    # fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.grid(True, alpha=0.3)

    colors = [(random.random(), random.random(), random.random()) for x in range(N_CLUSTERS)]
    for k, col in zip(range(N_CLUSTERS), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        points = ax.plot(X[my_members, 0], X[my_members, 1], 'w', markerfacecolor=col, marker='.')
        centers = ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
        
        labels = []
        for movie in movies[k_means_labels == k]:
            labels.append(movie.get('Title', '') + " " + movie.get('imdbID', '') + " " + ", ".join(movie.get('Genre', '')) )

        tooltip = plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10)
        plugins.connect(fig, tooltip)

    # import pdb; pdb.set_trace()

    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())

    # plt.show()
    with open("output.html", 'w') as f:
        mpld3.save_html(fig, f)
    
    mpld3.show()


if PLOT==False:

    print("Top terms per cluster:")
    print()
    order_centroids = k_means_cluster_centers.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(N_CLUSTERS):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :100]:
            print(' %s' % terms[ind], end='')
        print()
        print()

    # changed genres into array so cannot just use "mode" method any longer

    # print("Top genres per cluster:")
    # print()
    # for k in range(N_CLUSTERS):
    #   print("Cluster %d:" % i, end='')
    #   genres = [movie.get('Genre') for movie in movies[k_means_labels == k] ]
    #   print (mode(genres))
    #   print ("out of")
    #   print (len(genres))

