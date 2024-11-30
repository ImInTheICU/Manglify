import random, os, ast

source_path: str = input("Enter source file -> ")

if not os.path.exists(source_path):
    input("File does not exist.")

output_dir: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
output_file: str = os.path.join(output_dir, f"{random.randint(1000, 9999)}_{os.path.basename(source_path)}")

chunked_dict: dict[int, str] = {} 
used_chunks: set[int] = set()
used_names: set[int] = set()
dict_key: int = random.randint(1000, 9999)
chunk_amount: int = random.choice([8, 16, 32])
full_chunk: str = ""

def xor_encrypt_decrypt(input_string: str, key: int) -> str:
    input_bytes = input_string.encode()
    key_bytes = bytearray(str(key), 'utf-8') 
    output_bytes = bytearray()
    
    for i in range(len(input_bytes)):
        output_bytes.append(input_bytes[i] ^ key_bytes[i % len(key_bytes)])
    
    return output_bytes.hex()

def to_octal_escape(string: str) -> str:
    return ''.join(f'\\{oct(ord(char))[2:]}' for char in string)

def c_encode(raw_chunk: str) -> tuple[int, str]:
    def _get_index() -> int:
        _index: int = random.randint(100000, 999999)

        while _index in used_chunks:
            _index: int = random.randint(100000, 999999)

        used_chunks.add(_index)
        
        return _index
        
    def _do_chunk(passed_chunk: str) -> str:
        _level: int = random.randint(1, 5)
        
        if _level == 1:
            # Hex
            return _level, passed_chunk.encode().hex(' ')
        elif _level == 2:
            # Ordinal
            return _level, ' '.join(str(ord(i)) for i in passed_chunk)
        elif _level == 3:
            # Binary
            return _level, ''.join(format(ord(char), '08b') for char in passed_chunk)
        elif _level == 4:
            # ROT13
            return _level, ''.join(chr((ord(c) - 65 + 13) % 26 + 65) if 'A' <= c <= 'Z' else chr((ord(c) - 97 + 13) % 26 + 97) if 'a' <= c <= 'z' else c for c in passed_chunk)
        elif _level == 5:
            # AtBash
            def atbash(c: str) -> str:
                if 'a' <= c <= 'z':
                    return chr(219 - ord(c))  # 'a' + 'z' = 219
                elif 'A' <= c <= 'Z':
                    return chr(155 - ord(c))  # 'A' + 'Z' = 155
                return c
            return _level, ''.join(atbash(c) for c in passed_chunk)
    
    level_used, chunk = _do_chunk(raw_chunk)        
    index: int = _get_index()

    return int(f"{level_used}{index}"), chunk

def get_unique_name() -> str:
    while True:
        name: int = random.randint(100000, 999999)

        if name not in used_names:
            used_names.add(name) 
            return f"_{name}"

def get_import_tree(code: str):
    tree = ast.parse(code)
    
    imports = []
    tree_output = []

    fallback_builtin = "__annotations__"
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name
                
                if alias.asname:
                    import_name = alias.asname 
                else:
                    import_name = module_name  
                
                try:
                    module_ref = __import__(module_name)
                    module_name_attr = f"{module_ref.__name__}.__name__"
                except ImportError:
                    module_name_attr = fallback_builtin
                
                imports.append(f"import {module_name} as {import_name}" if alias.asname else f"import {module_name}")
                tree_output.append(import_name)

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                module_name = node.module
                
                if alias.asname:
                    import_name = alias.asname 
                else:
                    import_name = alias.name 
                
                try:
                    module_ref = __import__(module_name)
                    module_name_attr = f"{module_ref.__name__}.__name__"
                except ImportError:
                    module_name_attr = fallback_builtin
                
                imports.append(f"from {module_name} import {import_name}")
                tree_output.append(import_name)

    return imports, tree_output

with open(file=source_path, mode='r', encoding='utf-8') as f:
    while (chunk := f.read(chunk_amount)):
        index, cchunk = c_encode(raw_chunk=chunk)
        chunked_dict[index] = xor_encrypt_decrypt(input_string=cchunk, key=dict_key)
        full_chunk += chunk

imports, tree = get_import_tree(full_chunk)

