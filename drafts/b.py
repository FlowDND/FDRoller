import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
from math import cos, sin, pi

# 设置页面配置
st.set_page_config(
    page_title="DND 骰子系统",
    page_icon="🎲",
    layout="wide"
)

# 骰子类定义
class Dice3D:
    def __init__(self, dice_type):
        self.dice_type = dice_type
        self.sides = int(dice_type[1:])  # 从 'd6' 提取 6
        self.result = None
        
    def roll(self):
        self.result = random.randint(1, self.sides)
        return self.result

# 创建3D骰子模型
def create_dice_mesh(dice_type, result=None):
    if dice_type == 'd6':
        return create_cube_mesh(result)
    elif dice_type == 'd20':
        return create_icosahedron_mesh(result)
    elif dice_type == 'd12':
        return create_dodecahedron_mesh(result)
    elif dice_type == 'd10':
        return create_pentagonal_trapezohedron_mesh(result)
    elif dice_type == 'd8':
        return create_octahedron_mesh(result)
    elif dice_type == 'd4':
        return create_tetrahedron_mesh(result)
    else:
        return create_cube_mesh(result)

def create_cube_mesh(result=None):
    # 立方体顶点
    vertices = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # 底面
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # 顶面
    ])
    
    # 立方体面（三角形）
    faces = [
        [0, 1, 2], [0, 2, 3],  # 底面
        [4, 7, 6], [4, 6, 5],  # 顶面
        [0, 4, 5], [0, 5, 1],  # 前面
        [2, 6, 7], [2, 7, 3],  # 后面
        [0, 3, 7], [0, 7, 4],  # 左面
        [1, 5, 6], [1, 6, 2]   # 右面
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    # 根据结果设置颜色
    if result:
        colors = ['red' if face_idx // 2 + 1 == result else 'lightblue' 
                 for face_idx in range(len(faces))]
    else:
        colors = ['lightblue'] * len(faces)
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='lightblue',
        opacity=0.8,
        name='D6'
    )

def create_icosahedron_mesh(result=None):
    # 二十面体顶点（黄金比例）
    phi = (1 + np.sqrt(5)) / 2
    vertices = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
    ]) / np.sqrt(1 + phi**2)
    
    # 简化的面定义
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='gold',
        opacity=0.8,
        name='D20'
    )

