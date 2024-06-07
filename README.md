# music-genre-classification

This is a final project for ML Basics course in HSE SPb. [Presentation link](https://github.com/nixiieee/music-genre-classification/blob/main/presentation.pdf).

## Dataset
[GTZAN Dataset](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification/) from Kaggle was used.

## About the project
Some experiments on music genre classification task (can be found in [project.ipynb](https://github.com/nixiieee/music-genre-classification/blob/main/notebooks/project.ipynb) file).

The model chosen as a final one (which is CatBoost with tuned hyperparametrs) was integrated in a pipeline for telegram bot, which helps to get prediction on any music file with ```.wav``` or ```.mp3``` extension. 
