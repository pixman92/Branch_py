import argparse
import difflib
import os

def read_file(filepath):
    """Reads a file and returns its contents as a list of lines."""
    with open(filepath, 'r') as file:
        return file.readlines()

def compare_files(original_lines, secondary_lines):
    """Generates lists of common lines and differences between two files."""
    common_lines = []
    differences = []
    diff = difflib.ndiff(original_lines, secondary_lines)
    for line in diff:
        if line.startswith('  '):  # Common lines
            common_lines.append(line[2:])
        elif line.startswith('- ') or line.startswith('+ '):  # Differences
            differences.append(line)
    return common_lines, differences

def user_decision(differences):
    """Prompts user to decide on each difference, returns a list of accepted changes."""
    accepted_changes = []
    for line in differences:
        action = "ADD" if line.startswith('+ ') else "REMOVE"
        # Adjusted for Python 2.7 compatibility
        print "\n====="
        print "Change (%s): %s" % (action, line[2:])  # Show change without '- ' or '+ '
        choice = raw_input("Keep this change? (y/n): ").lower()
        if choice == 'y':
            accepted_changes.append(line[2:])  # Append accepted changes without markers
    return accepted_changes

def save_new_file(filepath, common_lines, accepted_changes):
    """Saves the new file with both common lines and accepted changes."""
    with open(filepath, 'w') as file:
        for line in common_lines + accepted_changes:
            file.write(line)

def main():
    parser = argparse.ArgumentParser(description="Compare two files and merge changes interactively.")
    parser.add_argument('--original', required=True, help="Path to the original file.")
    parser.add_argument('--secondary', required=True, help="Path to the secondary file.")
    args = parser.parse_args()

    # Check if 'new_file.txt' exists and handle according to user preference
    if os.path.exists('new_file.txt'):
        overwrite = raw_input("new_file.txt exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print "Operation cancelled by user."
            return

    original_lines = read_file(args.original)
    secondary_lines = read_file(args.secondary)

    common_lines, differences = compare_files(original_lines, secondary_lines)
    accepted_changes = user_decision(differences)

    save_new_file('new_file.txt', common_lines, accepted_changes)
    print "New file saved with accepted changes."

if __name__ == "__main__":
    main()