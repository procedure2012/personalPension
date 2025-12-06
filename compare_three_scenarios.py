import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


def calculate_scenario_a(r1=0.25, m1=12000, a1=10, r2=0.10, m2=4000, a2=24, b1=0.0345, b2=0.018):
    """
    计算方案A：分段缴存个人养老金

    参数:
        r1: 前a1年税率
        m1: 前a1年每年缴存金额
        a1: 前期缴存年数
        r2: 后a2年税率
        m2: 后a2年每年缴存金额
        a2: 后期年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
    """
    # 前a1年养老金本息（到退休时）
    V1 = m1 * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1)

    # 后a2年养老金本息（到退休时）
    V2 = m2 * ((1 + b1) ** 1) * (((1 + b1) ** a2 - 1) / b1)

    # 养老金总额扣除3%税
    V_pension = (V1 + V2) * 0.97

    # 前a1年退税投资收益（每年退税m1*r1）
    tax_refund1 = m1 * r1
    V3 = tax_refund1 * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)

    # 后a2年退税投资收益（每年退税m2*r2）
    tax_refund2 = m2 * r2
    V4 = tax_refund2 * ((1 + b2) ** 1) * (((1 + b2) ** a2 - 1) / b2)

    # 总收益
    V_A = V_pension + V3 + V4

    print(f"方案A详细计算:")
    print(f"  前{a1}年养老金本息(税前): {V1:,.2f} 元")
    print(f"  后{a2}年养老金本息(税前): {V2:,.2f} 元")
    print(f"  养老金总额(扣3%税后): {V_pension:,.2f} 元")
    print(f"  前{a1}年退税收益: {V3:,.2f} 元")
    print(f"  后{a2}年退税收益: {V4:,.2f} 元")
    print(f"  方案A总收益: {V_A:,.2f} 元")

    return V_A


def calculate_scenario_b(r1=0.25, m1=12000, a1=10, m2=4000, a2=24, b1=0.0345, b2=0.018, stock_rate=0.04):
    """
    计算方案B：前期养老金 + 后期股票

    参数:
        r1: 前a1年税率
        m1: 前a1年每年缴存金额
        a1: 前期缴存年数
        m2: 后a2年每年投资金额
        a2: 后期年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
        stock_rate: 股票年化收益率
    """
    # 前a1年养老金本息（到退休时，扣除3%税）
    V1 = m1 * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1) * 0.97

    # 前a1年退税投资收益（每年退税m1*r1）
    tax_refund1 = m1 * r1
    V3 = tax_refund1 * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)

    # 后a2年股票投资收益
    V5 = m2 * ((1 + stock_rate) ** 1) * (((1 + stock_rate) ** a2 - 1) / stock_rate)

    # 总收益
    V_B = V1 + V3 + V5

    print(f"\n方案B详细计算:")
    print(f"  前{a1}年养老金本息(扣3%税后): {V1:,.2f} 元")
    print(f"  前{a1}年退税收益: {V3:,.2f} 元")
    print(f"  后{a2}年股票收益: {V5:,.2f} 元")
    print(f"  方案B总收益: {V_B:,.2f} 元")

    return V_B


def calculate_scenario_c(m1=12000, a1=10, m2=4000, a2=24, stock_rate=0.04):
    """
    计算方案C：全程股票投资

    参数:
        m1: 前a1年每年投资金额
        a1: 前期年数
        m2: 后a2年每年投资金额
        a2: 后期年数
        stock_rate: 股票年化收益率
    """
    # 前a1年股票投资收益（到退休时）
    V6 = m1 * ((1 + stock_rate) ** (a2 + 1)) * (((1 + stock_rate) ** a1 - 1) / stock_rate)

    # 后a2年股票投资收益
    V7 = m2 * ((1 + stock_rate) ** 1) * (((1 + stock_rate) ** a2 - 1) / stock_rate)

    # 总收益
    V_C = V6 + V7

    print(f"\n方案C详细计算:")
    print(f"  前{a1}年股票收益: {V6:,.2f} 元")
    print(f"  后{a2}年股票收益: {V7:,.2f} 元")
    print(f"  方案C总收益: {V_C:,.2f} 元")

    return V_C


