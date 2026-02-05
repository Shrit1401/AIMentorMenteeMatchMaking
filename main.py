import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pandas as pd

from src.loadData import loadMentees, loadMentors
from src.matcher import findBestMentor, rankTopMentors


def buildMatches(mentees: pd.DataFrame, mentors: pd.DataFrame, top_k: int) -> Tuple[List[Dict], List[Dict]]:
    summary = []
    rankings = []

    for _, mentee in mentees.iterrows():
        bestMentor, bestScore, bestReason = findBestMentor(mentee, mentors)
        topMentors = rankTopMentors(mentee, mentors, topK=top_k)

        summary.append(
            {
                "mentee_name": mentee["name"],
                "mentor_name": bestMentor,
                "confidence_score": bestScore,
                "reason": bestReason,
            }
        )

        rankings.extend(
            {
                "mentee_name": mentee["name"],
                "rank": rank,
                "mentor_name": mentorInfo["mentor"],
                "confidence_score": mentorInfo["score"],
                "reason": mentorInfo["reason"],
            }
            for rank, mentorInfo in enumerate(topMentors, start=1)
        )

    return summary, rankings


def saveOutputs(results: List[Dict], ranked: List[Dict], output_dir: Union[str, Path], top_k: int) -> Tuple[Path, Path]:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result_path = out_dir / "result.csv"
    topk_path = out_dir / f"top{int(top_k)}.csv"
    pd.DataFrame(results).to_csv(result_path, index=False)
    pd.DataFrame(ranked).to_csv(topk_path, index=False)
    return result_path, topk_path


def run(mentees_path: Union[str, Path], mentors_path: Union[str, Path], output_dir: Union[str, Path], top_k: int) -> None:
    menteesCSV = loadMentees(mentees_path)
    mentorsCSV = loadMentors(mentors_path)
    results, top_results = buildMatches(menteesCSV, mentorsCSV, top_k)
    result_path, topk_path = saveOutputs(results, top_results, output_dir, top_k)
    print(f"Results saved to {result_path} and {topk_path}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mentormentee")
    p.add_argument("--mentees", default="data/mentees.csv")
    p.add_argument("--mentors", default="data/mentors.csv")
    p.add_argument("--out", default="output")
    p.add_argument("--top-k", type=int, default=3)
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    run(
        mentees_path=args.mentees,
        mentors_path=args.mentors,
        output_dir=args.out,
        top_k=args.top_k,
    )


if __name__ == "__main__":
    main()