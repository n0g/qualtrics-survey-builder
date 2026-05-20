#!/usr/bin/env python3
"""Generate a PDF flow diagram of a Qualtrics survey's block structure.

Usage:
    python visualize.py survey.md
    python visualize.py survey.md -o output.pdf
    python visualize.py survey.md -f svg
"""

import argparse
import sys
from pathlib import Path

try:
    from graphviz import Digraph
except ImportError:
    print("graphviz is required: pip install graphviz", file=sys.stderr)
    sys.exit(1)

from convert import parse_survey


def _label_to_name(ref: str) -> str:
    if ref.startswith("@"):
        return ref[1:].replace("_", " ")
    return ref


def _resolve_choice_text(survey: dict, qid_ref: str, choice_idx: int) -> str:
    """Look up the choice text for a given question reference and choice index."""
    label_to_q: dict = {}
    qnum_to_q: dict = {}
    qid_num = 1
    for block in survey["blocks"]:
        for q in block["questions"]:
            if q.get("type") == "page_break":
                continue
            if q.get("label"):
                label_to_q[q["label"]] = q
            qnum_to_q[f"QID{qid_num}"] = q
            qid_num += 1

    q = label_to_q.get(qid_ref[1:]) if qid_ref.startswith("@") else qnum_to_q.get(qid_ref.upper())
    if q and q.get("choices") and 0 < choice_idx <= len(q["choices"]):
        return q["choices"][choice_idx - 1]
    return f"choice {choice_idx}"


def _condition_label(bl: dict, survey: dict) -> str:
    q_name = _label_to_name(bl["qid"])
    choice = _resolve_choice_text(survey, bl["qid"], bl["choice"])
    # Truncate long choice text
    if len(choice) > 20:
        choice = choice[:18] + "…"
    op = bl["operator"].lower()
    if op == "selected":
        return f"if {q_name} =\n{choice}"
    if op == "notselected":
        return f"if {q_name} ≠\n{choice}"
    return f"{q_name} {op} {choice}"


def build_flow_graph(survey: dict) -> Digraph:
    dot = Digraph(
        name="survey_flow",
        graph_attr={
            "rankdir": "TB",
            "splines": "polyline",
            "nodesep": "0.8",
            "ranksep": "0.6",
            "fontname": "Helvetica",
            "bgcolor": "white",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "10",
            "margin": "0.2,0.12",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "8",
            "color": "#333333",
        },
    )

    dot.node("__start__", "Start", shape="oval", style="filled", fillcolor="#dddddd")
    dot.node("__end__", "End of Survey", shape="oval", style="filled", fillcolor="#dddddd")

    prev_id = "__start__"

    for i, block in enumerate(survey["blocks"]):
        block_id = f"block_{i}"
        lines = [block["name"]]

        if block.get("loop_from"):
            lines.append(f"↻  {_label_to_name(block['loop_from'])}")

        label = "\n".join(lines)

        node_kw: dict = {"shape": "box"}
        if block.get("loop_from"):
            node_kw["style"] = "filled"
            node_kw["fillcolor"] = "#fff9c4"
        elif block.get("branch_logic"):
            node_kw["style"] = "dashed"

        dot.node(block_id, label, **node_kw)

        if block.get("branch_logic"):
            cond = _condition_label(block["branch_logic"], survey)
            dot.edge(prev_id, block_id, label=cond, style="dashed", color="#666666", fontcolor="#444444")
        else:
            dot.edge(prev_id, block_id)

        # Early exit to end of survey from skip logic
        has_early_exit = any(
            sl.get("destination") == "ENDOFSURVEY"
            for q in block["questions"]
            if q.get("type") != "page_break"
            for sl in q.get("skip_logic", [])
        )
        if has_early_exit:
            dot.edge(
                block_id, "__end__",
                style="dashed", color="#aaaaaa", fontcolor="#888888",
                label="early exit", constraint="false",
            )

        prev_id = block_id

    dot.edge(prev_id, "__end__")
    return dot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a flow diagram of a survey's block structure"
    )
    parser.add_argument("input", help="Input .md survey file")
    parser.add_argument("-o", "--output", help="Output path (default: same name as input)")
    parser.add_argument(
        "-f", "--format", default="pdf",
        choices=["pdf", "svg", "png"],
        help="Output format (default: pdf)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_stem = Path(args.output).with_suffix("")
    else:
        output_stem = input_path.with_suffix("")

    survey = parse_survey(input_path.read_text(encoding="utf-8"))
    dot = build_flow_graph(survey)
    dot.format = args.format
    dot.render(str(output_stem), cleanup=True)

    print(f"✓ {output_stem}.{args.format}")
    print(f"  Blocks: {len(survey['blocks'])}")


if __name__ == "__main__":
    main()
