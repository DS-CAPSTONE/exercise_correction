import os
import pandas as pd


def dataset_foreach_feature(csv_file):
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, csv_file)
    dataset = pd.read_csv(csv_path, sep='\t')
    print(f'Testing {csv_file} for binary classification: BL0 and PA4.')

    # Data standardization (z-score [-1,1])
    output_labels = dataset['PAIN_LEVEL'].copy()
    raw_input = dataset.drop(['SUBJECT_ID', 'PAIN_LEVEL', 'AGE', 'TRIAL', 'SEX'], axis=1)
    raw_input = (raw_input - raw_input.mean()) / raw_input.std()
    raw_input = raw_input.dropna(axis=1)
    raw_input = raw_input.dropna(axis=0)

    # No biosignals, focusing on video features only
    return raw_input, output_labels


def io_sets_multiclass(csv_file):
    # Data loading
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, csv_file)
    dataset = pd.read_csv(csv_path, sep='\t')
    print(f'Extracting sets from {csv_file}, for multiclass classification of the labels BL0 and PA4.')

    # Mapping to numeric values (one-hot encoding not used)
    dataset['PAIN_LEVEL'] = dataset['PAIN_LEVEL'].replace(['BL1', 'PA1', 'PA2', 'PA3', 'PA4'], [0, 1, 2, 3, 4])

    # Drop the null attributes and the subject column
    dataset = dataset.dropna(axis=1)
    dataset = dataset.drop(['SUBJECT_ID'], axis=1)

    # Data standardization (z-score [-1,1])
    y = dataset['PAIN_LEVEL'].copy()
    X = dataset.drop(['PAIN_LEVEL', 'AGE', 'TRIAL'], axis=1)
    X = (X - X.mean()) / X.std()
    X = X.dropna(axis=1)
    X = X.dropna(axis=0)

    return X, y


def io_sets_binary(csv_file):
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, csv_file)
    dataset = pd.read_csv(csv_path, sep='\t')

    # Mapping to binary labels
    dataset['PAIN_LEVEL'] = dataset['PAIN_LEVEL'].replace(['BL1', 'PA4'], [0, 1])

    # Drop the null attributes and the subject column
    dataset = dataset.dropna(axis=1)
    dataset = dataset.drop(['SUBJECT_ID'], axis=1)

    # Data standardization (z-score [-1,1])
    y = dataset['PAIN_LEVEL'].copy()
    X = dataset.drop(['PAIN_LEVEL', 'AGE', 'TRIAL', 'SEX'], axis=1)
    X = (X - X.mean()) / X.std()
    X = X.dropna(axis=1)
    X = X.dropna(axis=0)

    return X, y


def io_sets_video_only():
    csv_file = "features/extracted_video_features_binary.csv"
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, csv_file)
    dataset = pd.read_csv(csv_path, sep='\t')

    # Mapping to binary labels
    dataset['PAIN_LEVEL'] = dataset['PAIN_LEVEL'].replace(['BL1', 'PA4'], [0, 1])

    # Drop the null attributes and the subject column
    dataset = dataset.dropna(axis=1)
    dataset = dataset.drop(['SUBJECT_ID'], axis=1)

    # Data standardization (z-score [-1,1])
    y = dataset['PAIN_LEVEL'].copy()
    X = dataset.drop(['PAIN_LEVEL', 'AGE', 'TRIAL', 'SEX'], axis=1)
    X = (X - X.mean()) / X.std()
    X = X.dropna(axis=1)
    X = X.dropna(axis=0)

    return X, y


def binarize_video_features():
    f = open('features/extracted_video_features.csv', 'r', encoding='UTF-8', newline='')
    df = pd.read_csv(f, sep='\t')
    df = df[~df['PAIN_LEVEL'].isin(['PA1', 'PA2', 'PA3'])]
    df.to_csv('features/extracted_video_features_binary.csv', index=False, sep='\t')
    f.close()


def early_fusion_video_features():
    # Placeholder if video fusion is necessary in the future
    print("Performing early fusion on video features.")
    pass
