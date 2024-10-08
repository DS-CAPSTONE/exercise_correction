import os
import pandas as pd

from utility import DataGeneration

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


VIDEO_FEATURES_BINARY_PATH = "features/extracted_video_features_binary.csv"
EARLY_FUSED_FEATURES_BINARY_PATH = "features/fused_features_binary.csv"
VIDEO_FEATURES_MULTI_PATH = "features/extracted_video_features.csv"
EARLY_FUSED_FEATURES_MULTI_PATH = "features/fused_features.csv"


def evaluate_accuracy(X, y, support_vector_machine):
    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.25)
    clf = support_vector_machine.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print("Accuracy:", accuracy)
    return clf


def train_svm_binary_video():
    svm_video_binary = svm.SVC(kernel="poly", C=1)
    X, y = DataGeneration.io_sets_binary(VIDEO_FEATURES_BINARY_PATH)
    X = X.drop(['CORRUGATOR_GRAD'], axis=1)  # Remove unnecessary features
    print("SVM Video Binary Classification")
    svm_video_binary = evaluate_accuracy(X, y, svm_video_binary)
    return svm_video_binary


def train_svm_early_fusion():
    svm_early_fusion = svm.SVC(kernel="linear", C=1)
    X, y = DataGeneration.io_sets_binary(EARLY_FUSED_FEATURES_BINARY_PATH)
    X = X.drop(['NOSE_X', 'NOSE_Y', 'NOSE_Z', 'CORRUGATOR_GRAD'], axis=1)  # Remove unnecessary features
    print("SVM Early Fusion Binary Classification")
    svm_early_fusion = evaluate_accuracy(X, y, svm_early_fusion)
    return svm_early_fusion


def binary_classification():
    svm_video_binary = train_svm_binary_video()
    svm_early_fusion = train_svm_early_fusion()
    print("Binary classification for video and early fusion completed.")


def multiclass_classification():
    svm_video_multi = svm.SVC(kernel="poly", C=1)
    X, y = DataGeneration.io_sets_multiclass(VIDEO_FEATURES_MULTI_PATH)
    X = X.drop(['NOSE_X', 'NOSE_Y', 'NOSE_Z', 'CORRUGATOR_GRAD'], axis=1)
    print("SVM Video Multiclass Classification")
    svm_video_multi = evaluate_accuracy(X, y, svm_video_multi)

    svm_early_fusion_multi = svm.SVC(kernel="linear", C=1)
    X, y = DataGeneration.io_sets_multiclass(EARLY_FUSED_FEATURES_MULTI_PATH)
    X = X.drop(['NOSE_X', 'NOSE_Y', 'NOSE_Z', 'CORRUGATOR_GRAD'], axis=1)
    print("SVM Early Fusion Multiclass Classification")
    svm_early_fusion_multi = evaluate_accuracy(X, y, svm_early_fusion_multi)
