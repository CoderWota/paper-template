# Japanese Patterns

Concrete signals of the [pattern families](patterns.md) in Japanese academic prose. The examples are invented; every revision uses only the information in its original. Articles keep the である style throughout; letters keep です・ます. Do not mix in noun-ending sentences (体言止め), colloquial endings, or personal asides to make a paper sound human: the cure for monotony is varied sentence structure and length, not a change of register.

## 1. Emphasis without content

- Contrasts: 「単なる〜ではなく、〜である」「〜というよりむしろ〜」 when nobody holds the first view.
- Closers: 「このことは〜の重要性を如実に示している」「以上のことから、〜は極めて重要であると言える」 after the result already shows the point.
- Sayings: 「〜の本質は〜にある」「〜こそが鍵である」.
- Announcements: 「ここで重要なのは〜という点である」「注目すべきは」「以下で詳しく見ていく」「言うまでもなく」 before a routine statement.

> Before: 提案手法は単なる既存手法の改良ではなく、スパース注意の計算方法を根本から見直すものであり、1 回の走査で計算を完了する。このことは効率的な注意機構の重要性を如実に示している。
>
> After: 提案手法は 1 回の走査でスパース注意の計算を完了する。

## 2. Inflated significance and promotion

- Significance: 「重要な役割を果たす」「極めて重要である」「計り知れない意義」「〜の礎となる」「今後のさらなる発展が期待される」「大いに期待される」.
- Promotion: 「画期的」「革新的」「飛躍的に向上」「圧倒的」.
- Novelty: 「世界で初めて」「従来にない」 without a recorded search.
- Statistics words: 「有意に」「顕著に」 need a test in the result record.

> Before: 提案手法は既存手法を大幅に上回り（平均 IoU 74.0、最良のベースラインは 71.2）、今後のさらなる発展が大いに期待される。
>
> After: 提案手法の平均 IoU は 74.0 であり、最良のベースラインは 71.2 であった。

## 3. Unsourced authority and vague relations

- Authority: 「多くの研究で示されているように」「専門家によれば」「一般に〜と言われている」「周知のとおり」 without citations.
- Relations: 「〜と密接に関連している」「〜に関係する」「〜に影響を与える」 when the text knows the relation.

> Before: 多くの研究で示されているように、睡眠不足は作業記憶の低下と密接に関連している。
>
> After: 睡眠不足は作業記憶の低下と関連する [TODO: 引用を追加し、因果関係を示す証拠かどうかを記す]。

## 4. Template rhythm

- Connectives: 「さらに」「また」「加えて」「一方で」「このように」 opening sentence after sentence.
- Triads: 「高速かつ高精度、そして汎用的」.
- Openings: 「本研究は〜。本研究は〜。本研究は〜。」.
- Dashes: 「——」 for asides in many sentences.
- Hedge stacks: 「〜可能性があると考えられる」「〜かもしれないと思われる」.
- Endings: every sentence ending in 「〜である。」 with the same length; vary the structure instead.

> Before: さらに、本モデルは軽量かつ高速、そして高効率である。また、本モデルは単一の GPU で学習できる。加えて、本モデルは数時間で収束し——ベースラインよりも速く——他分野へ転用できる可能性があると考えられる。
>
> After: 本モデルは単一の GPU で学習でき、数時間で収束する。収束はベースラインよりも速く、他分野へ転用できる可能性がある。

## 5. Wordy constructions

- 「〜することができる」 (〜できる).
- 「〜を行う」「〜を実施する」: 「分析を行った」 (分析した), 「検証を実施した」 (検証した).
- Frequent 「〜という形で」「〜において」「〜における」「〜に対して」 where a plain particle fits.
- Chains of 「の」: 「提案手法の性能の評価の結果」; split or rephrase.

## 6. Stock vocabulary

Watch these, especially in groups: 「多角的」「包括的」「網羅的」 (outside their literal use), 「シームレス」「レバレッジ」「エンパワー」「パラダイムシフト」「ゲームチェンジャー」, 「〜を浮き彫りにする」「示唆に富む」「注目に値する」「〜と言っても過言ではない」「〜と言えるだろう」「〜ではないだろうか」. Prefer the established Japanese term where the field uses one (手法 rather than アプローチ, 解決策 rather than ソリューション), and keep the katakana terms the field uses (モデル, データ, アルゴリズム).

## 7. Template formatting

- Bold or italic emphasis in running text; 「**利点：**」 labels before each item; lists where the argument needs prose; headings for every short paragraph.
- Punctuation: use 「、。」 or 「，．」 as the venue or the field does, and keep one choice throughout; keep full-width or half-width digits and Latin letters consistent.

## 8. Assistant residue and placeholders

- 「もちろんです」「以下に修正版を示します」「お役に立てれば幸いです」「ご不明な点があればお知らせください」.
- 「AI 言語モデルとして」「私の知識の範囲では」.
- 「（ここに引用を挿入）」「XX%」.

## 9. Translated-sounding prose

- Explicit subjects in every sentence: 「本手法は〜。本手法は〜。」, frequent 「我々は」「それは」.
- Long modifiers before a noun; move part of them into a following clause.
- Passive where the authors act: 「〜されることが示された」 (〜ことを示した). Keep the passive when the agent is unknown.
- 「〜において」「〜に対して」 as default translations of "in" and "for"; katakana where a Japanese word exists (see section 6).

> Before: 本手法は軽量である。本手法はエッジ端末において実時間で動作することが可能である。本手法の有効性は実験により示された。
>
> After: 本手法は軽量で、エッジ端末で実時間に動作できる。その有効性は実験で示した [TODO: 該当する実験結果を明記する]。

「可能である」 becomes 「できる」, not 「動作する」: the revision keeps the modality of the original.

## 10. Letters that bury the answer

- 「査読者の大変貴重なご指摘に心より感謝申し上げます」 before every answer.
- A restatement of the comment, then background, then the change in the last sentence.

> Before: 査読者の大変貴重なご指摘に心より感謝申し上げます。ベースラインの選定は実証研究の要となる点であり、ご指摘を踏まえて慎重に検討いたしました。その結果、4.2 節に最新の 2 手法との比較を追加いたしました。
>
> After: ご指摘ありがとうございます。4.2 節に最新の 2 手法との比較を追加しました。
