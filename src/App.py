"""
# @ Author: FlowDND
# @ Create Time: 2025-08-02 00:35:11
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import streamlit as st
import plotly
from Dices import view, hide, configTemplate, createDice
from DiceData import DICE_NUMBER
import pandas as pd


def main() -> None:
    st.set_page_config(
        page_title="FlowDNDRoller-龙与地下城之骰子",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("FlowDNDRoller - 龙与地下城之骰子")
    template = configTemplate()
    st.sidebar.header("骰子配置")
    st.sidebar.markdown("---")
    start_color = st.sidebar.color_picker("起始颜色", value=template["start_color"])
    middle_color = st.sidebar.color_picker("中间颜色", value=template["middle_color"])
    end_color = st.sidebar.color_picker("结束颜色", value=template["end_color"])
    opacity = st.sidebar.slider(
        "透明度", min_value=0.0, max_value=1.0, value=template["opacity"], step=0.1
    )
    st.sidebar.markdown("---")
    font_size = st.sidebar.slider(
        "字体大小", min_value=10, max_value=100, value=template["font_size"], step=1
    )
    font_color = st.sidebar.color_picker("字体颜色", value=template["font_color"])
    edge_color = st.sidebar.color_picker("边缘颜色", value=template["edge_color"])
    edge_width = st.sidebar.slider(
        "边缘宽度", min_value=0, max_value=10, value=template["edge_width"], step=1
    )
    st.sidebar.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.header("骰子设置")
        dice_type = st.selectbox(
            "骰子类型",
            options=DICE_NUMBER.keys(),
            index=0,
            help="选择骰子类型",
        )
        dice_times = st.number_input(
            "掷骰次数",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            help="设置掷骰的次数",
        )
        dice_addition = st.number_input(
            "骰子加值",
            min_value=-100,
            max_value=100,
            value=0,
            step=1,
            help="设置骰子加值",
        )
        dice_button = st.button(
            "掷骰",
            help="点击掷骰按钮进行掷骰",
        )
        pass
    with col2:
        if dice_button:
            results = []
            for _ in range(dice_times):
                result = random.randint(1, DICE_NUMBER[dice_type]) + dice_addition
                results.append(result)
                pass
            st.markdown("### 掷骰结果")
            st.write(f"骰子类型: {dice_type}")
            st.write(f"掷骰次数: {dice_times}")
            st.write(f"骰子加值: {dice_addition}")
            st.write(f"结果: {results}")
            dice_trace = createDice(
                dice_type,
                {
                    "start_color": start_color,
                    "middle_color": middle_color,
                    "end_color": end_color,
                    "opacity": opacity,
                    "font_size": font_size,
                    "font_color": font_color,
                    "edge_color": edge_color,
                    "edge_width": edge_width,
                },
            )
            dice_figure = plotly.graph_objects.Figure(data=dice_trace)
            hide(dice_figure)
            st.plotly_chart(
                view(dice_figure, results[-1]),
                use_container_width=True,
                config={"displayModeBar": False, "scrollZoom": True},
            )
            # 添加到历史记录
            if "history" not in st.session_state:
                st.session_state.history = []
            new_entry = {
                "掷骰编号": len(st.session_state.history) + 1,
                "骰子类型": dice_type,
                "掷骰次数": dice_times,
                "骰子加值": dice_addition,
                "各骰结果": results,
                "总和": sum(results),
            }
            st.session_state.history.append(new_entry)
        else:
            # 显示预览骰子（不投掷）
            st.markdown("### 骰子预览")
            st.write(f"骰子类型: {dice_type}")
            st.write("点击'掷骰'按钮开始投掷")
            dice_trace = createDice(
                dice_type,
                {
                    "start_color": start_color,
                    "middle_color": middle_color,
                    "end_color": end_color,
                    "opacity": opacity,
                    "font_size": font_size,
                    "font_color": font_color,
                    "edge_color": edge_color,
                    "edge_width": edge_width,
                },
            )
            dice_figure = plotly.graph_objects.Figure(data=dice_trace)
            hide(dice_figure)
            st.plotly_chart(
                view(dice_figure, 1),  # 默认显示面1
                use_container_width=True,
                config={"displayModeBar": False, "scrollZoom": True},
            )
        pass
    # 历史记录
    st.markdown("---")
    st.header("历史记录")
    if "history" not in st.session_state:
        st.session_state.history = []
        pass
    if st.session_state.history:
        dataframe = pd.DataFrame(st.session_state.history)
        st.dataframe(dataframe, use_container_width=True)
        pass
    # clean up dataframe
    if st.button("清除历史记录"):
        st.session_state.history = []
        st.success("历史记录已清除")
        pass
    pass


if __name__ == "__main__":
    main()
    pass