final_names: list = [
    get_unique_name(), # 0
    get_unique_name(), # 1
    get_unique_name(), # 2
    get_unique_name(), # 3
    get_unique_name(), # 4
    get_unique_name(), # 5
    get_unique_name(), # 6
    get_unique_name(), # 7
    get_unique_name(), # 8
    get_unique_name(), # 9
    get_unique_name(), # 10
    get_unique_name(), # 11
    get_unique_name(), # 12
    get_unique_name(), # 13
    get_unique_name(), # 14
    get_unique_name(), # 15
    get_unique_name(), # 16
    get_unique_name(), # 17
    get_unique_name(), # 18
    get_unique_name(), # 19
    get_unique_name(), # 20
    get_unique_name(), # 21
    get_unique_name(), # 22
    get_unique_name(), # 23
    get_unique_name(), # 24
    get_unique_name(), # 25
    get_unique_name(), # 26
    get_unique_name(), # 27
    get_unique_name(), # 28
    get_unique_name(), # 29
    get_unique_name(), # 30
    get_unique_name(), # 31
    get_unique_name(), # 32
    get_unique_name(), # 33
    get_unique_name(), # 34
    get_unique_name(), # 35
]
const_assignments: list = [
    (final_names[0], chunked_dict),
    (final_names[7], 'bytes'),
    (final_names[8], 'bytearray'),
    (final_names[9], 'str'),
    (final_names[10], 'range'),
    (final_names[11], 'len'),
    (final_names[12], 'ord'),
    (final_names[13], 'chr'),
    (final_names[14], 'sum'),
    (final_names[15], 'int'),
    (final_names[16], 'isinstance'),
    (final_names[21], '__import__'),
    (final_names[22], 'dict'),
    (final_names[24], 'abs'),
    (final_names[25], 'globals'),
    (final_names[30], 'exec'),
    (final_names[35], 'globals'),
]

random.shuffle(const_assignments)

