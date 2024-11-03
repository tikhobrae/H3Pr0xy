import json  # Import the json library to handle JSON data
import os  # Import os for file path operations
import random  # Import random for selecting proxies randomly

# Define the path to the configuration file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'conf.json')

def load_config(file_path=config_path) -> json:
    """Load the configuration from a JSON file."""
    with open(file_path, 'r') as conf:
        config = json.load(conf)  # Load the JSON data into a dictionary
    return config  # Return the configuration dictionary

# Load the configuration when the module is imported
config = load_config()

def get(proxy_type: str) -> list:
    """Retrieve a list of proxies based on the specified type.

    Args:
        proxy_type (str): Type of proxies to retrieve ('best', 'good', or 'all').

    Returns:
        list: A list of proxies as strings.

    Raises:
        ValueError: If an invalid proxy type is provided.
    """
    # Determine the type of available proxies based on the input
    if proxy_type == 'best':
        avail_type = 'lowping'
    elif proxy_type == 'good':
        avail_type = 'working'
    elif proxy_type == 'all':
        avail_type = 'allproxy'
    else:
        raise ValueError('check proxy Type!')  # Raise an error for invalid types

    # Construct the path to the proxy file based on the configuration
    proxy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', config['proxy_path'][avail_type])
    
    # Read the proxy file and clean the lines
    with open(proxy_path, 'r') as file:
        get = file.readlines()  # Read all lines from the file
        cleaned_lines = [line.strip() for line in get if line.strip()]  # Remove empty lines and whitespace
    return cleaned_lines  # Return the cleaned list of proxies

def load(num: int, type: str) -> list:
    """Load a specified number of random proxies of a given type.

    Args:
        num (int): The number of proxies to load.
        type (str): The type of proxies to load ('best', 'good', or 'all').

    Returns:
        list: A list of randomly selected proxies.
    """
    proxies = get(proxy_type=type)  # Get the list of proxies of the specified type
    
    if num > len(proxies):
        num = len(proxies)  # Adjust num to the length of proxies if it's too large
    
    result = random.sample(proxies, num)  # Randomly sample the requested number of proxies
    return result  # Return the sampled proxies

def remove(proxy_type: str, which: str) -> None:
    """Remove a specified proxy from the proxy list.

    Args:
        proxy_type (str): The type of proxies from which to remove (e.g., 'best', 'good').
        which (str): The specific proxy to remove.
    
    Raises:
        ValueError: If an invalid proxy type is provided.
    """
    # Determine the available proxy type
    if proxy_type == 'best':
        avail_type = 'lowping'
    elif proxy_type == 'good':
        avail_type = 'working'
    elif proxy_type == 'all':
        avail_type = 'allproxy'
    else:
        raise ValueError('check proxy Type!')  # Raise an error for invalid types

    # Construct the path to the proxy file based on the configuration
    proxy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', config['proxy_path'][avail_type])
    
    # Read the existing proxies and filter out the one to be removed
    with open(proxy_path, "r") as file:
        lines = file.readlines()  # Read all lines from the file
    new_lines = [line for line in lines if which not in line]  # Keep lines that do not contain the proxy to remove

    # Write the remaining proxies back to the file
    with open(proxy_path, "w") as file:
        file.writelines(new_lines)  # Write the filtered lines back to the file
