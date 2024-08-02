def Benchmark(gguf_model, max_tokens, temperature, device):
        toks = [gguf_model.tokenizer.bos_id()]
        start_pos = 0
        start_time = time.time()
        for i in range(max_tokens):
            start_pos_var = 0 if start_pos == 0 else Variable("start_pos", 1, 1024).bind(start_pos)
            if isinstance(start_pos_var, Variable):
                start_pos_val = start_pos_var.val 
            else:
                start_pos_val = start_pos_var
            tok_tensor = gguf_model.model(Tensor([toks[start_pos:]], device=device), start_pos_val, temperature)
            tok_tensor.realize() #ISSUE IS WHILE REALIZE
            tok = tok_tensor.item()

            toks.append(tok)
            start_pos += 1
            decoded_output = gguf_model.tokenizer.decode(toks)
            print(decoded_output)
            current_time = time.time()
            elapsed_time = current_time - start_time
            tokens_per_sec = (i + 1) / elapsed_time
            print(f"Token {i + 1}/{max_tokens}: {decoded_output[-len(gguf_model.tokenizer.decode([tok])):]}")
            print(f"Time elapsed: {elapsed_time:.2f} seconds, Tokens/sec: {tokens_per_sec:.2f}")

        total_time = time.time() - start_time
        print(f"Generated {max_tokens} tokens in {total_time:.2f} seconds ({tokens_per_sec:.2f} tokens/sec)")

        return gguf_model.tokenizer.decode(toks)

