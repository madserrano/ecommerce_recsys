# AIML-Recommender System for e-commerce

This project is a recommender system built for an e-commerce website selling cars such as Autotrader. Surprise, or Simple Python Recommendation System Engine, is a python Scikit package that we leveraged to build and analyze this RecSys. It provides prediction algorithm modules that we can easily use, such as k-NN based algorithm and the built-in similarity measures. 

The development process began with transforming the car reviews dataset into a format that Surprise can work with – a series of a sparse matrix where items are transposed into columns and ratings become elements in this matrix. 
Our model was trained on the data related to the same year of the car selected by the user. When we worked with KNNBaseline to derive the nearest neighbor, there are two parameters that we need to define: (1) k or the maximum number of neighbors to consider for accumulation, and (2) sim_options which pertains to similarity options. 
In our solution, cosine similarity and Pearson baseline are the methods that we have assessed.

Due to capacity limitation, the full code cannot be pushed to this repo. But can be viewed in this public colab:
https://drive.google.com/drive/folders/1TtKHa_U60G-3LYkfkLDmTUqsEPMid8mW?usp=sharing
