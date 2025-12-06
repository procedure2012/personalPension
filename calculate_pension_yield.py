import numpy as np
from scipy.optimize import fsolve


def calculate_equivalent_yield(r, m, a1, a2, b1, b2):
    """
    计算个人养老金的等价年化收益率y

    参数:
        r (float): 当前税率 (例如: 0.20 表示20%)
        m (float): 每年缴存总数 (元)
        a1 (int): 缴存年数
        a2 (int): 缴存a1年后，距离退休的年数
        b1 (float): 个人养老金理财产品年化收益率 (例如: 0.05 表示5%)
        b2 (float): 其他理财产品年化收益率 (例如: 0.03 表示3%)

    返回:
        float: 等价年化收益率y
    """

    def equation(y):
        """
        求解超越方程:
        (1+y)^(a2+1) · [(1+y)^a1 - 1] / y =
            0.97 · (1+b1)^(a2+1) · [(1+b1)^a1 - 1] / b1
            + r · (1+b2)^(a2+1) · [(1+b2)^a1 - 1] / b2
        """
        left_side = ((1 + y) ** (a2 + 1)) * (((1 + y) ** a1 - 1) / y)

        right_term1 = 0.97 * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1)
        right_term2 = r * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)
        right_side = right_term1 + right_term2

        return left_side - right_side

    # 使用b1作为初始猜测值
    initial_guess = b1

    # 求解方程
    solution = fsolve(equation, initial_guess)

    return solution[0]


def calculate_pension_value(r, m, a1, a2, b1, b2):
    """
    计算方案A的总收益 V_A

    参数:
        r (float): 当前税率
        m (float): 每年缴存总数 (元)
        a1 (int): 缴存年数
        a2 (int): 缴存a1年后，距离退休的年数
        b1 (float): 个人养老金理财产品年化收益率
        b2 (float): 其他理财产品年化收益率

    返回:
        dict: 包含各部分收益的字典
    """
    # 养老金账户收益（扣除3%税后）
    S1_gross = m * ((1 + b1) ** (a2 + 1)) * (((1 + b1) ** a1 - 1) / b1)
    S1_net = S1_gross * 0.97

    # 退税再投资收益
    S2 = m * r * ((1 + b2) ** (a2 + 1)) * (((1 + b2) ** a1 - 1) / b2)

    # 总收益
    V_A = S1_net + S2

    return {
        '养老金账户收益(税前)': S1_gross,
        '养老金账户收益(扣除3%税后)': S1_net,
        '退税再投资收益': S2,
        '总收益': V_A
    }


if __name__ == '__main__':
    # 示例：计算等价年化收益率
    print("=" * 60)
    print("个人养老金等价年化收益率计算")
    print("=" * 60)

    # 示例参数
    r = 0.25      # 税率20%
    m = 12000     # 每年缴存12000元
    a1 = 10       # 缴存10年
    a2 = 24       # 缴存后距离退休20年
    b1 = 0.0345     # 养老金产品年化5%
    b2 = 0.02     # 其他理财产品年化3%

    print(f"\n输入参数:")
    print(f"  当前税率 r = {r*100:.1f}%")
    print(f"  每年缴存 m = {m:,.0f} 元")
    print(f"  缴存年数 a1 = {a1} 年")
    print(f"  距离退休年数 a2 = {a2} 年")
    print(f"  养老金产品年化 b1 = {b1*100:.1f}%")
    print(f"  其他理财年化 b2 = {b2*100:.1f}%")

    # 计算等价年化收益率
    y = calculate_equivalent_yield(r, m, a1, a2, b1, b2)

    print(f"\n计算结果:")
    print(f"  等价年化收益率 y = {y*100:.4f}%")

    # 计算详细收益
    values = calculate_pension_value(r, m, a1, a2, b1, b2)
    print(f"\n收益明细:")
    for key, value in values.items():
        print(f"  {key}: {value:,.2f} 元")

    # 对比分析
    print(f"\n对比分析:")
    print(f"  养老金产品本身年化 b1 = {b1*100:.2f}%")
    print(f"  考虑退税和提取税后 y = {y*100:.4f}%")
    print(f"  差异 = {(y-b1)*100:.4f}%")

    if y > b2:
        print(f"  ✓ 等价年化 y ({y*100:.4f}%) > 其他理财 b2 ({b2*100:.2f}%), 投资养老金有优势")
    else:
        print(f"  ✗ 等价年化 y ({y*100:.4f}%) ≤ 其他理财 b2 ({b2*100:.2f}%), 投资养老金无优势")

    print("\n" + "=" * 60)

    # 敏感性分析：不同税率下的等价年化
    print("\n敏感性分析：不同税率下的等价年化收益率")
    print("=" * 60)
    print(f"{'税率':<10} {'等价年化y':<15} {'vs b1差异':<15} {'vs b2比较'}")
    print("-" * 60)

    for tax_rate in [0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.45]:
        y_temp = calculate_equivalent_yield(tax_rate, m, a1, a2, b1, b2)
        diff = y_temp - b1
        comparison = "优于b2" if y_temp > b2 else "不如b2"
        print(f"{tax_rate*100:>5.0f}%     {y_temp*100:>8.4f}%      {diff*100:>+8.4f}%      {comparison}")
