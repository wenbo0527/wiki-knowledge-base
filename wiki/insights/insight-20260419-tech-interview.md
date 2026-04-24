# Insight: Tech Interview Handbook - 技术面试完全指南

> **来源**: GitHub开源项目  
> **项目**: Tech Interview Handbook  
> **Star数**: 138K+  
> **日期**: 2026-04-19  
> **评级**: ⭐⭐⭐⭐ (4/5)  
> **标签**: #技术面试 #算法 #系统设计 #职业发展 #面试技巧

---

## 执行摘要

Tech Interview Handbook是GitHub上最受欢迎的面试准备资源之一，累积138K+ Stars。该项目由前Facebook工程师Yangshun Tay创建，系统性地涵盖了技术面试的各个环节，从算法准备到系统设计，从简历优化到薪资谈判。

**核心洞察**: 技术面试不仅是算法能力的考察，更是问题解决能力、沟通技巧和工程思维的全面评估。

---

## 项目概览

### 内容结构

```
Tech Interview Handbook/
├── 准备阶段/
│   ├── 简历优化
│   ├── 公司研究
│   └── 时间规划
├── 算法面试/
│   ├── 数据结构
│   ├── 算法模式
│   └── LeetCode指南
├── 系统设计/
│   ├── 基础知识
│   ├── 案例分析
│   └── 设计文档
├── 行为面试/
│   ├── STAR法则
│   ├── 常见问题
│   └── 经验分享
└── 面试后/
    ├── 复盘总结
    ├── 薪资谈判
    └── 决策框架
```

### 核心贡献者

- **Yangshun Tay**: 创始人，前Facebook工程师
- **社区贡献者**: 500+ 贡献者，持续更新
- **行业专家**: 来自Google、Amazon、Microsoft等公司的面试官参与内容审核

---

## 算法面试准备指南

### 学习路径规划

**第1-2周：基础夯实**
- 数组、链表、栈、队列
- 哈希表、集合
- 树（二叉树、BST）
- 图的基础（表示方法）

**第3-4周：算法模式**
- 双指针技术
- 滑动窗口
- 快慢指针
- 合并区间
- 循环排序

**第5-6周：高级算法**
- 动态规划基础
- 递归与回溯
- 分治法
- 贪心算法
- 图的遍历算法

**第7-8周：模拟面试**
- 每天2-3道LeetCode题
- 计时练习（15-20分钟/题）
- 白板练习
- 录制视频复盘

### 重点算法模式详解

**1. 滑动窗口模式**

```python
# 题目：给定数组，找到和为k的连续子数组
# 输入：nums = [1, 1, 1], k = 2
# 输出：2 (有两个和为2的子数组)

def subarray_sum(nums: List[int], k: int) -> int:
    """
    使用前缀和 + 哈希表的滑动窗口技巧
    
    核心思想：
    - prefix_sum[i] = sum(nums[0:i+1])
    - 如果 prefix_sum[j] - prefix_sum[i] = k
    - 则 nums[i+1:j+1] 的和为 k
    
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    count = 0
    prefix_sum = 0
    # 哈希表：前缀和 -> 出现次数
    sum_count = {0: 1}  # 初始值：前缀和为0出现1次（空数组）
    
    for num in nums:
        prefix_sum += num
        
        # 如果存在 prefix_sum - k，说明有子数组和为k
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        
        # 更新当前前缀和的出现次数
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count


# 面试话术：
# "这道题的难点在于数组中有负数，不能用传统的滑动窗口。
# 我想到用前缀和的思想，配合哈希表来记录前缀和出现的次数。
# 这样时间复杂度是O(n)，空间复杂度也是O(n)。"
```

**2. 动态规划模式**

```python
# 题目：最长递增子序列 (LIS)
# 输入：nums = [10, 9, 2, 5, 3, 7, 101, 18]
# 输出：4 (最长递增子序列是 [2, 3, 7, 101])

def length_of_lis(nums: List[int]) -> int:
    """
    动态规划解法
    
    状态定义：
    - dp[i] = 以nums[i]结尾的最长递增子序列的长度
    
    状态转移：
    - dp[i] = max(dp[j] + 1) for all j < i and nums[j] < nums[i]
    - 如果没有这样的j，dp[i] = 1
    
    答案：max(dp)
    
    时间复杂度：O(n²)
    空间复杂度：O(n)
    """
    if not nums:
        return 0
    
    n = len(nums)
    dp = [1] * n  # 每个元素至少可以构成长度为1的子序列
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                # 如果nums[j] < nums[i]，可以接在后面形成更长的子序列
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


# 更优解法：二分查找 O(n log n)
def length_of_lis_optimized(nums: List[int]) -> int:
    """
    使用二分查找优化到 O(n log n)
    
    核心思想：
    - tails[i] = 长度为i+1的递增子序列的最小末尾元素
    - 维护tails数组，保持其递增（可用二分查找）
    
    时间复杂度：O(n log n)
    空间复杂度：O(n)
    """
    tails = []  # tails[i] = 长度为i+1的LIS的最小末尾元素
    
    for num in nums:
        # 二分查找：找到第一个 >= num的位置
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        # 如果left == len(tails)，说明num比所有末尾都大，可以扩展LIS
        if left == len(tails):
            tails.append(num)
        else:
            # 否则替换，保持tails的递增性
            tails[left] = num
    
    return len(tails)


# 面试进阶话术：
# "我先给出了O(n²)的动态规划解法，解释了状态定义和转移方程。
# 然后面试官问我能不能优化，我想到可以用二分查找优化到O(n log n)。
# 关键是维护一个tails数组，记录每个长度LIS的最小末尾元素。"
```

### LeetCode刷题指南

**按类别刷题计划**:

| 周次 | 主题 | 题量 | 重点题目 |
|------|------|------|----------|
| 1 | 数组&链表 | 15 | 两数之和、合并区间、LRU缓存 |
| 2 | 栈&队列 | 12 | 有效的括号、每日温度、滑动窗口最大值 |
| 3 | 哈希表 | 10 | 字母异位词、最长连续序列、四数之和 |
| 4 | 树 | 20 | 二叉树遍历、最近公共祖先、序列化和反序列化 |
| 5 | 图 | 15 | 课程表、岛屿数量、