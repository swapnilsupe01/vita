import numpy as np
from prettytable import PrettyTable
from collections import defaultdict

def compute_transition_emission_matrices(corpus):
    transition_counts = defaultdict(lambda: defaultdict(int))
    emission_counts = defaultdict(lambda: defaultdict(int))
    tag_counts = defaultdict(int)
    
    for sentence in corpus:
        prev_tag = None
        for word, tag in sentence:
            emission_counts[tag][word] += 1
            tag_counts[tag] += 1
            if prev_tag is not None:
                transition_counts[prev_tag][tag] += 1
            prev_tag = tag
    
    # Normalize counts to obtain probabilities
    transition_matrix = np.zeros((len(tag_counts), len(tag_counts)))
    emission_matrix = np.zeros((len(tag_counts), len(word_to_index)))
    
    for i, tag1 in enumerate(tag_counts):
        for j, tag2 in enumerate(tag_counts):
            transition_matrix[i][j] = transition_counts[tag1][tag2] / tag_counts[tag1]
    
    for i, tag in enumerate(tag_counts):
        for j, word in enumerate(word_to_index):
            emission_matrix[i][j] = emission_counts[tag][word] / tag_counts[tag]
    
    return transition_matrix, emission_matrix

def load_corpus(file_path):
    corpus = []
    with open(file_path, 'r') as file:
        for line in file:
            sentence = [tuple(word_tag.split('/')) for word_tag in line.strip().split()]
            corpus.append(sentence)
    return corpus

# Load corpus


# Function to compute transition and emission matrices from user-input sentences
def compute_transition_emission_matrices_from_input():
    # Prompt user to enter sentences
    corpus = []
    while True:
        sentence = input("Enter a sentence (or type 'done' to finish): ")
        if sentence.lower() == 'done':
            break
        corpus.append(sentence)

    # Calculate or estimate transition and emission matrices from the user-provided sentences
    # Example code to compute matrices (replace with actual implementation)
    transition_matrix = np.array([[0.1, 0.2, 0.3, 0.4],
                                   [0.2, 0.3, 0.1, 0.4],
                                   [0.3, 0.1, 0.2, 0.4],
                                   [0.2, 0.2, 0.3, 0.3]])  # Example transition matrix
    emission_matrix = np.array([[0.1, 0.2, 0.3, 0.1],
                                 [0.2, 0.3, 0.1, 0.2],
                                 [0.3, 0.1, 0.2, 0.3],
                                 [0.4, 0.1, 0.3, 0.4]])  # Example emission matrix

    return transition_matrix, emission_matrix

# Example usage:
T, E = compute_transition_emission_matrices_from_input()


# Now you can use the Viterbi algorithm with the computed matrices for POS tagging.
# Example usage:
x = input("Enter the sentence (words separated by spaces): ").split()  # Sequence of observations
S = [0.2, 0.3, 0.5, 0.4]  # Initial probabilities for states (including STOP state)

# Map words to indices
word_to_index = {"hi": 0, "hello": 1, "every": 2, "one": 3}
x_indices = [word_to_index.get(word, -1) for word in x]  # Map unknown words to -1

# Function to perform POS tagging on user-input sentences
def perform_pos_tagging_from_input(transition_matrix, emission_matrix, tag_set):
    pos_tagged_corpus = []
    while True:
        sentence = input("Enter a sentence (or type 'done' to finish): ")
        if sentence.lower() == 'done':
            break
        tokens = sentence.split()  # Tokenize sentence into words
        word_indices = [word_to_index.get(word.lower(), -1) for word in tokens]
        if -1 in word_indices:
            # Handle unknown words
            word_indices = [index if index != -1 else len(word_to_index) for index in word_indices]
        pos_tags = viterbi(word_indices, initial_probs, transition_matrix, emission_matrix)
        pos_tagged_corpus.append(list(zip(tokens, [tag_set[tag] for tag in pos_tags])))
    return pos_tagged_corpus

# Example usage:
# Assuming transition_matrix, emission_matrix, and tag_set are already defined
pos_tagged_corpus = perform_pos_tagging_from_input(transition_matrix, emission_matrix, tag_set)

# Output POS tags
for i, sentence in enumerate(pos_tagged_corpus):
    print(f"Sentence {i+1}:")
    table = PrettyTable(["Word", "POS Tag"])
    table.add_rows(sentence)
    print(table)
    print()


best_sequence = viterbi(x_indices, S, T, E)
display_table(x, best_sequence)  
