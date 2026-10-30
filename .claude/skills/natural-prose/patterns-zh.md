# Chinese Patterns

Concrete signals of the [pattern families](patterns.md) in Chinese academic prose. The examples are invented; every revision uses only the information in its original. Chinese academic writing is formal by nature: passives, four-character phrases, and nominal style are often correct, so judge each signal in context.

## 1. Emphasis without content

- Contrasts: “不仅仅是……更是……”, “不是……而是……”, “与其说……不如说……” when nobody holds the first view.
- Closers: “这充分说明了……的重要性”, “由此可见” after an example that already shows the point, “意义重大”.
- Sayings: “归根结底”, “本质上”, “说到底”, “……的核心在于……”.
- Announcements: “下面我们将深入探讨……”, “值得注意的是”, “需要指出的是”, “不难发现”, “众所周知” before a routine statement.

> Before: 下面将深入探讨本文方法：它只需一次遍历即可完成稀疏注意力的计算。换言之，本文方法只需遍历一次。
>
> After: 本文方法只需一次遍历即可完成稀疏注意力的计算。

## 2. Impact language and overstatement

- Significance: “具有重要的理论意义和应用价值”, “具有里程碑意义”, “开辟了新的途径”, “奠定了坚实基础”, “为……提供了新思路”, “具有广阔的应用前景”.
- Promotion: “颠覆性”, “革命性”, “前所未有”, “极大地”, “全面提升”, “完美解决”.
- Novelty: “首次提出”, “填补了国内外空白” without a recorded search.
- Statistical or magnitude language: “显著” can mean statistical significance or a conspicuous difference. Require a reported test when the context asserts statistical significance; do not treat every strong comparison or impact adjective as a statistical claim.

> Before: 实验结果表明，本文方法显著优于现有方法（平均 IoU 为 74.0，最强基线为 71.2），具有广阔的应用前景。
>
> After: 实验结果表明，本文方法显著优于现有方法，平均 IoU 为 74.0，最强基线为 71.2。本文方法具有广阔的应用前景。

The comparison and outlook remain. Inspect the evidence for the comparison and any statistical meaning of “显著”; do not infer that a test is absent from the wording alone. “具有广阔的应用前景” is allowed as an authorial assessment of potential, without implying that applications were already tested.

## 3. Unsourced authority and vague relations

- Authority: “有研究表明”, “大量研究证明”, “学术界普遍认为”, “专家指出” without citations.
- Relations: “与……密切相关”, “与……存在关联”, “对……产生影响” when the text knows the relation.

> Before: 大量研究表明，睡眠不足与工作记忆受损密切相关。
>
> After: 大量研究表明，睡眠不足与工作记忆受损密切相关 [TODO: 补充这些研究的引用，并核实关联的强度和性质]。

## 4. Template rhythm

- Connectives: “首先……其次……再次……最后……” for points without an order; “此外”, “另外”, “同时”, “与此同时”, “进一步地” opening sentence after sentence.
- Stacked four-character phrases: “高效稳定、灵活便捷、安全可靠”.
- Openings: “本文……本文……本文……”.
- Dashes: “——” for asides in many sentences.
- Hedge stacks: “可能在一定程度上或许能够……”.

> Before: 此外，该模型高效稳定、灵活便捷、安全可靠。同时，该模型只需单张 GPU 即可训练。进一步地，该模型通常在数小时内收敛——明显快于基线——并且可能在一定程度上或许能够迁移到其他领域。
>
> After: 该模型高效稳定、灵活便捷、安全可靠，只需单张 GPU 即可训练。它通常在数小时内收敛，明显快于基线，并可能在一定程度上迁移到其他领域。

The listed properties, the strength of the baseline comparison, and “在一定程度上” remain; none follows merely from using one GPU.

Keep “首先……其次……” for steps with a real order, a parallel structure that lists distinct facts, and established four-character terms such as “实时处理” or “端到端”.

## 5. Wordy constructions

