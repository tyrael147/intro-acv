"""
Utility functions for visualization in Life Cycle Assessment (LCA).
"""

from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.sankey import Sankey


def plot_sankey_tree(
    data: List[Dict[str, Any]],
    title: str = "LCA Contribution Tree",
    value_field: str = "fraction",
    height: int = 800,
    width: int = 1200,
    use_plotly: bool = True,
    max_label_length: int = 50,
    min_fraction: float = 0.0,
    show_values: bool = True,
) -> None:
    """
    Plot a Sankey diagram showing the hierarchical tree structure of LCA contributions.

    The thickness of arrows represents the contribution (fraction) of each node to its parent.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of dictionaries, each representing a node in the tree with keys:
        - 'label': unique identifier for the node
        - 'parent': label of parent node (None for root)
        - 'score': impact score
        - 'fraction': contribution to total impact (used for arrow thickness)
        - 'name': descriptive name of the activity
        - 'amount': amount value
        - 'key': unique key tuple
    title : str, optional
        Title of the diagram (default: "LCA Contribution Tree")
    value_field : str, optional
        Field to use for link values ('fraction' or 'score') (default: "fraction")
    height : int, optional
        Height of the figure in pixels (default: 800)
    width : int, optional
        Width of the figure in pixels (default: 1200)
    use_plotly : bool, optional
        If True, use Plotly; if False, use matplotlib (default: True)
    max_label_length : int, optional
        Maximum length for node labels (default: 50)
    min_fraction : float, optional
        Minimum fraction to display (filter small contributions) (default: 0.0)
    show_values : bool, optional
        Whether to show values in labels (default: True)

    Returns
    -------
    None
        Displays the Sankey diagram

    Examples
    --------
    >>> data = [
    ...     {'label': 'root', 'parent': None, 'score': 62.29, 'fraction': 1.0,
    ...      'amount': 1.0, 'name': 'Bicycle, conventional, urban, 2020',
    ...      'key': ('bafu', '522701.0')},
    ...     {'label': 'root_a', 'parent': 'root', 'score': 56.58, 'fraction': 0.908,
    ...      'amount': 0.706, 'name': 'Bicycle, at regional storage',
    ...      'key': ('bafu', '291950.0')},
    ... ]
    >>> plot_sankey_tree(data)
    """

    if use_plotly:
        _plot_sankey_plotly(
            data,
            title,
            value_field,
            height,
            width,
            max_label_length,
            min_fraction,
            show_values,
        )
    else:
        _plot_sankey_matplotlib(
            data,
            title,
            value_field,
            height,
            width,
            max_label_length,
            min_fraction,
            show_values,
        )


def _plot_sankey_plotly(
    data: List[Dict[str, Any]],
    title: str,
    value_field: str,
    height: int,
    width: int,
    max_label_length: int,
    min_fraction: float,
    show_values: bool,
) -> None:
    """Internal function to plot Sankey diagram using Plotly."""

    # Filter data by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    if not filtered_data:
        print("No data to display after filtering.")
        return

    # Create a mapping from label to index
    label_to_idx = {node["label"]: idx for idx, node in enumerate(filtered_data)}

    # Prepare node labels
    node_labels = []
    for node in filtered_data:
        name = node["name"]
        if len(name) > max_label_length:
            name = name[: max_label_length - 3] + "..."

        if show_values:
            label = f"{name}<br>({node['fraction'] * 100:.1f}%)"
        else:
            label = name

        node_labels.append(label)

    # Prepare links (edges from parent to child)
    sources = []
    targets = []
    values = []
    link_labels = []

    for node in filtered_data:
        if node["parent"] is not None:
            # Check if parent exists in filtered data
            if node["parent"] in label_to_idx:
                parent_idx = label_to_idx[node["parent"]]
                child_idx = label_to_idx[node["label"]]

                sources.append(parent_idx)
                targets.append(child_idx)

                # Use specified field for link value
                value = node.get(value_field, node.get("fraction", 0))
                values.append(value)

                # Create hover text for link
                link_label = f"{node['name'][:30]}<br>Fraction: {node['fraction'] * 100:.2f}%<br>Score: {node['score']:.2f}"
                link_labels.append(link_label)

    # Create color scale based on fraction
    node_colors = []
    for node in filtered_data:
        fraction = node["fraction"]
        # Color gradient from light blue (low) to dark red (high)
        if fraction > 0.5:
            color = f"rgba(220, 20, 60, {0.3 + fraction * 0.7})"  # Crimson
        elif fraction > 0.1:
            color = f"rgba(255, 140, 0, {0.3 + fraction * 0.7})"  # Dark orange
        else:
            color = f"rgba(70, 130, 180, {0.3 + fraction * 0.7})"  # Steel blue
        node_colors.append(color)

    # Create link colors (lighter versions, with transparency)
    link_colors = []
    for target_idx in targets:
        node = filtered_data[target_idx]
        fraction = node["fraction"]
        if fraction > 0.5:
            color = "rgba(220, 20, 60, 0.2)"  # Light crimson
        elif fraction > 0.1:
            color = "rgba(255, 140, 0, 0.2)"  # Light orange
        else:
            color = "rgba(70, 130, 180, 0.2)"  # Light steel blue
        link_colors.append(color)

    # Create the Sankey diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=node_labels,
                    color=node_colors,
                    hovertemplate="%{label}<br>Score: %{value:.2f}<extra></extra>",
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                    hovertemplate="%{label}<extra></extra>",
                    customdata=link_labels,
                ),
                orientation="h",
                arrangement="snap",
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial, sans-serif"),
            x=0.5,
            xanchor="center",
        ),
        font=dict(size=12),
        height=height,
        width=width,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.show()


