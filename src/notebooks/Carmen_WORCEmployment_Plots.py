import sys
import os

# Add the parent directory (src) to sys.path
sys.path.append(os.path.abspath(".."))

from Carmen_WORCEmployment import load_and_clean
import matplotlib.pyplot as plt
import seaborn as sns


def plot_salary_by_gender(data):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x='Gender', y='Salary')
    plt.title("Salary Distribution by Gender")
    plt.show()


def plot_avg_salary_by_city(data):
    region_salary = data.groupby('Mailing City')['Salary'].mean().sort_values()
    region_salary.plot(kind='barh', figsize=(8, 5), title="Average Salary by KY Region")
    plt.xlabel("Average Salary")
    plt.show()


def plot_placements_over_time(data):
    data.set_index('Start Date').resample('M').size().plot(kind='line', marker='o', figsize=(10, 4))
    plt.title("Number of Placements Over Time")
    plt.ylabel("Placements")
    plt.show()


def plot_placement_type_by_program(data):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=data, x='ATP Placement Type', hue='Program: Program Name')
    plt.xticks(rotation=45)
    plt.title("Placement Type by Program")
    plt.show()


def plot_top_cities(data):
    city_counts = data['Mailing City'].value_counts().head(10)
    city_counts.plot(kind='bar', title='Top Cities by Participant Count', figsize=(8, 4))
    plt.ylabel("Count")
    plt.show()


def main():
    worc_clean = load_and_clean()

    plot_salary_by_gender(worc_clean)
    plot_avg_salary_by_city(worc_clean)
    plot_placements_over_time(worc_clean)
    plot_placement_type_by_program(worc_clean)
    plot_top_cities(worc_clean)


if __name__ == "__main__":
    main()
