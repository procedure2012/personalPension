import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False


def calculate_equivalent_yield(r, m, a1, a2, b1, b2):
    """
    计算个人养老金的等价年化收益率y

    参数:
        r (float): 当前税率
        m (float): 每年缴存总数 (元)
        a1 (int): 缴存年数
        a2 (int): 缴存a1年后，距离退休的年数
        b1 (float): 个人养老金理财产品年化收益率
        b2 (float): 其他理财产品年化收益率

    返回:
        float: 等价年化收益率y
    """

    def equation(y):
        """
        求解超越方程
        """
        if y <= 0:
            return 1e10  # 返回一个大数，避免无效解

        left_side = ((1 + y) ** (a2 + 1)) * (((1 + y) ** a1 - 1) / y)

        right_term1 = 0.97 * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1)
        right_term2 = r * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)
        right_side = right_term1 + right_term2

        return left_side - right_side

    # 使用b1作为初始猜测值
    initial_guess = b1

    try:
        # 求解方程
        solution = fsolve(equation, initial_guess, full_output=True)
        if solution[2] == 1:  # 求解成功
            return solution[0][0]
        else:
            # 如果求解失败，尝试其他初始值
            initial_guess = (b1 + b2) / 2
            solution = fsolve(equation, initial_guess)
            return solution[0]
    except:
        return np.nan


