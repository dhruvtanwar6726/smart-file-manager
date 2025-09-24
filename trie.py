import os
from collections import defaultdict

# -------------------------------------------
# Trie Node Definition
# Each TrieNode represents a character in a word
# -------------------------------------------
class TrieNode:
    def __init__(self):
        self.children = {}     # Dictionary of child characters
        self.is_end = False    # Marks the end of a complete word (file name)

# -------------------------------------------
# FileTrie: Trie Data Structure for File Names
# Used for fast prefix-based search and autocomplete
# -------------------------------------------
class FileTrie:
    def __init__(self):
        self.root = TrieNode()

    # Insert a word (file name) into the Trie
    def insert(self, word):
        node = self.root
        for char in word.lower():  # Case-insensitive insertion
            node = node.children.setdefault(char, TrieNode())
        node.is_end = True  # Mark end of the file name

    # Search for file names starting with a given prefix
    def search(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []  # If prefix path breaks, return empty list
            node = node.children[char]
        return self._collect(prefix, node)

    # Helper function to collect all words starting from a node
    def _collect(self, prefix, node):
        results = [prefix] if node.is_end else []
        for char, next_node in node.children.items():
            results.extend(self._collect(prefix + char, next_node))
        return results

# -------------------------------------------
# File Categorization Logic
# -------------------------------------------
CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.docx', '.txt', '.xls', '.xlsx', '.pptx'],
    'Code': ['.py', '.java', '.cpp', '.js', '.html', '.css', '.ts'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Video': ['.mp4', '.mkv', '.avi'],
    'Archives': ['.zip', '.rar', '.7z'],
    'Others': []
}

# Determine the category of a file based on its extension
def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    return next((cat for cat, exts in CATEGORIES.items() if ext in exts), 'Others')

# -------------------------------------------
# Scanning and Indexing Files
# Builds:
# - file_map: file name → full path
# - categories: categorized files for UI
# - Inserts file names into the Trie
# -------------------------------------------
def build_file_index(root_dir, trie):
    file_map = {}                       # Maps file name to full path
    categories = defaultdict(list)      # Categorized file structure

    for dirpath, _, filenames in os.walk(root_dir):  # Traverse directories
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            file_map[file] = full_path  # Save file's full path
            trie.insert(file)           # Insert file name into the Trie
            cat = get_category(file)    # Categorize the file
            categories[cat].append({
                'name': file,
                'path': full_path
            })

    return file_map, categories

# -------------------------------------------
# Get all available categories (for UI display)
# -------------------------------------------
def get_all_categories(categories):
    return list(categories.keys())