def _plot_sankey_matplotlib(
    data: List[Dict[str, Any]],
    title: str,
    value_field: str,
    height: int,
    width: int,
    max_label_length: int,
    min_fraction: float,
    show_values: bool,
) -> None:
    """
    Internal function to plot Sankey diagram using Matplotlib.

    Note: Matplotlib's Sankey is more limited and works best for simpler diagrams.
    For complex hierarchical trees, consider using Plotly instead.
    """

    # Filter data by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    if not filtered_data:
        print("No data to display after filtering.")
        return

    # Note: Matplotlib's Sankey is designed for flow diagrams, not hierarchical trees
    # This is a simplified implementation
    print("Warning: Matplotlib's Sankey has limited support for hierarchical trees.")
    print("For better results, use use_plotly=True")

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))

    # Build tree level by level
    root = None
    for node in filtered_data:
        if node["parent"] is None:
            root = node
            break

    if root is None:
        print("No root node found.")
        return

    # Simple visualization: just show top-level contributions
    children = [node for node in filtered_data if node["parent"] == root["label"]]

    if not children:
        print("No children found for root node.")
        return

    # Sort children by fraction (descending)
    children.sort(key=lambda x: x["fraction"], reverse=True)

    # Create a simple Sankey diagram for one level
    sankey = Sankey(ax=ax, scale=0.01, offset=0.3, head_angle=120)

    # Calculate flows
    flows = []
    labels = []
    orientations = []

    # Input flow (root)
    flows.append(1.0)
    root_name = root["name"][:max_label_length]
    if show_values:
        labels.append(f"{root_name}\n{root['fraction'] * 100:.1f}%")
    else:
        labels.append(root_name)
    orientations.append(0)

    # Output flows (children)
    for child in children[:10]:  # Limit to top 10 for readability
        flows.append(-child["fraction"])
        child_name = child["name"][:max_label_length]
        if show_values:
            labels.append(f"{child_name}\n{child['fraction'] * 100:.1f}%")
        else:
            labels.append(child_name)
        orientations.append(1)

    # Add remaining as "others" if needed
    if len(children) > 10:
        remaining = sum(c["fraction"] for c in children[10:])
        flows.append(-remaining)
        labels.append(f"Others\n{remaining * 100:.1f}%")
        orientations.append(1)

    sankey.add(
        flows=flows,
        labels=labels,
        orientations=orientations,
        pathlengths=[0.25] * len(flows),
    )

    diagrams = sankey.finish()

    plt.title(title, fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()


def print_tree_structure(
    data: List[Dict[str, Any]],
    max_depth: Optional[int] = None,
    min_fraction: float = 0.0,
) -> None:
    """
    Print the tree structure in a readable text format.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        List of dictionaries representing the tree nodes
    max_depth : int, optional
        Maximum depth to display (None for all levels)
    min_fraction : float, optional
        Minimum fraction to display (default: 0.0)
    """

    # Filter by minimum fraction
    filtered_data = [node for node in data if node.get("fraction", 0) >= min_fraction]

    # Build parent-to-children mapping
    children_map = {}
    root = None

    for node in filtered_data:
        parent = node.get("parent")
        if parent is None:
            root = node
        else:
            if parent not in children_map:
                children_map[parent] = []
            children_map[parent].append(node)

    # Sort children by fraction (descending)
    for children_list in children_map.values():
        children_list.sort(key=lambda x: x["fraction"], reverse=True)

    def print_node(node, depth=0, prefix=""):
        """Recursively print node and its children."""
        if max_depth is not None and depth > max_depth:
            return

        indent = "  " * depth
        fraction_pct = node["fraction"] * 100
        score = node["score"]
        name = node["name"]

        print(f"{indent}{prefix}{name}")
        print(f"{indent}  └─ Fraction: {fraction_pct:.2f}% | Score: {score:.2f}")

        # Print children
        label = node["label"]
        if label in children_map:
            for i, child in enumerate(children_map[label]):
                is_last = i == len(children_map[label]) - 1
                child_prefix = "└─ " if is_last else "├─ "
                print_node(child, depth + 1, child_prefix)

    if root:
        print("\n" + "=" * 80)
        print("LCA CONTRIBUTION TREE")
        print("=" * 80 + "\n")
        print_node(root)
        print("\n" + "=" * 80)
    else:
        print("No root node found in data.")
