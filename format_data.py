"""Aggregate counts from the format/citation study, generated from the study databases.

No response text, prompts or trial rows are included. Regenerate with build_data.py.
"""

DESIGN = {'categories': {'Beauty': 10, 'Beverage': 10, 'Consumer Tech/CPG': 10, 'Grocery/Retail': 10},
 'cells': 2400,
 'collected': '2026-07-22',
 'engines': {'ChatGPT': 'gpt-5.5-2026-04-23', 'Claude': 'claude-sonnet-5', 'Perplexity': 'sonar'},
 'example_question': 'How many days does Sephora give customers to return a purchase?',
 'facts': 40,
 'formats': ['table', 'bullet', 'prose', 'diffuse_prose'],
 'reruns': 5}

CITATION_COUNTS = {'ChatGPT|bullet': [200, 200],
 'ChatGPT|diffuse_prose': [200, 198],
 'ChatGPT|prose': [200, 198],
 'ChatGPT|table': [200, 200],
 'Claude|bullet': [200, 200],
 'Claude|diffuse_prose': [200, 200],
 'Claude|prose': [200, 200],
 'Claude|table': [200, 200],
 'Perplexity|bullet': [200, 124],
 'Perplexity|diffuse_prose': [200, 110],
 'Perplexity|prose': [200, 107],
 'Perplexity|table': [200, 132]}

CORRECT_VALUE_PUBLISHED = {'bullet': [555, 519], 'diffuse_prose': [555, 521], 'prose': [555, 525], 'table': [555, 524]}

CORRECT_VALUE_CORRECTED = {'bullet': [555, 549], 'diffuse_prose': [555, 551], 'prose': [555, 555], 'table': [555, 554]}

SONAR_SLOT = {1: [160, 115, 124], 2: [160, 101, 115], 3: [160, 63, 94], 4: [160, 100, 119], 5: [160, 94, 122]}

SONAR_PAIRED_NAMED = [{'a': 'table', 'a_only': 47, 'b': 'diffuse_prose', 'b_only': 25, 'p': 0.012774595538064901, 'pairs': 200},
 {'a': 'bullet', 'a_only': 44, 'b': 'diffuse_prose', 'b_only': 30, 'p': 0.13017768031912758, 'pairs': 200},
 {'a': 'prose', 'a_only': 33, 'b': 'diffuse_prose', 'b_only': 36, 'p': 0.8099490529189248, 'pairs': 200},
 {'a': 'table', 'a_only': 48, 'b': 'prose', 'b_only': 23, 'p': 0.004065116124638666, 'pairs': 200},
 {'a': 'bullet', 'a_only': 48, 'b': 'prose', 'b_only': 31, 'p': 0.07116340869529121, 'pairs': 200},
 {'a': 'table', 'a_only': 42, 'b': 'bullet', 'b_only': 34, 'p': 0.42219110499231566, 'pairs': 200}]

SONAR_NAMED_OR_BRACKET_BY_FORMAT = {'bullet': [200, 154], 'diffuse_prose': [200, 137], 'prose': [200, 132], 'table': [200, 151]}

HARDER_COUNTS = {'ChatGPT|bullet': [200, 200],
 'ChatGPT|diffuse_prose': [200, 199],
 'ChatGPT|prose': [200, 199],
 'ChatGPT|table': [200, 200],
 'Claude|bullet': [200, 200],
 'Claude|diffuse_prose': [200, 200],
 'Claude|prose': [200, 200],
 'Claude|table': [200, 200]}

CONTRADICTION = {'near_duplicate': {'ChatGPT|bullet': {'hedged': 20},
                    'ChatGPT|diffuse_prose': {'hedged': 15},
                    'ChatGPT|prose': {'hedged': 17},
                    'ChatGPT|table': {'hedged': 20},
                    'Claude|bullet': {'hedged': 20},
                    'Claude|diffuse_prose': {'hedged': 15},
                    'Claude|prose': {'hedged': 17},
                    'Claude|table': {'hedged': 20},
                    'Perplexity|bullet': {'correct': 119, 'hedged': 48, 'unclear': 8, 'wrong': 25},
                    'Perplexity|diffuse_prose': {'correct': 122, 'hedged': 39, 'unclear': 13, 'wrong': 26},
                    'Perplexity|prose': {'correct': 115, 'hedged': 50, 'unclear': 9, 'wrong': 26},
                    'Perplexity|table': {'correct': 113, 'hedged': 48, 'unclear': 10, 'wrong': 29}},
 'subtle': {'ChatGPT|bullet': {'hedged': 25},
            'ChatGPT|diffuse_prose': {'hedged': 25},
            'ChatGPT|prose': {'hedged': 25},
            'ChatGPT|table': {'hedged': 25},
            'Claude|bullet': {'hedged': 25},
            'Claude|diffuse_prose': {'hedged': 25},
            'Claude|prose': {'hedged': 25},
            'Claude|table': {'hedged': 25},
            'Perplexity|bullet': {'correct': 120, 'hedged': 56, 'unclear': 12, 'wrong': 12},
            'Perplexity|diffuse_prose': {'correct': 109, 'hedged': 64, 'unclear': 11, 'wrong': 16},
            'Perplexity|prose': {'correct': 121, 'hedged': 55, 'unclear': 12, 'wrong': 12},
            'Perplexity|table': {'correct': 120, 'hedged': 44, 'unclear': 11, 'wrong': 25}}}

EXAMPLE_PASSAGES = {'bullet': {'outlet': 'The Household Record',
            'text': '- Sephora accepts returns within 30 days of purchase.\n'
                    '- Refunds go back to the original payment method.\n'
                    '- A receipt or order number is required to process the return.\n'
                    '- The policy applies to both in-store and online purchases.\n'
                    '- Opened or lightly used makeup, skincare, and fragrance can still be returned within '
                    'the 30-day window; only final sale items and gift cards are excluded.',
            'words': 66},
 'diffuse_prose': {'outlet': 'The Household Record',
                   'text': 'Refunds go back to the original payment method. A receipt or order number is '
                           'required to process the return. Sephora accepts returns within 30 days of '
                           'purchase. Opened or lightly used makeup, skincare, and fragrance can still be '
                           'returned within the 30-day window; only final sale items and gift cards are '
                           'excluded. The policy applies to both in-store and online purchases.',
                   'words': 61},
 'prose': {'outlet': 'The Household Record',
           'text': 'Sephora gives shoppers a 30-day window to return a purchase, with refunds issued back to '
                   'the original payment method. A receipt or order number is required to process the '
                   'request, and the policy covers both in-store and online purchases equally. Opened or '
                   'lightly used makeup, skincare, and fragrance can still be returned within the 30-day '
                   'window; only final sale items and gift cards are excluded.',
           'words': 65},
 'table': {'outlet': 'The Household Record',
           'text': '| Field | Detail |\n'
                   '|---|---|\n'
                   '| Retailer | Sephora |\n'
                   '| Return window | 30 days |\n'
                   '| Refund method | Original payment method |\n'
                   '| Proof required | Receipt or order number |\n'
                   '| Context | The policy applies to both in-store and online purchases |\n'
                   '| Context | Opened or lightly used makeup, skincare, and fragrance can still be returned '
                   'within the 30-day window; only final sale items and gift cards are excluded |',
           'words': 57}}

