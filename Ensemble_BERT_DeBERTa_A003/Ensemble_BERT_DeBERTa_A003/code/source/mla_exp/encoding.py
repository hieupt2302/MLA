"""Target-aware token budgeting, testable without torch or a GPU."""
def encode(tokenizer, row, context, max_length=512):
    prefix = tokenizer.encode(f"Type: {row['discourse_type']}\nTarget: ", add_special_tokens=False)
    target = tokenizer.encode(row["discourse_text"], add_special_tokens=False)
    special = tokenizer.num_special_tokens_to_add(pair=context)
    available = max_length - special - len(prefix)
    if available < 8:
        raise ValueError("Token budget cannot fit target")
    target_budget = available
    truncated = len(target) > target_budget
    if truncated:
        head = (target_budget + 1) // 2
        target = target[:head] + target[-(target_budget - head):]
    first = prefix + target
    second, context_truncated = None, False
    if context:
        prompt = tokenizer.encode("Prompt: " + row.get("assignment", ""), add_special_tokens=False)
        left = tokenizer.encode("Before: " + row.get("left_context", ""), add_special_tokens=False)
        right = tokenizer.encode("After: " + row.get("right_context", ""), add_special_tokens=False)
        remaining = max_length - special - len(first)
        prompt_budget = min(64, remaining // 3)
        p = prompt[:prompt_budget]
        remaining -= len(p)
        left_budget = min(len(left), remaining // 2)
        right_budget = min(len(right), remaining - left_budget)
        left_budget = min(len(left), remaining - right_budget)
        second = p + (left[-left_budget:] if left_budget else []) + right[:right_budget]
        context_truncated = len(second) < len(prompt) + len(left) + len(right)
    # Fast tokenizers do not all implement get_special_tokens_mask for pairs.
    # Use distinct sentinel IDs to locate the first sequence after the model's
    # actual special-token insertion; literal special tokens in text are safe.
    first_markers = [-10000-i for i in range(len(first))]
    second_markers = [-1000000-i for i in range(len(second))] if second is not None else None
    builder=getattr(tokenizer,'build_inputs_with_special_tokens',None)
    ids=builder(first,second) if builder else []
    layout=builder(first_markers,second_markers) if builder else []
    if len(ids) != len(first) + len(second or []) + special:
        # Generic fast tokenizers can install their special-token template in
        # the backend instead of overriding build_inputs_with_special_tokens.
        # Learn the template through the public sequence_ids interface.
        probe = tokenizer('x', text_pair='y' if context else None, add_special_tokens=True)
        sequences=probe.sequence_ids()
        built_ids, built_layout, built_types=[],[],[]
        inserted=set()
        for position, sequence in enumerate(sequences):
            type_id=probe.get('token_type_ids',[0]*len(sequences))[position]
            if sequence is None:
                built_ids.append(probe['input_ids'][position]); built_layout.append(probe['input_ids'][position]); built_types.append(type_id)
            elif sequence not in inserted:
                values, markers=(first,first_markers) if sequence==0 else (second,second_markers)
                built_ids.extend(values); built_layout.extend(markers); built_types.extend([type_id]*len(values)); inserted.add(sequence)
        ids,layout=built_ids,built_layout
    else:
        built_types=None
    first_set = set(first_markers)
    normal_positions = [i for i, value in enumerate(layout) if value in first_set]
    mask = [False] * len(ids)
    for i in normal_positions[len(prefix):len(first)]:
        mask[i] = True
    if not any(mask) or len(ids) > max_length:
        raise ValueError("Target disappeared or exceeded token budget")
    result = {"input_ids": ids, "attention_mask": [1] * len(ids)}
    if "token_type_ids" in tokenizer.model_input_names:
        result["token_type_ids"] = built_types if built_types is not None else tokenizer.create_token_type_ids_from_sequences(first, second)
    return result, mask, {"target_truncated": truncated, "context_truncated": context_truncated, "tokens": len(ids)}