def calculate_equivalent_yield(total_value, m1=12000, a1=10, m2=4000, a2=24):
    """
    计算等价年化收益率

    参数:
        total_value: 实际总收益
        m1: 前a1年每年投资金额
        a1: 前期年数
        m2: 后a2年每年投资金额
        a2: 后期年数
    """
    def equation(y):
        if y <= 0:
            return 1e10
        # 前a1年的终值 + 后a2年的终值
        fv = (m1 * ((1 + y) ** (a2 + 1)) * (((1 + y) ** a1 - 1) / y) +
              m2 * ((1 + y) ** 1) * (((1 + y) ** a2 - 1) / y))
        return fv - total_value

    # 使用4%作为初始猜测
    solution = fsolve(equation, 0.04)
    return solution[0]


def calculate_scenario_a_variable(a1_var, r1=0.25, m1=12000, r2=0.10, m2=4000, total_years=34, b1=0.0345, b2=0.018):
    """
    计算方案A在不同a1下的收益

    参数:
        a1_var: 前期缴存年数（变量）
        r1: 前期税率
        m1: 前期每年缴存金额
        r2: 后期税率
        m2: 后期每年缴存金额
        total_years: 总年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
    """
    a2_var = total_years - a1_var

    if a1_var <= 0 or a2_var <= 0:
        return 0

    # 前a1年养老金本息（到退休时）
    V1 = m1 * ((1 + b1) ** (a2_var + 1)) * (((1 + b1) ** a1_var - 1) / b1)

    # 后a2年养老金本息（到退休时）
    V2 = m2 * ((1 + b1) ** 1) * (((1 + b1) ** a2_var - 1) / b1)

    # 养老金总额扣除3%税
    V_pension = (V1 + V2) * 0.97

    # 前a1年退税投资收益
    tax_refund1 = m1 * r1
    V3 = tax_refund1 * ((1 + b2) ** (a2_var + 1)) * (((1 + b2) ** a1_var - 1) / b2)

    # 后a2年退税投资收益
    tax_refund2 = m2 * r2
    V4 = tax_refund2 * ((1 + b2) ** 1) * (((1 + b2) ** a2_var - 1) / b2)

    # 总收益
    V_A = V_pension + V3 + V4

    return V_A