def create_tetrahedron_mesh(result=None):
    # 四面体顶点
    vertices = np.array([
        [1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]
    ])
    
    faces = [
        [0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='green',
        opacity=0.8,
        name='D4'
    )

def create_octahedron_mesh(result=None):
    # 八面体顶点
    vertices = np.array([
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
    ])
    
    faces = [
        [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
        [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='purple',
        opacity=0.8,
        name='D8'
    )

def create_dodecahedron_mesh(result=None):
    # 十二面体顶点（简化版本）
    phi = (1 + np.sqrt(5)) / 2
    vertices = np.array([
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        [0, phi, 1/phi], [0, phi, -1/phi], [0, -phi, 1/phi], [0, -phi, -1/phi],
        [1/phi, 0, phi], [-1/phi, 0, phi], [1/phi, 0, -phi], [-1/phi, 0, -phi],
        [phi, 1/phi, 0], [phi, -1/phi, 0], [-phi, 1/phi, 0], [-phi, -1/phi, 0]
    ])
    
    # 简化的面定义（使用三角形近似）
    faces = [
        [0, 8, 9], [0, 9, 1], [1, 9, 14], [1, 14, 3],
        [2, 10, 12], [2, 12, 0], [3, 11, 7], [4, 13, 6],
        [5, 15, 18], [6, 19, 10], [7, 15, 19], [8, 4, 18]
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='orange',
        opacity=0.8,
        name='D12'
    )

def create_pentagonal_trapezohedron_mesh(result=None):
    # D10 (五角双锥)
    vertices = np.array([
        [0, 0, 1.5],  # 顶点
        [0, 0, -1.5], # 底点
        [1, 0, 0], [0.309, 0.951, 0], [-0.809, 0.588, 0],
        [-0.809, -0.588, 0], [0.309, -0.951, 0]
    ])
    
    faces = [
        [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 6], [0, 6, 2],
        [1, 3, 2], [1, 4, 3], [1, 5, 4], [1, 6, 5], [1, 2, 6]
    ]
    
    x, y, z = vertices.T
    i, j, k = np.array(faces).T
    
    return go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='red',
        opacity=0.8,
        name='D10'
    )

def create_rolling_animation(dice_mesh, frames=30):
    """创建骰子滚动动画"""
    angles = np.linspace(0, 4*pi, frames)
    
    animated_frames = []
    for angle in angles:
        # 旋转矩阵
        cos_a, sin_a = cos(angle), sin(angle)
        cos_b, sin_b = cos(angle*0.7), sin(angle*0.7)
        
        # 应用旋转
        rotated_mesh = go.Mesh3d(
            x=dice_mesh.x * cos_a - dice_mesh.y * sin_a,
            y=dice_mesh.x * sin_a + dice_mesh.y * cos_a,
            z=dice_mesh.z * cos_b + (dice_mesh.x * cos_a - dice_mesh.y * sin_a) * sin_b,
            i=dice_mesh.i,
            j=dice_mesh.j,
            k=dice_mesh.k,
            color=dice_mesh.color,
            opacity=dice_mesh.opacity,
            name=dice_mesh.name
        )
        animated_frames.append(rotated_mesh)
    
    return animated_frames

def main():
    st.title("🎲 DND 骰子系统")
    st.markdown("欢迎使用带有3D动画的DND骰子系统！")
    
    # 侧边栏控制
    st.sidebar.header("骰子控制")
    
    # 骰子类型选择
    dice_types = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
    selected_dice = st.sidebar.selectbox("选择骰子类型", dice_types, index=1)
    
    # 骰子数量
    num_dice = st.sidebar.slider("骰子数量", 1, 10, 1)
    
    # 修正值
    modifier = st.sidebar.number_input("修正值", value=0, step=1)
    
    # 动画设置
    show_animation = st.sidebar.checkbox("显示投掷动画", value=True)
    
    # 主要布局
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("3D 骰子可视化")
        
        # 创建占位符用于动画
        plot_placeholder = st.empty()
        
        # 初始显示静态骰子
        dice_mesh = create_dice_mesh(selected_dice)
        
        fig = go.Figure(data=[dice_mesh])
        fig.update_layout(
            scene=dict(
                xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                zaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                bgcolor='black',
                camera=dict(eye=dict(x=2, y=2, z=2))
            ),
            title=f"{selected_dice.upper()} 骰子",
            showlegend=False,
            margin=dict(l=0, r=0, t=50, b=0),
            height=500
        )
        
        plot_placeholder.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("投掷结果")
        
        # 投掷按钮
        if st.button("🎲 投掷骰子!", type="primary", use_container_width=True):
            # 投掷结果
            results = []
            total = 0
            
            for i in range(num_dice):
                dice = Dice3D(selected_dice)
                result = dice.roll()
                results.append(result)
                total += result
            
            if show_animation:
                # 显示投掷状态
                with st.spinner("投掷中..."):
                    # 简化动画效果，减少闪烁
                    for i in range(3):  # 减少动画帧数
                        # 创建旋转效果
                        angle = i * pi / 3
                        dice_mesh = create_dice_mesh(selected_dice)
                        
                        # 简单旋转变换
                        rotated_x = [x * cos(angle) - y * sin(angle) for x, y in zip(dice_mesh.x, dice_mesh.y)]
                        rotated_y = [x * sin(angle) + y * cos(angle) for x, y in zip(dice_mesh.x, dice_mesh.y)]
                        
                        # 创建临时网格对象
                        temp_mesh = go.Mesh3d(
                            x=rotated_x,
                            y=rotated_y,
                            z=dice_mesh.z,
                            i=dice_mesh.i,
                            j=dice_mesh.j,
                            k=dice_mesh.k,
                            color=dice_mesh.color,
                            opacity=0.7,
                            name=dice_mesh.name
                        )
                        
                        fig = go.Figure(data=[temp_mesh])
                        fig.update_layout(
                            scene=dict(
                                xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                                zaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                                bgcolor='black',
                                camera=dict(eye=dict(x=2, y=2, z=2))
                            ),
                            title=f"{selected_dice.upper()} 骰子 - 投掷中...",
                            showlegend=False,
                            margin=dict(l=0, r=0, t=50, b=0),
                            height=500
                        )
                        plot_placeholder.plotly_chart(fig, use_container_width=True, key=f"rolling_{i}")
                        time.sleep(0.3)  # 增加延迟减少闪烁
            
            # 显示最终结果的骰子
            final_dice_mesh = create_dice_mesh(selected_dice, results[0] if num_dice == 1 else None)
            fig = go.Figure(data=[final_dice_mesh])
            fig.update_layout(
                scene=dict(
                    xaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                    zaxis=dict(range=[-3, 3], showgrid=False, zeroline=False, showticklabels=False),
                    bgcolor='black',
                    camera=dict(eye=dict(x=2, y=2, z=2))
                ),
                title=f"{selected_dice.upper()} 骰子 - 结果: {results[0] if num_dice == 1 else '多个骰子'}",
                showlegend=False,
                margin=dict(l=0, r=0, t=50, b=0),
                height=500
            )
            plot_placeholder.plotly_chart(fig, use_container_width=True)
            
            # 显示投掷结果
            st.success("投掷完成！")
            
            if num_dice == 1:
                st.metric("骰子结果", f"{results[0]}")
                if modifier != 0:
                    final_result = results[0] + modifier
                    st.metric("最终结果", f"{final_result}", f"修正值: {modifier:+d}")
            else:
                st.write("**各骰子结果:**")
                for i, result in enumerate(results, 1):
                    st.write(f"骰子 {i}: {result}")
                
                st.metric("总和", f"{total}")
                if modifier != 0:
                    final_result = total + modifier
                    st.metric("最终结果", f"{final_result}", f"修正值: {modifier:+d}")
            
            # 存储到会话状态
            if 'roll_history' not in st.session_state:
                st.session_state.roll_history = []
            
            st.session_state.roll_history.append({
                'dice_type': selected_dice,
                'num_dice': num_dice,
                'results': results,
                'total': total,
                'modifier': modifier,
                'final_result': (total + modifier) if modifier != 0 else total
            })
    
    # 投掷历史
    st.subheader("投掷历史")
    if 'roll_history' in st.session_state and st.session_state.roll_history:
        history_df = []
        for i, roll in enumerate(reversed(st.session_state.roll_history[-10:]), 1):  # 显示最近10次
            history_df.append({
                '序号': i,
                '骰子': roll['dice_type'].upper(),
                '数量': roll['num_dice'],
                '结果': ', '.join(map(str, roll['results'])),
                '总和': roll['total'],
                '修正值': roll['modifier'],
                '最终结果': roll['final_result']
            })
        
        st.dataframe(history_df, use_container_width=True)
        
        if st.button("清空历史"):
            st.session_state.roll_history = []
            st.rerun()
    else:
        st.info("还没有投掷记录")
    
    # 快捷投掷按钮
    st.subheader("快捷投掷")
    quick_rolls = st.columns(6)
    
    quick_dice_types = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
    for i, dice_type in enumerate(quick_dice_types):
        with quick_rolls[i]:
            if st.button(f"🎲 {dice_type.upper()}", key=f"quick_{dice_type}"):
                dice = Dice3D(dice_type)
                result = dice.roll()
                
                # 存储到会话状态
                if 'roll_history' not in st.session_state:
                    st.session_state.roll_history = []
                
                st.session_state.roll_history.append({
                    'dice_type': dice_type,
                    'num_dice': 1,
                    'results': [result],
                    'total': result,
                    'modifier': 0,
                    'final_result': result
                })
                
                st.success(f"{dice_type.upper()}: {result}")
                st.rerun()  # 刷新页面显示最新历史记录

if __name__ == "__main__":
    main()
