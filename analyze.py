import json
import matplotlib.pyplot as plt
import os
from collections import Counter

# Setting up paths
data_file = r'c:\Users\2423029\Documents\GitHub\dataanalysis\dataset.json'
output_dir = r'C:\Users\2423029\Documents\GitHub\dataanalysis'
os.makedirs(output_dir, exist_ok=True)

# Load data
with open(data_file, 'r', encoding='utf-8') as f:
    tickets = json.load(f)

# Extract fields
categories = [t.get('category', 'Unknown') for t in tickets]
courses = [t.get('course', 'Unknown').capitalize() for t in tickets]
duplicates = [str(t.get('duplicate', False)) for t in tickets]
issue_tags = [t.get('issue_tag', 'Unknown') for t in tickets]

def plot_bar(counter_obj, title, xlabel, ylabel, filename, color='skyblue'):
    if not counter_obj:
        return
    labels, values = zip(*counter_obj.most_common())
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=color)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    # Only use integer ticks on y axis
    plt.yticks(range(0, max(values) + 2))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()

# 1. Number of tickets per category
cat_counts = Counter(categories)
plot_bar(cat_counts, 'Number of Tickets per Category', 'Category', 'Number of Tickets', 'tickets_per_category.png', color='coral')

# 2. Tickets per course/team
course_counts = Counter(courses)
plot_bar(course_counts, 'Tickets per Course/Team', 'Course', 'Number of Tickets', 'tickets_per_course.png', color='lightgreen')

# 3. Duplicate / repeat issues
dup_counts = Counter(duplicates)
# Standardize true/false to start with uppercase for pie chart labels
dup_counts_renamed = Counter({'Duplicate': dup_counts.get('True', 0), 'Unique': dup_counts.get('False', 0)})

plt.figure(figsize=(6, 6))
plt.pie(dup_counts_renamed.values(), labels=dup_counts_renamed.keys(), autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'], startangle=140)
plt.title('Proportion of Duplicate Issues', fontsize=14)
plt.axis('equal')
plt.savefig(os.path.join(output_dir, 'duplicate_issues.png'), dpi=300)
plt.close()

# 4. Most common issues (by issue_tag)
tag_counts = Counter(issue_tags)
labels, values = zip(*tag_counts.most_common())
plt.figure(figsize=(10, 6))
plt.barh(labels, values, color='mediumpurple')
plt.title('Most Common Issues (by Issue Tag)', fontsize=14)
plt.xlabel('Number of Occurrences', fontsize=12)
plt.ylabel('Issue Tag', fontsize=12)
plt.xticks(range(0, max(values) + 2))
plt.gca().invert_yaxis()  # Highest at top
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'most_common_issues.png'), dpi=300)
plt.close()

print("Graphs generated successfully.")