def plot_comparison(r1=0.25, m1=12000, a1=10, r2=0.10, m2=4000, a2=24,
                   b1=0.0345, b2=0.018, stock_rate=0.04):
    """
    绘制三种方案的对比图

    参数:
        r1: 前期税率
        m1: 前期每年缴存金额
        a1: 前期年数
        r2: 后期税率
        m2: 后期每年缴存金额
        a2: 后期年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
        stock_rate: 股票年化收益率
    """
    total_years = a1 + a2

    # 计算三种固定方案的收益
    V_A = calculate_scenario_a(r1, m1, a1, r2, m2, a2, b1, b2)
    V_B = calculate_scenario_b(r1, m1, a1, m2, a2, b1, b2, stock_rate)
    V_C = calculate_scenario_c(m1, a1, m2, a2, stock_rate)

    # 计算等价年化收益率
    y_A = calculate_equivalent_yield(V_A, m1, a1, m2, a2)
    y_B = calculate_equivalent_yield(V_B, m1, a1, m2, a2)
    y_C = calculate_equivalent_yield(V_C, m1, a1, m2, a2)

    print(f"\n等价年化收益率:")
    print(f"  方案A: {y_A * 100:.4f}%")
    print(f"  方案B: {y_B * 100:.4f}%")
    print(f"  方案C: {y_C * 100:.4f}%")

    # 计算方案A在不同a1下的收益率
    a1_values = range(1, total_years)
    y_A_variable = []

    print(f"\n计算方案A在不同a1下的等价年化收益率:")
    for a1_var in a1_values:
        V = calculate_scenario_a_variable(a1_var, r1, m1, r2, m2, total_years, b1, b2)
        y = calculate_equivalent_yield(V, m1, a1_var, m2, total_years - a1_var)
        y_A_variable.append(y * 100)
        if a1_var % 5 == 0 or a1_var == a1:
            print(f"  a1={a1_var}: y={y * 100:.4f}%")

    # 绘图
    plt.figure(figsize=(14, 8))

    # 绘制方案A的曲线（a1变化）
    plt.plot(a1_values, y_A_variable,
             linewidth=2.5, color='#2E86AB', marker='o', markersize=5,
             label=f'方案A (前a1年{m1}元r={r1*100:.0f}%，后年{m2}元r={r2*100:.0f}%)')

    # 标记指定a1的点
    if a1 - 1 < len(y_A_variable):
        plt.plot(a1, y_A_variable[a1 - 1],
                'r*', markersize=20,
                label=f'方案A(a1={a1}): {y_A * 100:.4f}%',
                zorder=5)

    # 绘制方案B和C的水平线
    plt.axhline(y=y_B * 100, color='#A23B72', linestyle='--', linewidth=2,
                alpha=0.8, label=f'方案B (前{a1}年养老金+后{a2}年股票): {y_B * 100:.4f}%')
    plt.axhline(y=y_C * 100, color='#F18F01', linestyle='--', linewidth=2,
                alpha=0.8, label=f'方案C (全程股票): {y_C * 100:.4f}%')

    # 标注部分数据点
    for i, a1_var in enumerate(a1_values):
        if i % 5 == 0 or a1_var == a1:
            plt.annotate(f'{y_A_variable[i]:.3f}%',
                        xy=(a1_var, y_A_variable[i]),
                        xytext=(0, 8),
                        textcoords='offset points',
                        fontsize=7,
                        ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat',
                                alpha=0.6, edgecolor='none'))

    # 设置标签和标题
    plt.xlabel('方案A前期缴存年数 a1 (年)', fontsize=12, fontweight='bold')
    plt.ylabel('等价年化收益率 y (%)', fontsize=12, fontweight='bold')
    plt.title('三种投资方案的等价年化收益率对比\n' +
              f'(总投入均为前{a1}年{m1}元/年 + 后{a2}年{m2}元/年)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, total_years + 1)
    y_min = min(min(y_A_variable), y_B * 100, y_C * 100) - 0.1
    y_max = max(max(y_A_variable), y_B * 100, y_C * 100) + 0.1
    plt.ylim(y_min, y_max)

    # 添加说明文字
    note_text = (f"方案A: 分段养老金 (前期r={r1*100:.0f}%，后期r={r2*100:.0f}%)\n"
                 f"方案B: 混合投资 (前期养老金，后期股票{stock_rate*100:.0f}%)\n"
                 f"方案C: 纯股票投资 (全程{stock_rate*100:.0f}%年化)")
    plt.text(0.98, 0.02, note_text,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\comparison_three_scenarios.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n对比图已保存到: {output_path}")

    # 显示图片
    plt.show()

    return y_A, y_B, y_C


def plot_all_scenarios_vs_a1(r1=0.25, m1=12000, r2=0.10, m2=4000, total_years=34,
                              b1=0.0345, b2=0.018, stock_rate=0.04):
    """
    绘制三种方案都以a1为横轴的对比图

    参数:
        r1: 前期税率
        m1: 前期每年缴存金额
        r2: 后期税率
        m2: 后期每年缴存金额
        total_years: 总年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
        stock_rate: 股票年化收益率
    """
    a1_values = range(1, total_years)
    y_A_values = []
    y_B_values = []
    y_C_values = []

    print(f"\n计算三种方案在不同a1下的等价年化收益率:")
    print(f"{'a1':<5} {'方案A':<12} {'方案B':<12} {'方案C':<12}")
    print("-" * 45)

    for a1 in a1_values:
        a2 = total_years - a1

        # 方案A: 全程养老金
        V_A = calculate_scenario_a_variable(a1, r1, m1, r2, m2, total_years, b1, b2)
        y_A = calculate_equivalent_yield(V_A, m1, a1, m2, a2)
        y_A_values.append(y_A * 100)

        # 方案B: 前a1年养老金，后a2年股票
        V1_B = m1 * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1) * 0.97
        V3_B = m1 * r1 * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)
        V5_B = m2 * ((1 + stock_rate) ** 1) * (((1 + stock_rate) ** a2 - 1) / stock_rate)
        V_B = V1_B + V3_B + V5_B
        y_B = calculate_equivalent_yield(V_B, m1, a1, m2, a2)
        y_B_values.append(y_B * 100)

        # 方案C: 全程股票
        V6_C = m1 * ((1 + stock_rate) ** (a2 + 1)) * (((1 + stock_rate) ** a1 - 1) / stock_rate)
        V7_C = m2 * ((1 + stock_rate) ** 1) * (((1 + stock_rate) ** a2 - 1) / stock_rate)
        V_C = V6_C + V7_C
        y_C = calculate_equivalent_yield(V_C, m1, a1, m2, a2)
        y_C_values.append(y_C * 100)

        if a1 % 5 == 0:
            print(f"{a1:<5} {y_A*100:>10.4f}%  {y_B*100:>10.4f}%  {y_C*100:>10.4f}%")

    # 绘图
    plt.figure(figsize=(14, 8))

    # 三条曲线
    plt.plot(a1_values, y_A_values,
             linewidth=2.5, color='#2E86AB', marker='o', markersize=4,
             label=f'方案A: 全程养老金 (r1={r1*100:.0f}%, r2={r2*100:.0f}%)')

    plt.plot(a1_values, y_B_values,
             linewidth=2.5, color='#A23B72', marker='s', markersize=4,
             label=f'方案B: 前a1年养老金 + 后年股票{stock_rate*100:.0f}%')

    plt.plot(a1_values, y_C_values,
             linewidth=2.5, color='#F18F01', marker='d', markersize=4,
             label=f'方案C: 全程股票{stock_rate*100:.0f}%')

    # 标注a1=10的点
    if 10 - 1 < len(y_A_values):
        plt.plot(10, y_A_values[9], 'r*', markersize=15, zorder=5)
        plt.plot(10, y_B_values[9], 'r*', markersize=15, zorder=5)
        plt.plot(10, y_C_values[9], 'r*', markersize=15, zorder=5)

    # 设置标签和标题
    plt.xlabel('前期年数 a1 (年)', fontsize=12, fontweight='bold')
    plt.ylabel('等价年化收益率 y (%)', fontsize=12, fontweight='bold')
    plt.title('三种投资方案的等价年化收益率对比\n' +
              f'(前a1年{m1}元/年，后(34-a1)年{m2}元/年)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, total_years + 1)
    all_y = y_A_values + y_B_values + y_C_values
    y_min = min(all_y) - 0.1
    y_max = max(all_y) + 0.1
    plt.ylim(y_min, y_max)

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\comparison_all_vs_a1.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图片已保存到: {output_path}")

    plt.show()


def plot_scenarios_vs_stock_rate(r1=0.25, m1=12000, a1=10, r2=0.10, m2=4000, a2=24,
                                  b1=0.0345, b2=0.018):
    """
    固定a1=10，绘制不同股票年化收益率下三种方案的对比

    参数:
        r1: 前期税率
        m1: 前期每年缴存金额
        a1: 前期年数（固定为10）
        r2: 后期税率
        m2: 后期每年缴存金额
        a2: 后期年数
        b1: 养老金产品年化收益率
        b2: 其他理财产品年化收益率
    """
    # 股票年化收益率范围：1%到8%
    stock_rates = np.linspace(0.01, 0.08, 30)
    y_A_values = []  # 方案A不变
    y_B_values = []
    y_C_values = []

    print(f"\n计算三种方案在不同股票年化下的等价年化收益率 (a1={a1}):")
    print(f"{'股票年化':<12} {'方案A':<12} {'方案B':<12} {'方案C':<12}")
    print("-" * 50)

    # 方案A收益（不依赖股票年化）
    V_A = calculate_scenario_a(r1, m1, a1, r2, m2, a2, b1, b2)
    y_A_fixed = calculate_equivalent_yield(V_A, m1, a1, m2, a2)

    for stock_rate in stock_rates:
        # 方案A: 全程养老金（不变）
        y_A_values.append(y_A_fixed * 100)

        # 方案B: 前a1年养老金，后a2年股票
        V_B = calculate_scenario_b(r1, m1, a1, m2, a2, b1, b2, stock_rate)
        y_B = calculate_equivalent_yield(V_B, m1, a1, m2, a2)
        y_B_values.append(y_B * 100)

        # 方案C: 全程股票
        V_C = calculate_scenario_c(m1, a1, m2, a2, stock_rate)
        y_C = calculate_equivalent_yield(V_C, m1, a1, m2, a2)
        y_C_values.append(y_C * 100)

    # 打印部分结果
    for i, stock_rate in enumerate(stock_rates):
        if i % 5 == 0 or abs(stock_rate - 0.04) < 0.001:
            print(f"{stock_rate*100:>10.2f}%  {y_A_values[i]:>10.4f}%  {y_B_values[i]:>10.4f}%  {y_C_values[i]:>10.4f}%")

    # 绘图
    plt.figure(figsize=(14, 8))

    stock_rates_percent = stock_rates * 100

    # 三条曲线
    plt.plot(stock_rates_percent, y_A_values,
             linewidth=2.5, color='#2E86AB', marker='o', markersize=4,
             label=f'方案A: 全程养老金 (固定，不受股票影响)')

    plt.plot(stock_rates_percent, y_B_values,
             linewidth=2.5, color='#A23B72', marker='s', markersize=4,
             label=f'方案B: 前{a1}年养老金 + 后{a2}年股票')

    plt.plot(stock_rates_percent, y_C_values,
             linewidth=2.5, color='#F18F01', marker='d', markersize=4,
             label=f'方案C: 全程股票')

    # 标注4%的点
    idx_4 = np.argmin(np.abs(stock_rates - 0.04))
    plt.plot(4, y_A_values[idx_4], 'r*', markersize=15, zorder=5)
    plt.plot(4, y_B_values[idx_4], 'r*', markersize=15, zorder=5)
    plt.plot(4, y_C_values[idx_4], 'r*', markersize=15, zorder=5)

    # 添加标注
    plt.annotate(f'股票4%时\nA:{y_A_values[idx_4]:.3f}%\nB:{y_B_values[idx_4]:.3f}%\nC:{y_C_values[idx_4]:.3f}%',
                xy=(4, y_B_values[idx_4]),
                xytext=(5, y_B_values[idx_4] + 0.3),
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='red', lw=1))

    # 设置标签和标题
    plt.xlabel('股票年化收益率 (%)', fontsize=12, fontweight='bold')
    plt.ylabel('等价年化收益率 y (%)', fontsize=12, fontweight='bold')
    plt.title(f'不同股票收益率下的三种方案对比 (固定a1={a1}年)\n' +
              f'(前{a1}年{m1}元/年，后{a2}年{m2}元/年)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(1, 8)
    all_y = y_A_values + y_B_values + y_C_values
    y_min = min(all_y) - 0.2
    y_max = max(all_y) + 0.2
    plt.ylim(y_min, y_max)

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\comparison_vs_stock_rate.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图片已保存到: {output_path}")

    plt.show()


if __name__ == '__main__':
    print("=" * 70)
    print("三种投资方案的等价年化收益率对比")
    print("=" * 70)
    print()

    # 默认参数（可以修改这些参数）
    params = {
        'r1': 0.25,        # 前期税率25%
        'm1': 12000,       # 前期每年缴存12000元
        'a1': 10,          # 前期10年
        'r2': 0.10,        # 后期税率10%
        'm2': 4000,        # 后期每年缴存4000元
        'a2': 24,          # 后期24年
        'b1': 0.0345,      # 养老金产品年化3.45%
        'b2': 0.018,       # 其他理财年化1.8%
        'stock_rate': 0.04 # 股票年化4%
    }

    print("使用参数:")
    print(f"  前期税率 r1 = {params['r1']*100:.0f}%")
    print(f"  前期缴存 m1 = {params['m1']} 元/年")
    print(f"  前期年数 a1 = {params['a1']} 年")
    print(f"  后期税率 r2 = {params['r2']*100:.0f}%")
    print(f"  后期缴存 m2 = {params['m2']} 元/年")
    print(f"  后期年数 a2 = {params['a2']} 年")
    print(f"  养老金年化 b1 = {params['b1']*100:.2f}%")
    print(f"  其他理财年化 b2 = {params['b2']*100:.2f}%")
    print(f"  股票年化 = {params['stock_rate']*100:.0f}%")
    print()

    y_A, y_B, y_C = plot_comparison(**params)

    print("\n" + "=" * 70)
    print("结论:")
    print("=" * 70)

    if y_A > y_B and y_A > y_C:
        print(f"方案A最优，等价年化收益率为 {y_A * 100:.4f}%")
    elif y_B > y_A and y_B > y_C:
        print(f"方案B最优，等价年化收益率为 {y_B * 100:.4f}%")
    else:
        print(f"方案C最优，等价年化收益率为 {y_C * 100:.4f}%")

    print(f"\n收益率排名:")
    scenarios = [('方案A', y_A), ('方案B', y_B), ('方案C', y_C)]
    scenarios_sorted = sorted(scenarios, key=lambda x: x[1], reverse=True)
    for i, (name, rate) in enumerate(scenarios_sorted, 1):
        print(f"  {i}. {name}: {rate * 100:.4f}%")

    # 生成新的对比图
    print("\n" + "=" * 70)
    print("生成额外的对比分析图表")
    print("=" * 70)

    # 图1: 所有方案以a1为横轴
    print("\n生成图表1: 三种方案随a1变化的对比图...")
    plot_all_scenarios_vs_a1(
        r1=params['r1'],
        m1=params['m1'],
        r2=params['r2'],
        m2=params['m2'],
        total_years=params['a1'] + params['a2'],
        b1=params['b1'],
        b2=params['b2'],
        stock_rate=params['stock_rate']
    )

    # 图2: 固定a1=10，股票收益率为横轴
    print("\n生成图表2: 不同股票收益率下的三种方案对比图...")
    plot_scenarios_vs_stock_rate(
        r1=params['r1'],
        m1=params['m1'],
        a1=params['a1'],
        r2=params['r2'],
        m2=params['m2'],
        a2=params['a2'],
        b1=params['b1'],
        b2=params['b2']
    )
