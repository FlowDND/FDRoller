"""
# @ Author: FlowDND
# @ Create Time: 2025-08-01 20:18:13
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import numpy as np
import plotly.graph_objects as PlotlyGraphObjects
from DiceData import (
    DICE_NUMBER,
    DICE_VERTICES,
    DICE_FACES,
    DICE_CENTERS,
    DICE_FACE_CENTERS,
)


def configTemplate() -> dict:
    folder: str = os.path.dirname(os.path.abspath(__file__))
    template_file_name: str = os.path.join(folder, "template.json")
    with open(template_file_name, "r", encoding="utf-8") as file:
        template: dict = json.load(file)
        pass
    return template
    pass


def hide(fig):
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                showbackground=False,
                zeroline=False,
                title="",
                visible=False,
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                showbackground=False,
                zeroline=False,
                title="",
                visible=False,
            ),
            zaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                showbackground=False,
                zeroline=False,
                title="",
                visible=False,
            ),
            bgcolor="rgba(0,0,0,0)",  # 透明背景
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),  # 调整视角
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # 去除纸张背景
        plot_bgcolor="rgba(0,0,0,0)",  # 去除绘图背景
        margin=dict(l=0, r=0, t=30, b=0),  # 减少边距
        showlegend=False,  # 隐藏图例
    )
    return fig
    pass


def createDice(dice: str, config: dict) -> list:
    """
    Creates a dice mesh with explicit edge lines for better visibility.
    Returns a list containing both the mesh and edge traces.
    """
    x, y, z = DICE_VERTICES[dice].T
    i, j, k = DICE_FACES[dice].T
    # Create the main mesh
    start_color = config.get("start_color", "green")
    middle_color = config.get("middle_color", "black")
    end_color = config.get("end_color", "lightgreen")
    mesh = PlotlyGraphObjects.Mesh3d(
        x=x,
        y=y,
        z=z,
        colorscale=[[0, start_color], [0.5, middle_color], [1, end_color]],
        # Intensity of each vertex, which will be interpolated and color-coded
        intensity=np.linspace(0, 1, len(x), endpoint=True),
        # i, j and k give the vertices of triangles
        i=i,
        j=j,
        k=k,
        name=dice,
        opacity=config.get("opacity", 0.8),
        showlegend=False,
        showscale=False,
    )
    # Start with the mesh in traces list
    traces = [mesh]
    # Add numbers on each face
    text_x, text_y, text_z, text_labels = [], [], [], []
    for idx, (i_val, j_val, k_val) in enumerate(zip(i, j, k)):
        # Calculate the centroid of the triangle
        centroid_x = (x[i_val] + x[j_val] + x[k_val]) / 3
        centroid_y = (y[i_val] + y[j_val] + y[k_val]) / 3
        centroid_z = (z[i_val] + z[j_val] + z[k_val]) / 3
        text_x.append(centroid_x)
        text_y.append(centroid_y)
        text_z.append(centroid_z)
        text_labels.append(str(idx + 1))
        pass
    # Add text trace for all numbers at once
    text_trace = PlotlyGraphObjects.Scatter3d(
        x=text_x,
        y=text_y,
        z=text_z,
        mode="text",
        text=text_labels,
        textposition="middle center",
        textfont=dict(
            size=config.get("font_size", 30), color=config.get("font_color", "white")
        ),
        showlegend=False,
        name=f"{dice}_numbers",
    )
    traces.append(text_trace)
    # Create edges if requested
    edge_color = config.get("edge_color", "black")
    edge_width = config.get("edge_width", 5)
    # Extract all edges from faces
    edges = set()
    faces = list(zip(i, j, k))
    for face in faces:
        # Add all edges of each triangle
        edges.add(tuple(sorted([face[0], face[1]])))
        edges.add(tuple(sorted([face[1], face[2]])))
        edges.add(tuple(sorted([face[2], face[0]])))
        pass
    # Create edge traces
    edge_x, edge_y, edge_z = [], [], []
    for edge in edges:
        v1, v2 = edge
        # Add line from vertex 1 to vertex 2
        edge_x.extend([x[v1], x[v2], None])
        edge_y.extend([y[v1], y[v2], None])
        edge_z.extend([z[v1], z[v2], None])
        pass
    edge_trace = PlotlyGraphObjects.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(color=edge_color, width=edge_width),
        name=f"{dice}_edges",
        showlegend=False,
    )
    traces.append(edge_trace)
    return traces
    pass


def view(figure: PlotlyGraphObjects.Figure, n_face: int) -> PlotlyGraphObjects.Figure:
    dice: str = figure.data[0].name
    if n_face <= len(DICE_FACES[dice]):
        ox: float = DICE_CENTERS[dice][0]
        oy: float = DICE_CENTERS[dice][1]
        oz: float = DICE_CENTERS[dice][2]
        cx: float = DICE_FACE_CENTERS[dice][n_face - 1][0]
        cy: float = DICE_FACE_CENTERS[dice][n_face - 1][1]
        cz: float = DICE_FACE_CENTERS[dice][n_face - 1][2]
        eye_pos: tuple[float, float, float] = (
            ox + (cx - ox) * 5,
            oy + (cy - oy) * 5,
            oz + (cz - oz) * 5,
        )
        figure.update_layout(
            scene_camera=dict(eye=dict(x=eye_pos[0], y=eye_pos[1], z=eye_pos[2]))
        )
        pass
    return figure
    pass


if __name__ == "__main__":
    config: dict = configTemplate()
    dice = createDice("d4", config)
    figure = PlotlyGraphObjects.Figure(data=dice)
    hide(figure)
    view(figure, 6)
    figure.show()
    pass
