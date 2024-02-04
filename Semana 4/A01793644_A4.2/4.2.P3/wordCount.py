"""
This module contains functions for processing data using sys, time, and collections.
"""
import sys
import time

def read_words_from_file(file_path):
    """
    Read and split words from a text file.

    This function takes a file path as input, attempts to open the file in read 
    mode with UTF-8 encoding,
    and reads the content of the file. The content is split into individual 
    words based on whitespace,
    and a list of words is returned.

    Args:
        file_path (str): The path to the text file to read.

    Returns:
        list of str: A list of words read from the file, split based on whitespace.

    Example:
        Given input file "sample.txt" containing:
        "The quick brown fox jumps over the lazy dog."

        Output:
        ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog.']

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If an error occurs while reading the file.

    Note:
        - The function handles both normal text files and those with UTF-8 encoding.
        - In case of a file not found error, the function prints an error message and exits.
        - If any other exception occurs while reading the file, an error message is printed, and an
          empty list is returned.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_words = file.read().split()
            return file_words
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)


def count_word_frequencies(word_list):
    """
    Count the frequencies of words in a list of words.

    This function takes a list of words as input, processes each word to remove non-alphanumeric
    characters and convert it to lowercase, and then counts the occurrences of each unique word.
    The result is returned as a dictionary where keys represent unique words, and values represent
    their respective frequencies in the input list.

    Args:
        words (list of str): A list of words to count the frequencies of.

    Returns:
        dict: A dictionary where keys are unique words, and values are their frequencies.

    Example:
        Given input words: ['apple', 'Apple', 'banana', 'banana!', 'Orange', 'orange']
        Output:
        {
            'apple': 2,
            'banana': 2,
            'orange': 2
        }

    Note:
        - The function treats words with different capitalizations as the same word after
          converting them to lowercase.
        - Non-alphanumeric characters are removed from each word before counting.
        - Empty words are ignored in the counting process.
    """
    word_freq = {}
    for word_in_list in word_list:
        # Remove any non-alphanumeric characters and convert to lowercase
        cleaned_word = ''.join(char.lower() for char in word_in_list if char.isalnum())
        if cleaned_word:
            word_freq[cleaned_word] = word_freq.get(cleaned_word, 0) + 1
    return word_freq

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_program.py input_file.txt")
        sys.exit(1)

    start_time = time.time()  # Record the start time

    input_file = sys.argv[1]
    words = read_words_from_file(input_file)

    if not words:
        print("No valid words found in the file. Exiting.")
        sys.exit(1)

    word_count = count_word_frequencies(words)

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time

    print("Words and their frequencies:")
    for word, frequency in word_count.items():
        print(f"{word}: {frequency}")

    # Write the results to WordCountResults.txt, including execution time
    with open("WordCountResults.txt", "w", encoding='utf-8') as result_file:
        result_file.write("Words and their frequencies:\n")
        for word, frequency in word_count.items():
            result_file.write(f"{word}: {frequency}\n")
        result_file.write(f"Execution time: {execution_time:.2f} seconds\n")

    print("Results have been saved to WordCountResults.txt")
    print(f"Execution time: {execution_time:.2f} seconds")