final: str = f"""
{";".join([imp for imp in imports])};{";".join([f"{name} = {value}" for name, value in const_assignments])}
{f"\n{final_names[23]} = {str(tree).replace("'", "")}; ({final_names[23]})"}
{final_names[19]} = lambda {final_names[26]}: {final_names[30]}(''.join({final_names[2]}({final_names[15]}({final_names[9]}({final_names[27]})[:1]), {final_names[1]}({final_names[6]}, {final_names[26]})) for {final_names[27]}, {final_names[6]} in {final_names[0]}.items()), {final_names[22]}())
{final_names[20]} = lambda {final_names[28]}: ({final_names[21]}('{to_octal_escape(f"gc{' ' * random.randint(5, 25)}")}'.strip()).collect())!=({final_names[28]}) if {final_names[21]}('{to_octal_escape(f'random{' ' * random.randint(5, 25)}')}'.strip()).randint({final_names[15]}('{to_octal_escape(f"1{' ' * random.randint(5, 25)}")}'),{final_names[15]}('{to_octal_escape(f"10{' ' * random.randint(5, 25)}")}')) == {random.randint(1,10)} else {final_names[21]}('{to_octal_escape(f"gc{' ' * random.randint(5, 25)}")}'.strip()).get_objects()

def {final_names[1]}({final_names[3]},{final_names[4]}):
	{final_names[31]}='{to_octal_escape(f"utf-8{' ' * random.randint(5, 25)}")}'.strip();{final_names[32]}=lambda {final_names[17]}:{final_names[7]}.fromhex({final_names[17]});{final_names[33]}=lambda {final_names[4]}:{final_names[8]}({final_names[9]}({final_names[4]}),{final_names[31]});{final_names[34]}=lambda x:(lambda y:y+42)(x*3);K=lambda x:(lambda y:y[::-1])({final_names[9]}(x));L=lambda:(lambda p:(lambda q:q*2)(p+7))(100);M=lambda z:z**3-10*z+7;Q={final_names[34]}(23);R=K(12);S=L();T=M(10);N=lambda a1b2z,z2b1:{final_names[8]}([a1b2z[{final_names[8]}]^z2b1[{final_names[8]}%{final_names[11]}(z2b1)]for {final_names[8]} in {final_names[10]}({final_names[11]}(a1b2z))]);C=(lambda a:a+1)(5);E=(lambda x:x*2-3)(7);F=(lambda y:y//2+10)(20)
	if C>10:F=E*2
	else:E=C+F
	def O(input_value):
		{final_names[8]}=input_value;E=0
		for C in {final_names[10]}(0,{final_names[11]}({final_names[8]}),2):E+={final_names[12]}({final_names[8]}[C])-{final_names[12]}({final_names[8]}[C-1])if C>0 else 0
		return E
	O('{os.urandom(random.randint(32,64)).hex()}');P=lambda {final_names[18]}:{final_names[18]}.decode({final_names[31]});return P(N({final_names[32]}({final_names[3]}),{final_names[33]}({final_names[4]})))

def {final_names[2]}({final_names[5]},{final_names[6]}):
	I='z';H='a';G='A';C='';K=lambda x:(lambda y:(lambda z:z(y))(M(y)))({final_names[25]}().get('y',None));M=lambda x:x[::-1];N={final_names[12]}(G)+{final_names[12]}('B')
	def O(x):return(x*{random.randint(9, 99)}+N)%{random.randint(100, 999)}
	def P(x):return {final_names[14]}([{final_names[15]}({final_names[12]})for {final_names[12]} in {final_names[9]}(x)])+O({random.randint(1000, 9999)})
	def Q({final_names[6]}):{final_names[9]}=C.join({final_names[13]}({final_names[12]}(C)+{random.randint(9, 99)})for C in {final_names[6]});return {final_names[9]}[::-1]
	def R(x):
		if {final_names[16]}(x,{final_names[7]}):return C.join([{final_names[13]}({final_names[12]}^{random.randint(1, 9)})for {final_names[12]} in x])
		elif {final_names[16]}(x,{final_names[9]}):return C.join([{final_names[13]}({final_names[12]}(C)+{random.randint(9, 99)}^{random.randint(-100,100)})for C in x])
		else:return x[::-1]
	def S(x):x={final_names[12]}(H)+{final_names[12]}(I);return {final_names[13]}(x%{random.choice([128, 256])})
	def V(x):return {final_names[14]}([{final_names[15]}({final_names[12]})for {final_names[12]} in {final_names[9]}({final_names[24]}(x))])
	def T({final_names[6]}):return C.join([{final_names[13]}({final_names[12]}(C)+{random.randint(9, 99)})for C in {final_names[6]}])[::-1]
	V({random.randint(1000, 9999)});K=lambda x:{final_names[7]}.fromhex(x).decode('utf-8')if {final_names[5]}==1 else C.join({final_names[13]}({final_names[15]}({final_names[12]}))for {final_names[12]} in {final_names[6]}.split())if {final_names[5]}==2 else C.join({final_names[13]}({final_names[15]}({final_names[6]}[{final_names[12]}:{final_names[12]}+8],2))for {final_names[12]} in {final_names[10]}(0,{final_names[11]}({final_names[6]}),8))if {final_names[5]}==3 else C.join([{final_names[13]}(({final_names[12]}(C)-65-13)%26+65)if G<=C<='Z'else {final_names[13]}(({final_names[12]}(C)-97-13)%26+97)if H<=C<=I else C for C in {final_names[6]}])if {final_names[5]}==4 else C.join([{final_names[13]}(219-{final_names[12]}(C))if H<=C<=I else {final_names[13]}(155-{final_names[12]}(C))if G<=C<='Z'else C for C in {final_names[6]}])if {final_names[5]}==5 else None;U=P(101);W=S(256);X=Q({final_names[6]});L=T({final_names[6]})
	if U>{random.randint(1000, 9999)}:L=L[::-1]
	return K({final_names[6]})if {final_names[16]}({final_names[6]},{final_names[9]})else R({final_names[9]}({final_names[5]}))

for {final_names[29]} in range({final_names[15]}('{to_octal_escape(f"1000{' ' * random.randint(5, 25)}")}'.strip()), {final_names[15]}('{to_octal_escape(f"{' ' * random.randint(5, 25)}9999")}'.strip())):
    try: {final_names[35]}().get('{final_names[19]}', None)( {final_names[29]} )
    except: {final_names[35]}().get('{final_names[20]}', None)( {final_names[29]} )

            """.strip()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(file=output_file, mode='w', encoding='utf-8') as f:
    f.write(final)

print(f"File has been saved to {output_file}.")
