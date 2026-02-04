from src.loadData import loadData
from src.compare import compareMenteeWithMentor


def main():
    menteesCSV, mentorsCSV = loadData()
    
    mentee = menteesCSV.iloc[0]
    comparisons = compareMenteeWithMentor(mentee, mentorsCSV)
    for c in comparisons:
        print(c)

if __name__ == "__main__":
    main()