- “进行” plus a verb: “对数据进行分析” (分析数据), “进行了实验验证” (通过实验验证). Keep it when it carries aspect, as in “测试正在进行”.
- “起到了……的作用” and “作为……而存在” where “用于” or “是” fits.
- Redundant frames: “基于……的基础上”, “对于……来说”, “在……方面”.
- Chains of “的”: “基于深度学习的图像分割方法的性能的提升”; split them into two clauses.

## 6. Stock vocabulary

Watch these words, especially in groups. Each one is a signal, not a ban: choose the specific wording that fits, or cut the word.

- Empty emphasis: 毋庸置疑, 不可磨灭, 举足轻重, 切中要害, 深刻, and 本质上 when it only adds emphasis.
- Inflated verbs and nouns: 赋能, 助力, 打造, 深耕, 抓手, 底层逻辑, 顶层设计, 颗粒度, 链路, 范式转移, 颠覆性.
- Words that add no information: 全方位, 多维度, 深度融合, 无缝, 极致, 至关重要, 不可或缺, 深入探讨.

Keep the technical senses: “闭环控制”, “维度” in mathematics, “范式” in its philosophical sense, and “生态” in ecology.

When a sentence only praises a method, replace the praise with what the method does. Before: “该方法十分强大，令人印象深刻，在三个数据集上的准确率均高于两种基线方法。” After: “该方法在三个数据集上的准确率均高于两种基线方法。”

## 7. Template formatting

- Bold or italic emphasis in running text; “**优势：**……” labels before each item; lists where the argument needs prose; emojis in headings.
- Punctuation: full-width marks in Chinese text (，。；：“”（）), half-width marks in formulas, code, and Western-language passages. Whether a space separates Chinese and Western words follows the venue or the manuscript's settled practice; keep one practice throughout.

## 8. Assistant residue and placeholders

- “好的，以下是修改后的段落：”, “希望对您有所帮助”, “如需进一步修改，请告诉我”.
- “作为一个人工智能模型”, “截至我的知识更新”.
- “（此处插入引用）”, “XX%”.

## 9. Translated-sounding prose

- Long modifiers before a noun: “一个能够在资源受限的边缘设备上实时运行的基于知识蒸馏的轻量级目标检测模型”; move part of it into a following clause.
- Stacked “被”: “该方法被广泛应用于……，被证明是有效的”; prefer an active or subjectless sentence when the agent is known. Keep “被” when the agent is unknown, as in “样本已被污染”.
- Pronouns that Chinese would drop (“它”, “其”, “他们” in every sentence); “一个” before every noun; “当……的时候”, “如果……的话”, “作为一种……，它……”.
- Old documentary register in modern prose: “系”, “拟”, “业已”, “兹”, and frequent “之”. “旨在” is current usage and stays.

> Before: 本文中，一个能够在资源受限的边缘设备上实时运行的基于知识蒸馏的轻量级目标检测模型被提出，并且它被证明是有效的。
>
> After: 本文提出一种基于知识蒸馏的轻量级目标检测模型，可在资源受限的边缘设备上实时运行，其有效性已得到证明 [TODO: 指明所依据的验证结果]。

The agent comes from “本文中”; without it, the passive would stay, because the text would not say who proposed the model.

## 10. Letters that bury the answer

- “非常感谢审稿人提出的宝贵意见，该意见对提高本文质量具有重要意义” before every answer.
- A restatement of the comment, then background, then the change in the last sentence.

> Before: 非常感谢审稿人提出的宝贵意见，这一意见对提升本文质量具有重要意义。我们完全同意基线选择是实证研究的重要方面，并对此进行了认真的思考。根据审稿人的建议，我们在第 4.2 节增加了与两种最新方法的比较。
>
> After: 感谢审稿人的意见，这一意见对提升本文质量具有重要意义。根据您的建议，我们在第 4.2 节增加了与两种最新方法的比较。我们完全同意基线选择是实证研究的重要方面，并已认真考虑这一点。
