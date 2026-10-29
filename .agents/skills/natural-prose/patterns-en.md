# English Patterns

Concrete signals of the [pattern families](patterns.md) in English scholarly prose. The examples are invented; every revision uses only the information in its original.

## 1. Emphasis without content

- Contrasts: "not only X but also Y" or "not merely X; it is Y" when nobody holds X; "rather than simply"; a negative tail ("..., not a heuristic").
- Closers: "This underscores the importance of ..."; "These findings highlight the need for ..."; "This represents a crucial step toward ..."; a single-sentence paragraph that echoes the previous paragraph.
- Sayings: "At its core, ..."; "The key lies in ..."; "X is the backbone of Y".
- Announcements: "In this section, we delve into ..."; "It is worth noting that"; "It is important to note that"; "Notably," or "Importantly," before a routine statement.
- Unraised objections: "This is not to say that ..."; "One might argue that ..., but ..." when nobody has argued it.

> Before: Our method is not merely an incremental improvement; it represents a fundamental rethinking of sparse attention, computing it in a single pass rather than two. This underscores the importance of efficient attention in modern architectures.
>
> After: Our method computes sparse attention in a single pass instead of two.

## 2. Inflated significance and promotion

- Significance: "plays a pivotal (crucial, vital) role", "a cornerstone of", "a testament to", "paves the way for", "opens new avenues", "sheds light on", "holds great promise", "far-reaching implications".
- Promotion: "groundbreaking", "revolutionary", "unprecedented", "remarkable", "superior", "novel" on every page, "state-of-the-art" without the comparison that shows it.
- Novelty: "To the best of our knowledge, this is the first ..." or "fills a critical gap" without a recorded search.
- Statistics words: "significantly", "dramatically", "substantially", "markedly" for a difference without a test, or without the numbers.

> Before: These remarkable results, a mean IoU of 74.0 against 71.2 for the strongest baseline, demonstrate that our framework significantly outperforms existing approaches and paves the way for a new generation of segmentation models.
>
> After: Our framework reaches a mean IoU of 74.0, against 71.2 for the strongest baseline.

"Significantly" returns only when the result record reports a test.

## 3. Unsourced authority and vague relations

- Authority: "Studies have shown", "Research suggests", "It is widely accepted", "Experts agree", "A growing body of literature", "Numerous works" without citations.
- Relations: "is associated with", "is linked to", "is related to", "in connection with", "plays a role in" when the text knows the relation.

> Before: Numerous studies have shown that sleep deprivation is closely linked to impaired working memory.
>
> After: Sleep deprivation is associated with impaired working memory [TODO: cite the studies and state whether they show a causal effect].

## 4. Template rhythm

- Triads: "efficient, scalable, and robust"; three examples where one carries the point; three parallel sentences followed by a summary.
- Connectives: "Moreover", "Furthermore", "Additionally", "In addition", "Consequently" opening consecutive sentences; "First and foremost".
- Openings: "This study ... This study ... This study ..."; "We ... We ... We ...".
- Dashes: em dashes or spaced hyphens for asides in sentence after sentence.
- Hedge stacks: "may potentially", "could possibly suggest", "might arguably indicate", "it seems that ... may".

> Before: Moreover, the model is lightweight, fast, and efficient. Furthermore, it trains on a single GPU. Additionally, it converges within a few hours — far faster than the baselines — and may potentially transfer to other domains.
>
> After: The model trains on a single GPU and converges within a few hours, faster than the baselines. It may transfer to other domains.

The triad only repeated what the concrete sentences show, so it goes; the single hedge "may" keeps the original uncertainty.

## 5. Wordy constructions

- "serves as", "stands as", "acts as" where "is" fits; "boasts", "features", "offers" where "has" fits.
- "perform an analysis of" (analyze), "conduct an investigation into" (investigate), "make a comparison between" (compare), "provide a description of" (describe), "in order to" (to), "due to the fact that" (because), "it is possible that" (may).
- "with respect to" and "in terms of" as all-purpose joints.

## 6. Stock vocabulary

Watch these words, especially in groups. Each one is a signal, not a ban: choose the plain word that fits the sentence, or cut the word.

- Verbs that inflate a plain action: bolster, delve, elucidate, endeavor, foster, galvanize, harness, leverage (outside finance), navigate (figurative), showcase, spearhead, underscore, unveil.
- Nouns that dress up a plain thing: cornerstone, interplay, journey (figurative), landscape (figurative), nexus, realm, tapestry, testament.
- Adjectives that add no information: commendable, crucial, groundbreaking, holistic, intricate, meticulous, multifaceted, noteworthy, nuanced, paramount, pivotal, profound, seamless, vibrant.
- Connectives that repeat: additionally, furthermore, importantly, moreover, notably. Count them only when two or more appear in a short passage.
- Phrases: a deep dive, ever-evolving, game-changing, in the realm of, navigate the complexities.

Words such as robust, comprehensive, and key are signals only in figurative use. Keep their technical senses, such as "robust estimator" or "key-value store".

## 7. Template formatting

- "**Accuracy:** The model ..." labels before each item; bold or italic emphasis inside sentences.
- A bulleted list where the argument needs prose. A list of contributions at the end of an introduction is a convention in some fields; keep it there when the venue's papers use one.
- Title Case headings when the venue uses sentence case, or the reverse; emojis or arrows in headings.

## 8. Assistant residue and placeholders

- "Certainly!", "I hope this helps", "Sure, here is ...", "Here is the revised paragraph:", "Let me know if you would like ...".
- "As an AI language model", "As of my last update", "I do not have access to ...".
- "This version emphasizes ...", "The revised text now ...".
- "[insert reference]", "XX%", "Author et al. (Year)".

## 9. Translated-sounding prose

Frequent in English drafted from Chinese or Japanese:

- Stock openers: "With the rapid development of X, Y has attracted more and more attention"; "In recent years, more and more researchers ...".
- "plays an important role in", "has been widely used in many fields", "aims to solve the problem of".
- Vague results: "Experimental results show that the proposed method is effective" without saying how.
- Chains of "of": "the improvement of the performance of the model of the proposed method".
- Stacked passives: "it is found that ... is improved ... is obtained".

> Before: With the rapid development of deep learning, image segmentation has attracted more and more attention and has been widely used in many fields.
>
> After: Image segmentation has received growing attention as deep learning developed rapidly, and it is used in many fields [TODO: name the fields and cite evidence for both claims].

Both claims stay, marked for the evidence they need; nothing is supplied from memory.

## 10. Letters that bury the answer

- "We sincerely thank the reviewer for this insightful and valuable comment" before every answer.
- A restatement of the comment, then background, then the change in the last sentence.

> Before: We sincerely thank the reviewer for this insightful and valuable comment. We fully agree that the choice of baselines is an important aspect of any empirical study, and we have carefully considered this point. Following the reviewer's suggestion, we have added a comparison with two recent methods in Section 4.2.
>
> After: Thank you. We added a comparison with two recent methods in Section 4.2.
