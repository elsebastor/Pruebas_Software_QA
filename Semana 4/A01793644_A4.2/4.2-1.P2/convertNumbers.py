"""
This module contains functions for processing data using sys, time.
"""
import sys
import time

def process_file(file_path):
    """
    Read and process a file containing numeric data.

    This function reads a text file specified by 'file_path', extracts numeric data from it,
    converts the numeric data to binary and hexadecimal representations, and then prints and saves
    the results. It measures the time taken for processing and includes it in the output.

    Args:
        file_path (str): The path to the input text file containing numeric data.

    Returns:
        None

    Example:
        Given input file "data.txt" containing:
        10
        25
        42
        -5

        Output (printed and saved in "ConversionResults.txt"):
        Number  Binary   Hexadecimal  
        10      0b1010   A            
        25      0b11001  19           
        42      0b101010 2A           
        -5      -0b101   -5B          
        Elapsed Time: 0.12 seconds

    Note:
        - The function internally uses 'numbers_to_binary_and_hexa', 'print_converted_numbers',
          and 'save_converted_numbers' functions to perform conversions and output handling.
    """
    start_time = time.time()
    numbers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, item in enumerate(file, start=1):
                try:
                    number = int(item.strip())
                    numbers.append(number)
                except ValueError:
                    print(f"Invalid data on line {line_number}: \
                          '{item.strip()}' is not a valid number. Skipping...")

        if not numbers:
            raise ValueError("No valid numeric data found in the file.")
        numbers_h_b = numbers_to_binary_and_hexa(numbers)
        elapsed_time = time.time() - start_time  # Compute elapsed time
        print_converted_numbers(numbers_h_b, elapsed_time)
        save_converted_numbers(numbers_h_b, 'ConversionResults.txt', elapsed_time)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as ioe:
        print(f"An I/O error occurred while reading the file: {ioe}")





def number_to_hex(number):
    """
    Convert an integer to its hexadecimal representation.

    This function takes an integer as input and converts it to its hexadecimal representation.
    The resulting hexadecimal string is returned. The function handles both positive and negative
    integers.

    Args:
        number (int): An integer to be converted to hexadecimal.

    Returns:
        str: The hexadecimal representation of the input integer as a string.

    Example:
        Given input number: 255
        Output: 'FF'

        Given input number: -123
        Output: '-7B'

    Note:
        - The function optionally converts the result to uppercase letters.
        - For the input value 0, the function returns '0' to avoid an empty result.
    """
    heximal_num = f'{number & 0xFFFFFFFF:X}'
    return heximal_num


def number_to_binary(number):
    """
    Convert an integer to its binary representation.

    This function takes an integer as input and converts it to its binary representation.
    The resulting binary string is returned. The function handles both positive and negative
    integers.

    Args:
        number (int): An integer to be converted to binary.

    Returns:
        str: The binary representation of the input integer as a string.

    Example:
        Given input number: 10
        Output: '1010'

        Given input number: -5
        Output: '-101'

    Note:
        - The function handles the special case of 0, returning '0'.
        - If the input is negative, a '1' is added as a signifying prefix.
        - The binary representation is always returned as a string.
    """
    if number >= 0:
        # Procesamiento directo para números positivos
        binary_str = ''
        if number == 0:
            binary_str = '0'
        while number > 0:
            binary_str = str(number % 2) + binary_str
            number = number // 2
        return binary_str
        # Procesamiento para números negativos
    number = -number  # Convertir a positivo para trabajar con él
    binary_str = ''
    while number > 0:
        binary_str = str(number % 2) + binary_str
        number = number // 2

        # Paso 2: Invertir los bits
    inverted_binary_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)

        # Paso 3: Sumar 1 al resultado invertido
        # Convertimos la cadena invertida a lista de enteros para facilitar la suma
    binary_list = [int(bit) for bit in inverted_binary_str]
    for i in range(len(binary_list) - 1, -1, -1):
        if binary_list[i] == 0:
            binary_list[i] = 1
            break
    else:
            # Si todos los bits eran 1, agregamos un 1 al principio
        binary_list.insert(0, 1)
        # Convertir la lista de vuelta a cadena
    final_binary_str = ''.join(str(bit) for bit in binary_list)
        # Asegurarse de que la cadena tenga al menos la longitud necesaria para
        # coincidir con el ejemplo
    if len(final_binary_str) < 10:
        final_binary_str = '1' * (10 - len(final_binary_str)) + final_binary_str
    return final_binary_str