def plot_yield_vs_years():
    """
    绘制缴存年数a1与等价年化收益率y的关系图
    """
    # 固定参数
    r = 0.25      # 税率25%
    m = 12000     # 每年缴存12000元
    b1 = 0.034    # 养老金产品年化3.4%
    b2 = 0.02     # 其他理财产品年化2%
    total_years = 33  # 总共33年（30岁到63岁）

    # 计算不同a1值对应的y
    a1_values = range(1, total_years + 1)
    y_values = []

    print("计算中...")
    print(f"{'a1 (缴存年数)':<15} {'a2 (距退休)':<15} {'y (等价年化)':<20}")
    print("-" * 50)

    for a1 in a1_values:
        a2 = total_years - a1
        y = calculate_equivalent_yield(r, m, a1, a2, b1, b2)
        y_values.append(y)
        print(f"{a1:<15} {a2:<15} {y*100:.4f}%")

    # 找到最优缴存年数
    y_values_array = np.array(y_values)
    max_idx = np.argmax(y_values_array)
    optimal_a1 = a1_values[max_idx]
    optimal_y = y_values[max_idx]

    print(f"\n最优缴存年数: {optimal_a1} 年")
    print(f"最大等价年化: {optimal_y*100:.4f}%")

    # 绘图
    plt.figure(figsize=(14, 8))

    # 主曲线
    y_values_percent = [y * 100 for y in y_values]
    plt.plot(a1_values, y_values_percent,
             linewidth=2.5, color='#2E86AB', marker='o', markersize=5,
             label=f'等价年化收益率 y')

    # 标记每个点的数值
    for i, (a1, y_pct) in enumerate(zip(a1_values, y_values_percent)):
        # 每隔2个点标注一次，避免过于密集
        if i % 2 == 0 or a1 == optimal_a1:
            plt.annotate(f'{y_pct:.3f}%',
                        xy=(a1, y_pct),
                        xytext=(0, 8),
                        textcoords='offset points',
                        fontsize=7,
                        ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat',
                                alpha=0.6, edgecolor='none'))

    # 标记最优点
    plt.plot(optimal_a1, optimal_y * 100,
             'r*', markersize=20, label=f'最优点: a1={optimal_a1}年, y={optimal_y*100:.4f}%',
             zorder=5)

    # 添加参考线：b1和b2
    plt.axhline(y=b1 * 100, color='green', linestyle='--', linewidth=1.5,
                alpha=0.7, label=f'养老金产品年化 b1 = {b1*100:.1f}%')
    plt.axhline(y=b2 * 100, color='orange', linestyle='--', linewidth=1.5,
                alpha=0.7, label=f'其他理财年化 b2 = {b2*100:.1f}%')

    # 设置标签和标题
    plt.xlabel('缴存年数 a1 (年)', fontsize=12, fontweight='bold')
    plt.ylabel('等价年化收益率 y (%)', fontsize=12, fontweight='bold')
    plt.title('个人养老金等价年化收益率与缴存年数的关系\n' +
              f'(税率r={r*100:.0f}%, m={m}元, b1={b1*100:.1f}%, b2={b2*100:.1f}%)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, total_years + 1)
    y_min = min(min(y_values) * 100, b2 * 100) - 0.2
    y_max = max(max(y_values) * 100, b1 * 100) + 0.3
    plt.ylim(y_min, y_max)

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\pension_yield_vs_years.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n图片已保存到: {output_path}")

    # 显示图片
    plt.show()

    return a1_values, y_values, optimal_a1, optimal_y


def plot_yield_diff_vs_years(a1_values, y_values):
    """
    绘制缴存年数a1与收益率差值(y-b1)的关系图，并标注每个点的y-b1值
    """
    # 固定参数
    r = 0.25      # 税率25%
    m = 12000     # 每年缴存12000元
    b1 = 0.034    # 养老金产品年化3.4%
    b2 = 0.02     # 其他理财产品年化2%
    total_years = 33  # 总共33年（30岁到63岁）

    # 计算y-b1的差值
    diff_values = [(y - b1) * 100 for y in y_values]

    # 找到最大差值
    max_diff_idx = np.argmax(diff_values)
    optimal_a1_diff = a1_values[max_diff_idx]
    optimal_diff = diff_values[max_diff_idx]

    # 绘图
    plt.figure(figsize=(14, 8))

    # 主曲线
    plt.plot(a1_values, diff_values,
             linewidth=2.5, color='#A23B72', marker='s', markersize=5,
             label=f'收益率提升 (y - b1)')

    # 标记每个点的数值
    for i, (a1, diff) in enumerate(zip(a1_values, diff_values)):
        # 每隔2个点标注一次，避免过于密集
        if i % 2 == 0 or a1 == optimal_a1_diff:
            plt.annotate(f'{diff:.3f}%',
                        xy=(a1, diff),
                        xytext=(0, 8 if diff > 0 else -12),
                        textcoords='offset points',
                        fontsize=7,
                        ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat',
                                alpha=0.6, edgecolor='none'))

    # 标记最优点
    plt.plot(optimal_a1_diff, optimal_diff,
             'r*', markersize=20, label=f'最大提升: a1={optimal_a1_diff}年, 提升={optimal_diff:.4f}%',
             zorder=5)

    # 添加零线
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1,
                alpha=0.5, label='零线 (y = b1)')

    # 填充正值区域
    plt.fill_between(a1_values, 0, diff_values,
                     where=[d > 0 for d in diff_values],
                     alpha=0.2, color='green', label='有优势区域 (y > b1)')

    # 填充负值区域
    plt.fill_between(a1_values, 0, diff_values,
                     where=[d < 0 for d in diff_values],
                     alpha=0.2, color='red', label='无优势区域 (y < b1)')

    # 设置标签和标题
    plt.xlabel('缴存年数 a1 (年)', fontsize=12, fontweight='bold')
    plt.ylabel('收益率提升 y - b1 (%)', fontsize=12, fontweight='bold')
    plt.title('个人养老金相对产品本身的收益率提升\n' +
              f'(考虑退税优惠和3%提取税后的净提升)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, total_years + 1)
    diff_min = min(diff_values) - 0.1
    diff_max = max(diff_values) + 0.15
    plt.ylim(diff_min, diff_max)

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\pension_yield_diff_vs_years.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n第二张图片已保存到: {output_path}")

    # 显示图片
    plt.show()

    return diff_values, optimal_a1_diff, optimal_diff


def plot_yield_diff_growth_vs_years(a1_values, y_values):
    """
    绘制缴存年数a1与收益率提升增长速度的关系图
    增长速度 = d(y-b1)/da1，使用差分近似
    """
    # 固定参数
    b1 = 0.034    # 养老金产品年化3.4%
    total_years = 33  # 总共33年（30岁到63岁）

    # 计算y-b1的差值
    diff_values = [(y - b1) * 100 for y in y_values]

    # 计算增长速度（使用中心差分）
    growth_rates = []
    a1_list = list(a1_values)

    for i in range(len(diff_values)):
        if i == 0:
            # 第一个点使用前向差分
            growth = diff_values[i+1] - diff_values[i]
        elif i == len(diff_values) - 1:
            # 最后一个点使用后向差分
            growth = diff_values[i] - diff_values[i-1]
        else:
            # 中间点使用中心差分
            growth = (diff_values[i+1] - diff_values[i-1]) / 2
        growth_rates.append(growth)

    # 找到增长速度为0的点（拐点）
    zero_crossings = []
    for i in range(len(growth_rates) - 1):
        if growth_rates[i] * growth_rates[i+1] < 0:  # 符号改变
            zero_crossings.append(a1_list[i])

    # 绘图
    plt.figure(figsize=(14, 8))

    # 主曲线
    plt.plot(a1_values, growth_rates,
             linewidth=2.5, color='#F18F01', marker='d', markersize=5,
             label=f'收益率提升的增长速度 d(y-b1)/da1')

    # 标记每个点的数值
    for i, (a1, growth) in enumerate(zip(a1_values, growth_rates)):
        # 每隔3个点标注一次，避免过于密集
        if i % 3 == 0:
            plt.annotate(f'{growth:.4f}',
                        xy=(a1, growth),
                        xytext=(0, 8 if growth > 0 else -12),
                        textcoords='offset points',
                        fontsize=7,
                        ha='center',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue',
                                alpha=0.6, edgecolor='none'))

    # 添加零线
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1,
                alpha=0.5, label='零线 (增长速度为0)')

    # 标记拐点
    for zc in zero_crossings:
        plt.axvline(x=zc, color='red', linestyle='--', linewidth=1,
                   alpha=0.5)
        plt.annotate(f'拐点: a1≈{zc}',
                    xy=(zc, 0),
                    xytext=(5, 0.002),
                    fontsize=9,
                    color='red',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='pink', alpha=0.7))

    # 填充正值区域（边际收益递增）
    plt.fill_between(a1_values, 0, growth_rates,
                     where=[g > 0 for g in growth_rates],
                     alpha=0.2, color='blue', label='边际收益递增区域')

    # 填充负值区域（边际收益递减）
    plt.fill_between(a1_values, 0, growth_rates,
                     where=[g < 0 for g in growth_rates],
                     alpha=0.2, color='orange', label='边际收益递减区域')

    # 设置标签和标题
    plt.xlabel('缴存年数 a1 (年)', fontsize=12, fontweight='bold')
    plt.ylabel('增长速度 d(y-b1)/da1 (%/年)', fontsize=12, fontweight='bold')
    plt.title('个人养老金收益率提升的边际变化\n' +
              f'(每增加1年缴存，收益率提升(y-b1)的变化量)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, total_years + 1)
    growth_min = min(growth_rates) - 0.001
    growth_max = max(growth_rates) + 0.001
    plt.ylim(growth_min, growth_max)

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\pension_yield_diff_growth_vs_years.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n第三张图片已保存到: {output_path}")

    # 显示图片
    plt.show()

    return growth_rates, zero_crossings


def plot_yield_vs_tax_rate():
    """
    绘制不同税率r下，三种缴存年数(a1=10, 20, 33)的等价年化收益率y的关系
    """
    # 固定参数
    b1 = 0.034    # 养老金产品年化3.4%
    b2 = 0.02     # 其他理财产品年化2%
    total_years = 33  # 总共33年（30岁到63岁）

    # 税率和对应的缴存金额（根据文档142行的假设）
    tax_rates = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
    m_values = {
        0.03: 0,
        0.10: 4000,
        0.20: 8000,
        0.25: 12000,
        0.30: 12000,
        0.35: 12000,
        0.45: 12000
    }

    # 三种缴存年数
    a1_scenarios = [10, 20, 33]
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    markers = ['o', 's', 'd']

    # 绘图
    plt.figure(figsize=(14, 8))

    # 为每个a1场景绘制曲线
    for idx, a1 in enumerate(a1_scenarios):
        y_values = []
        a2 = total_years - a1

        print(f"\n计算 a1={a1} 年的情况:")
        print(f"{'税率r':<10} {'缴存金额m':<15} {'a2':<10} {'等价年化y':<20}")
        print("-" * 55)

        for r in tax_rates:
            m = m_values[r]
            if m == 0:
                # 如果不缴存，y为0
                y = 0
            else:
                y = calculate_equivalent_yield(r, m, a1, a2, b1, b2)
            y_values.append(y)
            print(f"{r*100:<10.0f}% {m:<15.0f} {a2:<10} {y*100:.4f}%")

        # 绘制曲线
        plt.plot([r * 100 for r in tax_rates], [y * 100 for y in y_values],
                linewidth=2.5, color=colors[idx], marker=markers[idx], markersize=8,
                label=f'a1={a1}年 (缴存{a1}年，持有{a2}年)')

        # 标记每个点的数值
        for i, (r, y) in enumerate(zip(tax_rates, y_values)):
            if i % 2 == 0 or m_values[r] == 0:  # 每隔一个点标注，以及m=0的点
                plt.annotate(f'{y*100:.3f}%',
                            xy=(r * 100, y * 100),
                            xytext=(0, 8),
                            textcoords='offset points',
                            fontsize=7,
                            ha='center',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat',
                                    alpha=0.6, edgecolor='none'))

    # 添加参考线：b1和b2
    plt.axhline(y=b1 * 100, color='green', linestyle='--', linewidth=1.5,
                alpha=0.7, label=f'养老金产品年化 b1 = {b1*100:.1f}%')
    plt.axhline(y=b2 * 100, color='orange', linestyle='--', linewidth=1.5,
                alpha=0.7, label=f'其他理财年化 b2 = {b2*100:.1f}%')

    # 设置标签和标题
    plt.xlabel('税率 r (%)', fontsize=12, fontweight='bold')
    plt.ylabel('等价年化收益率 y (%)', fontsize=12, fontweight='bold')
    plt.title('不同税率和缴存年数下的等价年化收益率\n' +
              f'(b1={b1*100:.1f}%, b2={b2*100:.1f}%)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, 50)
    plt.ylim(0, 5)

    # 添加说明文字
    note_text = "注: 税率3%时缴存金额m=0；税率10%时m=4000元；\n税率20%时m=8000元；税率≥25%时m=12000元"
    plt.text(0.02, 0.98, note_text,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\pension_yield_vs_tax_rate.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n第四张图片已保存到: {output_path}")

    # 显示图片
    plt.show()


def plot_yield_diff_growth_vs_tax_rate():
    """
    绘制税率r与收益率提升(y-b1)增长速度的关系图
    固定a1=10，计算d(y-b1)/dr
    """
    # 固定参数
    a1 = 10       # 缴存10年
    a2 = 23       # 距离退休23年（总共33年）
    b1 = 0.034    # 养老金产品年化3.4%
    b2 = 0.02     # 其他理财产品年化2%

    # 税率和对应的缴存金额
    tax_rates = [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]
    m_values = {
        0.03: 0,
        0.10: 4000,
        0.20: 8000,
        0.25: 12000,
        0.30: 12000,
        0.35: 12000,
        0.45: 12000
    }

    # 计算每个税率下的y值和y-b1
    y_values = []
    diff_values = []

    print(f"\n计算 a1={a1} 年，不同税率下的收益率:")
    print(f"{'税率r':<10} {'缴存金额m':<15} {'等价年化y':<20} {'y-b1':<15}")
    print("-" * 60)

    for r in tax_rates:
        m = m_values[r]
        if m == 0:
            y = 0
            diff = -b1
        else:
            y = calculate_equivalent_yield(r, m, a1, a2, b1, b2)
            diff = y - b1
        y_values.append(y)
        diff_values.append(diff * 100)  # 转换为百分点
        print(f"{r*100:<10.0f}% {m:<15.0f} {y*100:.4f}%          {diff*100:.4f}%")

    # 计算增长速度 d(y-b1)/dr（使用差分近似）
    growth_rates = []
    r_percent = [r * 100 for r in tax_rates]

    for i in range(len(diff_values)):
        if i == 0:
            # 第一个点使用前向差分
            dr = tax_rates[i+1] - tax_rates[i]
            growth = (diff_values[i+1] - diff_values[i]) / (dr * 100)
        elif i == len(diff_values) - 1:
            # 最后一个点使用后向差分
            dr = tax_rates[i] - tax_rates[i-1]
            growth = (diff_values[i] - diff_values[i-1]) / (dr * 100)
        else:
            # 中间点使用中心差分
            dr = tax_rates[i+1] - tax_rates[i-1]
            growth = (diff_values[i+1] - diff_values[i-1]) / (dr * 100)
        growth_rates.append(growth)

    # 绘图
    plt.figure(figsize=(14, 8))

    # 主曲线
    plt.plot(r_percent, growth_rates,
             linewidth=2.5, color='#C73E1D', marker='v', markersize=6,
             label=f'收益率提升的增长速度 d(y-b1)/dr')

    # 标记每个点的数值
    for i, (r, growth) in enumerate(zip(r_percent, growth_rates)):
        plt.annotate(f'{growth:.4f}',
                    xy=(r, growth),
                    xytext=(0, 8 if growth > 0 else -12),
                    textcoords='offset points',
                    fontsize=8,
                    ha='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral',
                            alpha=0.7, edgecolor='none'))

    # 添加零线
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1,
                alpha=0.5, label='零线 (增长速度为0)')

    # 填充正值区域（边际收益递增）
    plt.fill_between(r_percent, 0, growth_rates,
                     where=[g > 0 for g in growth_rates],
                     alpha=0.2, color='blue', label='边际收益递增区域')

    # 填充负值区域（边际收益递减）
    plt.fill_between(r_percent, 0, growth_rates,
                     where=[g < 0 for g in growth_rates],
                     alpha=0.2, color='orange', label='边际收益递减区域')

    # 设置标签和标题
    plt.xlabel('税率 r (%)', fontsize=12, fontweight='bold')
    plt.ylabel('增长速度 d(y-b1)/dr (%/百分点税率)', fontsize=12, fontweight='bold')
    plt.title(f'税率提升对收益率提升的边际影响 (a1={a1}年)\n' +
              f'(每提升1个百分点税率，收益率提升(y-b1)的变化量)',
              fontsize=14, fontweight='bold', pad=20)

    # 添加网格
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

    # 图例
    plt.legend(fontsize=10, loc='best', framealpha=0.9)

    # 设置坐标轴范围
    plt.xlim(0, 50)
    growth_min = min(growth_rates) - 0.01
    growth_max = max(growth_rates) + 0.01
    plt.ylim(growth_min, growth_max)

    # 添加说明文字
    note_text = f"注: 固定缴存年数a1={a1}年，a2={a2}年\n税率变化时，缴存金额m也随之变化"
    plt.text(0.02, 0.98, note_text,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()

    # 保存图片
    output_path = r'c:\procedure2012\pension\pension_yield_diff_growth_vs_tax_rate.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n第五张图片已保存到: {output_path}")

    # 显示图片
    plt.show()

    return growth_rates, r_percent


if __name__ == '__main__':
    print("=" * 60)
    print("个人养老金等价年化收益率 vs 缴存年数")
    print("=" * 60)
    print()

    # 第一张图：y vs a1
    a1_vals, y_vals, opt_a1, opt_y = plot_yield_vs_years()

    print("\n" + "=" * 60)
    print("分析总结 (图1: y vs a1):")
    print("=" * 60)
    print(f"最优缴存年数: {opt_a1} 年")
    print(f"最大等价年化收益率: {opt_y*100:.4f}%")
    print(f"相比养老金产品本身(3.4%)提升: {(opt_y - 0.034)*100:.4f}%")
    print(f"相比其他理财产品(2.0%)提升: {(opt_y - 0.02)*100:.4f}%")

    # 第二张图：(y-b1) vs a1
    print("\n" + "=" * 60)
    print("绘制第二张图：收益率提升 (y - b1) vs 缴存年数")
    print("=" * 60)
    print()

    diff_vals, opt_a1_diff, opt_diff = plot_yield_diff_vs_years(a1_vals, y_vals)

    print("\n" + "=" * 60)
    print("分析总结 (图2: y-b1 vs a1):")
    print("=" * 60)
    print(f"最大提升对应的缴存年数: {opt_a1_diff} 年")
    print(f"最大收益率提升: {opt_diff:.4f}%")
    print(f"解读: 考虑退税优惠和3%提取税后，")
    print(f"      在缴存{opt_a1_diff}年时，整体年化比产品本身高{opt_diff:.4f}%")

    # 第三张图：d(y-b1)/da1 vs a1
    print("\n" + "=" * 60)
    print("绘制第三张图：收益率提升的增长速度 d(y-b1)/da1 vs 缴存年数")
    print("=" * 60)
    print()

    growth_rates, zero_crossings = plot_yield_diff_growth_vs_years(a1_vals, y_vals)

    print("\n" + "=" * 60)
    print("分析总结 (图3: d(y-b1)/da1 vs a1):")
    print("=" * 60)
    print(f"增长速度范围: [{min(growth_rates):.5f}, {max(growth_rates):.5f}] %/年")
    if zero_crossings:
        print(f"拐点位置: a1 ≈ {zero_crossings} 年")
        print(f"解读: 在拐点之前，边际收益递增；在拐点之后，边际收益递减")
    else:
        if all(g > 0 for g in growth_rates):
            print("解读: 收益率提升在整个区间内单调递增")
        elif all(g < 0 for g in growth_rates):
            print("解读: 收益率提升在整个区间内单调递减")
        else:
            print("解读: 收益率提升存在非单调变化")
    print(f"实际意义: 此图展示每多缴存1年，收益率提升(y-b1)会增加多少个百分点")

    # 第四张图：y vs r (不同a1)
    print("\n" + "=" * 60)
    print("绘制第四张图：不同税率下的等价年化收益率 (三种缴存年数对比)")
    print("=" * 60)
    print()

    plot_yield_vs_tax_rate()

    print("\n" + "=" * 60)
    print("分析总结 (图4: y vs r):")
    print("=" * 60)
    print("解读: ")
    print("  - 税率越高，退税优惠越大，等价年化收益率y越高")
    print("  - 缴存年数越长(a1越大)，整体年化收益率y越高")
    print("  - 税率3%时不缴存(m=0)，收益为0")
    print("  - 三条曲线的差异展示了缴存时长对收益的影响")

    # 第五张图：d(y-b1)/dr vs r (固定a1=10)
    print("\n" + "=" * 60)
    print("绘制第五张图：税率提升对收益率提升的边际影响 (a1=10年)")
    print("=" * 60)
    print()

    growth_rates_r, r_percent = plot_yield_diff_growth_vs_tax_rate()

    print("\n" + "=" * 60)
    print("分析总结 (图5: d(y-b1)/dr vs r):")
    print("=" * 60)
    print(f"增长速度范围: [{min(growth_rates_r):.5f}, {max(growth_rates_r):.5f}] %/百分点税率")
    print("解读: ")
    print("  - 此图展示每提升1个百分点税率，收益率提升(y-b1)会增加多少")
    print("  - 正值表示税率提升带来的边际收益为正")
    print("  - 数值越大，说明该税率区间对收益提升的边际贡献越大")
    print("  - 实际意义：帮助判断在哪个税率档位，提升税率对养老金收益的边际影响最大")
