# An implementation of the Huffman coding algorithm

class Tree:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({self.left}_{self.right})"

    @property
    def children(self):
        return (self.left, self.right)
    
def get_frequency(string) -> dict:
    freq = {}
    for c in string:
        freq[c] = freq.get(c, 0) + 1
    return dict(sorted(freq.items(), key = lambda x: x[1], reverse=True))

def get_tree(frequencies) -> Tree:
    node_order = list(frequencies.items())
    while len(node_order) > 1:
        (node1, freq1) = node_order.pop()
        (node2, freq2) = node_order.pop()
        node = Tree(node1, node2)
        node_order.append((node, freq1+freq2))
        node_order.sort(key = lambda x: x[1], reverse=True)
    tree_head_node = node_order[0][0]
    return tree_head_node

def get_huffman_encoding_table(node, bin_string="") -> dict:
    if type(node) is str:
        return {node: bin_string}
    d = {}
    (l, r) = node.children
    d.update(get_huffman_encoding_table(l, bin_string+"0"))
    d.update(get_huffman_encoding_table(r, bin_string+"1"))
    return d

def huffman_encode(string) -> dict:
    huffman_lookup = get_huffman_encoding_table(get_tree(get_frequency(string)))
    bin_string = ''
    for char in string:
        bin_string += huffman_lookup[char]
    return {'encoded':bin_string, 'tree':huffman_lookup}

def huffman_decode(encoded_data, huffman_lookup) -> str:
    decoded_data = current_code = str()
    for bit in encoded_data:
        current_code += bit
        for char, code in huffman_lookup.items():
            if code == current_code:
                decoded_data += char
                current_code = str()
                break
    return decoded_data

# demonstration
if __name__ == '__main__':
    uncompressed = input('\nEnter string to compress: ')
    uncompressed_bin = str().join(format(ord(char)-48, 'b').zfill(8) for char in uncompressed) # ascii

    output = huffman_encode(uncompressed)
    compressed_bin = output['encoded']
    tree = output['tree']

    decompressed = huffman_decode(compressed_bin, tree)
    compression_rate = round((100 - ((len(compressed_bin)/len(uncompressed_bin))*100)), 2)
    
    print()
    print(f'-> Input string:                     {uncompressed}')
    print(f'-> Decompressed output:              {decompressed}')
    print(f'-> Huffman encoding table:           {tree}')
    print(f'-> Original amount of bits:          {len(uncompressed_bin)}')
    print(f'-> Amount of bits after compression: {len(compressed_bin)}')
    print(f'-> Compression rate:                 {compression_rate}%')
    print()