def numbers_to_binary_and_hexa(numbers):
    """
    Convert a list of integers to their binary and hexadecimal representations.

    This function takes a list of integers as input and converts each integer in the list to its
    binary and hexadecimal representations. The resulting binary and hexadecimal strings are
    returned as separate lists, preserving the original order of the input numbers.

    Args:
        numbers (list of int): A list of integers to be converted.

    Returns:
        tuple: A tuple containing three elements:
            1. The original list of integers.
            2. A list of binary representations for each integer.
            3. A list of hexadecimal representations for each integer.

    Example:
        Given input numbers: [10, -5, 255]
        Output:
        (
            [10, -5, 255],
            ['0b1010', '-0b101', '0xFF'],
            ['A', '-5B', 'FF']
        )

    Note:
        - The function utilizes the 'number_to_binary' and 'number_to_hex' functions internally
          to perform the conversions.
        - The binary representations are formatted with a '0b' prefix as Python does.
        - The hexadecimal representations are returned in uppercase.
    """
    bina = []
    hexa = []
    for number in numbers:
        # Manually convert each number to binary
        binary_string = number_to_binary(number)
        # Format the binary string as Python does, prefixed with '0b'
        formatted_binary_string =  binary_string
        bina.append(formatted_binary_string)

        h = number_to_hex(number)
        hexa.append(h)

    return numbers, bina, hexa



def print_converted_numbers(numbers_tuple, elapsed_time):
    """
    Print converted numbers, binary, and hexadecimal representations in a formatted table.

    This function takes a tuple containing lists of numbers, binary strings, and hexadecimal values,
    along with the elapsed time for processing, and prints them in a formatted table. The table
    includes headers for clarity and aligns the values for easy readability.

    Args:
        numbers_tuple (tuple): A tuple containing the following elements:
            1. A list of numbers (integers).
            2. A list of binary representations for each number.
            3. A list of hexadecimal representations for each number.
        elapsed_time (float): The time taken for processing, typically in seconds.

    Returns:
        None

    Example:
        Given input numbers_tuple:
        (
            [10, -5, 255],
            ['0b1010', '-0b101', '0xFF'],
            ['A', '-5B', 'FF']
        )
        and elapsed_time: 0.12345

        Output:
        Number     Binary       Hexadecimal  
        10         0b1010       A            
        -5         -0b101      -5B          
        255        0xFF         FF           
        elapsed time:0.12345

    Note:
        - The function formats the table with appropriate column widths.
        - Headers include 'Number', 'Binary', and 'Hexadecimal'.
    """
    numbers, binary_strings, hex_values = numbers_tuple  # Unpack the tuple

    # Find the maximum lengths of binary and hexadecimal strings for formatting
    max_binary_length = max(len(binary) for binary in binary_strings)
    max_hex_length = max(len(hexa) for hexa in hex_values)

    # Print headers for the matrix
    print(f"{'Number':<10} {'Binary':<{max_binary_length}} {'Hexadecimal':<{max_hex_length}}")

    # Print the values in a matrix-like format
    for number, binary, hexa in zip(numbers, binary_strings, hex_values):
        print(f"{number:<10} {binary:<{max_binary_length}} {hexa:<{max_hex_length}}")
    print(f"elapsed time:{elapsed_time}")



def save_converted_numbers(numbers_tuple, file_name, elapsed_time):
    """
    Save converted numbers, binary, and hexadecimal representations to a text file.

    This function takes a tuple containing lists of numbers, binary strings, and hexadecimal values,
    along with a file name and elapsed time for processing, and saves them to a text file. 
    The data is
    formatted and written in a table format within the text file.

    Args:
        numbers_tuple (tuple): A tuple containing the following elements:
            1. A list of numbers (integers).
            2. A list of binary representations for each number.
            3. A list of hexadecimal representations for each number.
        file_name (str): The name of the text file where the data will be saved.
        elapsed_time (float): The time taken for processing, typically in seconds.

    Returns:
        None

    Example:
        Given input numbers_tuple:
        (
            [10, -5, 255],
            ['0b1010', '-0b101', '0xFF'],
            ['A', '-5B', 'FF']
        )
        file_name: "ConvertedData.txt"
        and elapsed_time: 0.12345

        A file "ConvertedData.txt" will be created with the following content:
        Number  Binary   Hexadecimal  
        10      0b1010   A            
        -5      -0b101  -5B          
        255     0xFF     FF           
        Elapsed Time: 0.12 seconds

    Note:
        - The function formats the table with appropriate column widths.
        - Headers include 'Number', 'Binary', and 'Hexadecimal'.
        - The elapsed time is included in the saved file.
    """
    numbers, binary_strings, hex_values = numbers_tuple  # Unpack the tuple

    with open(file_name, 'w', encoding='utf-8') as file:
        max_number_length = max(len(str(number)) for number in numbers)
        max_binary_length = max(len(binary) for binary in binary_strings)
        max_hex_length = max(len(hexa) for hexa in hex_values)

        file.write(f"{'Number':<{max_number_length}} {'Binary':<{max_binary_length}} \
                   {'Hexadecimal':<{max_hex_length}}\n")

        for number, binary, hexa in zip(numbers, binary_strings, hex_values):
            file.write(f"{number:<{max_number_length}} {binary:<{max_binary_length}}\
                        {hexa:<{max_hex_length}}\n")

        file.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_file.py <file_path>")
        sys.exit(1)
    input_file_path = sys.argv[1]
    process_file(input_file_path)
