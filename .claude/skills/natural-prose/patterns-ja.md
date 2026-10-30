# Japanese Patterns

Concrete signals of the [pattern families](patterns.md) in Japanese academic prose. The examples are invented; ordinary style revisions use only the information in their originals. Family 11 states separate evidence assumptions for an authorized recalibration. Articles keep the である style throughout; letters keep です・ます. Do not mix in noun-ending sentences (体言止め), colloquial endings, or personal asides to make a paper sound human: the cure for monotony is varied sentence structure and length, not a change of register.

## 1. Emphasis without content

- Contrasts: 「単なる〜ではなく、〜である」「〜というよりむしろ〜」 when nobody holds the first view.
- Closers: 「このことは〜の重要性を如実に示している」「以上のことから、〜は極めて重要であると言える」 after the result already shows the point.
- Sayings: 「〜の本質は〜にある」「〜こそが鍵である」.
- Announcements: 「ここで重要なのは〜という点である」「注目すべきは」「以下で詳しく見ていく」「言うまでもなく」 before a routine statement.

> Before: ここでは提案手法について詳しく述べる。提案手法は 1 回の走査でスパース注意の計算を完了する。言い換えれば、必要な走査は 1 回である。
>
> After: 提案手法は 1 回の走査でスパース注意の計算を完了する。

## 2. Impact language and overstatement

- Significance: 「重要な役割を果たす」「極めて重要である」「計り知れない意義」「〜の礎となる」「今後のさらなる発展が期待される」「大いに期待される」.
- Promotion: 「画期的」「革新的」「飛躍的に向上」「圧倒的」.
- Novelty: 「世界で初めて」「従来にない」 without a recorded search.
- Statistical or magnitude language: 「有意に」 in a statistical claim needs a reported test. 「顕著に」「大幅に」 can describe magnitude without asserting statistical significance. Strong impact language alone is not an error.

> Before: 提案手法は既存手法を大幅に上回り（平均 IoU 74.0、最良のベースラインは 71.2）、今後のさらなる発展が大いに期待される。
>
> After: 提案手法は既存手法を大幅に上回る（平均 IoU 74.0、最良のベースラインは 71.2）。今後のさらなる発展が大いに期待される。

The comparison's degree and ambitious outlook remain. Check the actual comparison scope; 「大幅に」 does not by itself assert a statistical test, and the outlook does not say that future developments have already occurred.

## 3. Unsourced authority and vague relations

- Authority: 「多くの研究で示されているように」「専門家によれば」「一般に〜と言われている」「周知のとおり」 without citations.
- Relations: 「〜と密接に関連している」「〜に関係する」「〜に影響を与える」 when the text knows the relation.

> Before: 多くの研究で示されているように、睡眠不足は作業記憶の低下と密接に関連している。
>
> After: 多くの研究で、睡眠不足は作業記憶の低下と密接に関連していることが示されている [TODO: これらの研究を引用し、関連の強さと性質を確認する]。

## 4. Template rhythm

- Connectives: 「さらに」「また」「加えて」「一方で」「このように」 opening sentence after sentence.
- Triads: 「高速かつ高精度、そして汎用的」.
- Openings: 「本研究は〜。本研究は〜。本研究は〜。」.
- Dashes: 「——」 for asides in many sentences.
- Hedge stacks: 「〜可能性があると考えられる」「〜かもしれないと思われる」.
- Endings: every sentence ending in 「〜である。」 with the same length; vary the structure instead.

> Before: さらに、本モデルは軽量かつ高速、そして高効率である。また、本モデルは単一の GPU で学習できる。加えて、本モデルは数時間で収束し——ベースラインよりも速く——他分野へ転用できる可能性があると考えられる。
>
> After: 本モデルは軽量、高速、高効率であり、単一の GPU で学習できる。数時間で収束し、ベースラインよりも速い。他分野へ転用できる可能性があると考えられる。

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
> After: 本手法は軽量で、エッジ端末で実時間に動作できる。その有効性は実験で示された [TODO: 該当する実験結果を明記する]。

「可能である」 becomes 「できる」, not 「動作する」: the revision keeps the modality of the original.

## 10. Letters that bury the answer

- 「査読者の大変貴重なご指摘に心より感謝申し上げます」 before every answer.
- A restatement of the comment, then background, then the change in the last sentence.

> Before: 査読者の大変貴重なご指摘に心より感謝申し上げます。ベースラインの選定は実証研究の要となる点であり、ご指摘を踏まえて慎重に検討いたしました。その結果、4.2 節に最新の 2 手法との比較を追加いたしました。
>
> After: ご指摘ありがとうございます。ご指摘を踏まえ、4.2 節に最新の 2 手法との比較を追加しました。ベースラインの選定は実証研究の要であると認識し、慎重に検討しました。

## 11. Excessive caution and understatement

- Signals: 「慎重に解釈する必要がある」 without a specific consequence; 「可能性があると考えられる」 for a checked result; repeated apologies for tasks the paper never promised.
- The invented example assumes a checked result, an untested clinical use raised in the discussion, and no video claim. This is an authorized recalibration, not a translation or ordinary polish.

> Before: 本研究には限界があるものの、提案手法は三つのホールドアウトデータセットで誤差を 12% 低減する可能性がある。動画は処理できず、コントラストが異なる臨床画像では未検証である。さらなる研究が必要である。
>
> After: 提案手法は三つのホールドアウトデータセットで誤差を 12% 低減した。臨床画像はコントラストが異なり、未検証であるため、この結果は現時点では臨床利用を裏付けない。

The checked finding is direct; the clinical limit and its effect stay. The video boundary stays in the result record. Keep 「可能性がある」 when it marks a genuinely uncertain inference. Without the evidence or authorization, flag the proposed change.

The example states a checked result directly while retaining its conditions and relevant limit. Claims about novelty, causality, generalization, or impact also need support. For a requested change to claim strength, read [argument and impact guidance](../manuscript-writing/argument-and-impact.md).
