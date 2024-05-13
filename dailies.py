import sys
import re
import subprocess
from datetime import datetime

def update_html_list(html_file, new_list):
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Find the section of the HTML containing the list
    list_pattern = r'const inProgressItems = \[([\s\S]+?)\];'
    match = re.search(list_pattern, html_content)
    if match:
        old_list = match.group(1)

        # Update the list with the new one
        new_list_str = ',\n'.join(f'"{item}"' for item in new_list)
        new_html_content = html_content.replace(old_list, new_list_str)

        # Add current date to the HTML content
        current_date = datetime.now().strftime("%Y-%m-%d")
        new_html_content = re.sub(r'<p>Last updated: \d{4}-\d{2}-\d{2}</p>', f'<p>Last updated: {current_date}</p>', new_html_content)

        # Write the updated HTML to a file
        with open(html_file, 'w') as f:
            f.write(new_html_content)

        # Write the new list to dailies.txt
        with open('dailies.txt', 'a') as f:
            f.write(f'\n{current_date}\n')
            for item in new_list:
                f.write(item + '\n')

        # Commit and push changes to Git
        subprocess.run(['git', 'add', html_file, 'dailies.txt'])
        subprocess.run(['git', 'commit', '-m', 'Updated list in HTML file and dailies.txt'])
        subprocess.run(['git', 'push'])

        print("List updated successfully, dailies saved, and changes pushed to Vercel.")
    else:
        print("Failed to find the list section in the HTML.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_list.py <html_file> <item1> <item2> ... <itemN>")
    else:
        html_file = sys.argv[1]
        new_list = sys.argv[2:]
        update_html_list(html_file, new_list)
