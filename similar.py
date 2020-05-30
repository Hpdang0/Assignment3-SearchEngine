import hashlib

def Similarity(dict1, dict2, threshold, cache1 = None, cache2 = None):
    sim1 = create_simhash(dict1) if cache1 is None else cache1
    sim2 = create_simhash(dict2) if cache2 is None else cache2

    sim_val = _compute_similarity(sim1, sim2)

    if sim_val >= threshold:
        return True, sim1, sim2

    return False, sim1, sim2

    
def _compute_similarity(hash1, hash2):
    # Retuns the % of similarity between two hashes
    total_size = len(hash1)
    similar = 0
    for i in range(total_size):
        if hash1[i] == hash2[i]:
            similar += 1
    
    return similar/total_size


def create_simhash(words_dict):
    hash_digest_size = 64
    
    weights = []
    for i in range(hash_digest_size * 8):
        weights.append(int())

    for word in words_dict:
        hash = hashlib.blake2b(digest_size=hash_digest_size)
        # print('Working with: {}'.format(word))
        hash.update(word.encode('utf-8'))
        hashed = hash.digest()
        hashed_bytes = ensure_padding(''.join(format(int(b), 'b') for b in hashed), hash.digest_size * 8)
        # print(hashed_bytes)
        # print('>> Bytes: {}'.format(hashed_bytes))

        for i in range(hash.digest_size * 8):
            if bool(int(hashed_bytes[i])):
                weights[i] += words_dict[word][0]
            else:
                weights[i] -= words_dict[word][0]
        
    return normalize_weights(weights)


def ensure_padding(hashed_bytes, total_size):
    if len(hashed_bytes) >= total_size:
        return hashed_bytes
    
    extra_padding = total_size - len(hashed_bytes)    
    return '0' * extra_padding + hashed_bytes

def normalize_weights(weights):
    normalized = weights
    for i in range(len(normalized)):
        if normalized[i] > 0:
            normalized[i] = 1
        else:
            normalized[i] = 0
    
    return normalized