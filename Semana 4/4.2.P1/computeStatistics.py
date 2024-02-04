"""
This module contains functions for processing data using sys, time, and collections.
"""
import sys
import time
from collections import Counter


def process_file(file_path):
    """
    Process a text file containing numerical data and compute statistics.

    This function takes the path to a text file as input, reads the data from the file,
    and computes various statistics (such as mean, median, mode, etc.) based on the
    numerical data in the file. The computed statistics are then printed to the console
    and saved to a text file named 'StatisticsResults.txt'.

    Args:
        file_path (str): The path to the text file containing numerical data to be processed.

    Example:
        Given input file 'data.txt' with the following content:
        10.5
        20.3
        15.2
        18.7

        The function will compute statistics and save the results to 'StatisticsResults.txt'.

    Note:
        - The function assumes that the input file contains one numerical value per line.
        - Invalid data in the file will be skipped, and a message will be printed for each
          invalid line.

    Raises:
        ValueError: If no valid numeric data is found in the file.

    Returns:
        None
    """
    start_time = time.time()  # Start timing

    numbers = []  # Initialize an empty list to store valid numbers
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, item in enumerate(file, start=1):
                try:
                    number = float(item.strip())
                    numbers.append(number)
                except ValueError:
                    print(f"Invalid data on line {line_number}: \
                          '{item.strip()}' is not a valid number. Skipping...")
            if not numbers:
                raise ValueError("No valid numeric data found in the file.")
            stats = compute_statistics(numbers)
            elapsed_time = time.time() - start_time  # Compute elapsed time
            stats['execution_time'] = elapsed_time

            #print(f"Execution Time: {stats.get('execution_time', 'N/A'):.4f} seconds")
            print_statistics(stats)
            save_statistics(stats, 'StatisticsResults.txt')
    except Exception as e:
        print(f"An error occurred: {e}")

def compute_statistics(numbers):
    """
    Calculate various statistics for a list of numerical values.

    This function calculates and returns the following statistics:
    - Mean (average) of the input numbers.
    - Median, which is the middle value of the sorted numbers or the 
      average of the two middle values if the number of values is even.
    - Mode, the most frequently occurring value(s) in the input list.
    - Variance, a measure of the spread of the values.
    - Standard deviation, the square root of the variance, indicating the dispersion of the values.

    Args:
        numbers (list): A list of numerical values for which statistics are to be computed.

    Returns:
        dict: A dictionary containing the calculated statistics.
            - 'count': Total count of values in the input list.
            - 'mean': Mean (average) of the values.
            - 'median': Median of the values.
            - 'mode': Mode of the values (list if multiple modes, or single mode).
            - 'variance': Variance of the values.
            - 'standard_deviation': Standard deviation of the values.
    """
    mean = sum(numbers) / len(numbers)
    numbers_sort = sorted(numbers)
    median = numbers_sort[len(numbers_sort) // 2] if len(numbers) % 2 != 0 else \
        (numbers_sort[len(numbers_sort) // 2 - 1] + numbers_sort[len(numbers_sort) // 2]) / 2
    modes = compute_mode(numbers)
    mode = modes[0] if isinstance(modes, list) else modes
    variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    standard_deviation = variance ** 0.5
    count = len(numbers)
    return {
        'count': count,
        'mean': mean,
        'median': median,
        'mode': mode,
        'standard_deviation': standard_deviation
    }

def print_statistics(stats):
    """
    Print statistics from a dictionary.

    This function takes a dictionary containing various statistics and prints them to the console.
    Each statistic is printed in the format "Stat Name: Stat Value" where the first letter of
    each statistic name is capitalized.

    Args:
        stats (dict): A dictionary containing statistics to be printed.

    Example:
        Given input stats:
        {
            'count': 100,
            'mean': 42.5,
            'median': 39.0,
            'mode': 42,
            'standard_deviation': 8.7
        }
        
        Output:
        Count: 100
        Mean: 42.5
        Median: 39.0
        Mode: 42
        Standard_deviation: 8.7
    """
    for key, value in stats.items():
        print(f"{key.capitalize()}: {value}")
    #print(f"Execution Time: {stats['execution_time']:.4f} seconds")

def save_statistics(stats, file_name):
    """
    Save statistics to a text file.

    This function takes a dictionary containing statistics and saves them to a text file with the
    specified file name. Each statistic is written in the format "Stat Name: Stat Value" where
    the first letter of each statistic name is capitalized. Each statistic is written on a separate
    line in the text file.

    Args:
        stats (dict): A dictionary containing statistics to be saved.
        file_name (str): The name of the file where statistics will be saved.

    Example:
        Given input stats:
        {
            'count': 100,
            'mean': 42.5,
            'median': 39.0,
            'mode': 42,
            'standard_deviation': 8.7
        }
        and file_name: "statistics.txt"

        A file "statistics.txt" will be created with the following content:
        Count: 100
        Mean: 42.5
        Median: 39.0
        Mode: 42
        Standard_deviation: 8.7
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for key, value in stats.items():
            file.write(f"{key.capitalize()}: {value}\n")

def compute_mode(numbers):
    """
    Calculate the mode (most frequent value) of a list of numerical values.

    This function calculates and returns the mode of the input list, which is the value(s)
    that appear most frequently in the list. If there is a tie for the mode (multiple values
    with the same highest frequency), all such values are returned.

    Args:
        numbers (list): A list of numerical values for which the mode is to be computed.

    Returns:
        list or str: The mode(s) of the input list. If there is a tie, a list containing
        multiple modes is returned. If all values are unique, the function returns the string
        '#N/A' to indicate that there is no mode.

    Example:
        Given input: [1, 2, 2, 3, 3, 4]
        Output: [2, 3]
        
        Given input: [1, 2, 3, 4]
        Output: '#N/A'
    """
    # Calculate frequencies of each number
    data = Counter(numbers)

    # Find the highest frequency
    max_frequency = max(data.values())

    # Find all numbers with the highest frequency
    mode = [number for number, freq in data.items() if freq == max_frequency]

    # If every number appears only once, return '#N/A'
    if len(mode) == len(numbers):
        return "#N/A"
    return mode

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_file.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    process_file(file_path)
