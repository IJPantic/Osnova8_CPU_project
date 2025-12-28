"""
Created on 15. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 16. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 17. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 19. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 22. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 24. December, 2025. by Ivan Jonjic (IJPantic on github)
Updated on 28. December, 2025. by Ivan Jonjic (IJPantic on github)
"""

"""
This program simulates 'Osnova8' CPU.
"""

#CPU values
pfl = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
pfh = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
ra = [0, 1, 0, 0, 0, 0, 0, 0]
rb = [1, 0, 0, 0, 0, 0, 0, 0]
rc = [0, 0, 0, 0, 0, 0, 0, 0]
resr = [0, 0, 0, 0, 0, 0, 0, 0]
dvr = [1, 1, 0, 1, 0, 0, 1, 0]
ps = [0, 0, 0, 0, 1, 0, 0, 1]
sct = [[0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
bus = [0, 0, 0, 0, 0, 0, 0, 0]
ir = [0, 0, 0, 0, 0, 0, 0, 0]
add = 0
int_state_internal = 1
int_state_external = 1

#memory page values
memory_page_0 = {
	0	:	[0, 0, 0, 0, 0, 0, 0, 0],
}
memory_page_1 = {}
memory_page_2 = {}
memory_page_3 = {}
memory_page_4 = {}
memory_page_5 = {}
memory_page_6 = {}
memory_page_7 = {}
memory_page_8 = {}
memory_page_9 = {}
memory_page_a = {}
memory_page_b = {}
memory_page_c = {}
memory_page_d = {}
memory_page_e = {}
memory_page_f = {}

#memory sectors
memory_sectors = {
	0	:	memory_page_0,
	1	:	memory_page_1,
	2	:	memory_page_2,
	3	:	memory_page_3,
	4	:	memory_page_4,
	5	:	memory_page_5,
	6	:	memory_page_6,
	7	:	memory_page_7,
	8	:	memory_page_8,
	9	:	memory_page_9,
	10	:	memory_page_a,
	11	:	memory_page_b,
	12	:	memory_page_c,
	13	:	memory_page_d,
	14	:	memory_page_e,
	15	:	memory_page_f,
}

#Number's base converters
def bin_to_dec(bin_val):
	dec_val = 0
	place = -1
	for bin_index in range(len(bin_val)-1, -1, -1):
		place += 1
		dec_val += bin_val[bin_index] * (2**place)
	return dec_val

def word_expand(a, size):
	tmp = a
	for bit_num in range(size - len(a)):
		tmp.insert(0, 0)
	return tmp

#Binary operations
def log_not(a):
	tmp = []
	for bit_num in range(len(a)):
		bit = a[bit_num]
		if bit:
			tmp.append(0)
		else:
			tmp.append(1)
	return tmp

def log_and(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a and bit_b:
			tmp.append(1)
		else:
			tmp.append(0)
	return tmp

def log_or(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a or bit_b:
			tmp.append(1)
		else:
			tmp.append(0)
	return tmp

def log_nand(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a and bit_b:
			tmp.append(0)
		else:
			tmp.append(1)
	return tmp

def log_nor(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a or bit_b:
			tmp.append(0)
		else:
			tmp.append(1)
	return tmp

def log_xor(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a and not bit_b or bit_b and not bit_a:
			tmp.append(1)
		else:
			tmp.append(0)
	return tmp

def log_xnor(a, b):
	tmp = []
	for bit_num in range(len(a)):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		if bit_a and not bit_b or bit_b and not bit_a:
			tmp.append(0)
		else:
			tmp.append(1)
	return tmp

def log_add(a, b):
	tmp = []
	carry = 0
	for bit_num in range(len(a)-1, -1, -1):
		bit_a = a[bit_num]
		bit_b = b[bit_num]
		val = bit_a + bit_b + carry
		if val == 1:
			tmp.insert(0, 1)
			carry = 0
		elif val == 2:
			tmp.insert(0, 0)
			carry = 1
		elif val == 3:
			tmp.insert(0, 1)
			carry = 1
		else:
			tmp.insert(0, 0)
			carry = 0
	return tmp

def log_sub(a, b):
	tmp = log_add(a, log_add(log_not(b), word_expand([1], len(a))))
	return tmp

#ALU operation table
alu_log = {
	"[0, 0, 0, 0]":	log_not(ra),
	"[0, 0, 0, 1]":	log_nor(ra, rb),
	"[0, 0, 1, 0]":	log_and(log_not(ra), rb),
	"[0, 0, 1, 1]":	[0, 0, 0, 0, 0, 0, 0, 0],
	"[0, 1, 0, 0]":	log_nand(ra, rb),
	"[0, 1, 0, 1]":	log_not(rb),
	"[0, 1, 1, 0]":	log_xor(ra, rb),
	"[0, 1, 1, 1]":	log_and(ra, log_not(rb)),
	"[1, 0, 0, 0]":	log_or(log_not(ra), rb),
	"[1, 0, 0, 1]":	log_xnor(ra, rb),
	"[1, 0, 1, 0]":	rb,
	"[1, 0, 1, 1]":	log_and(ra, rb),
	"[1, 1, 0, 0]":	[0, 0, 0, 0, 0, 0, 0, 1],
	"[1, 1, 0, 1]":	log_or(ra, log_not(rb)),
	"[1, 1, 1, 0]":	log_or(ra, rb),
	"[1, 1, 1, 1]":	ra,
}

alu_ari = {
	"[0, 0, 0, 0]":	ra,
	"[0, 0, 0, 1]":	log_or(ra, rb),
	"[0, 0, 1, 0]":	log_or(ra, log_not(rb)),
	"[0, 0, 1, 1]":	[1, 1, 1, 1, 1, 1, 1, 1],
	"[0, 1, 0, 0]":	log_add(ra, log_and(ra, log_not(rb))),
	"[0, 1, 0, 1]":	log_add(log_or(ra, rb), log_and(ra, log_not(rb))),
	"[0, 1, 1, 0]":	log_sub(log_sub(ra, rb), [1, 1, 1, 1, 1, 1, 1, 1]),
	"[0, 1, 1, 1]":	log_sub(log_and(ra, log_not(rb)), [1, 1, 1, 1, 1, 1, 1, 1]),
	"[1, 0, 0, 0]": log_add(ra, log_and(ra, rb)),
	"[1, 0, 0, 1]":	log_add(ra, rb),
	"[1, 0, 1, 0]":	log_add(log_or(ra, log_not(rb)), log_and(ra, rb)),
	"[1, 0, 1, 1]":	log_sub(log_and(ra, rb), [1, 1, 1, 1, 1, 1, 1, 1]),
	"[1, 1, 0, 0]":	log_add(ra, ra),
	"[1, 1, 0, 1]":	log_add(log_or(ra, rb), ra),
	"[1, 1, 1, 0]":	log_add(log_or(ra, log_not(rb)), ra),
	"[1, 1, 1, 1]":	log_sub(ra, [1, 1, 1, 1, 1, 1, 1, 1]),
}

alu_ari_carry = {
	"[0, 0, 0, 0]":	log_add(ra, [0, 0, 0, 0, 0, 0, 0, 1]),
	"[0, 0, 0, 1]":	log_add(log_or(ra, rb), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[0, 0, 1, 0]":	log_add(log_or(ra, log_not(rb)), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[0, 0, 1, 1]":	[0, 0, 0, 0, 0, 0, 0, 0],
	"[0, 1, 0, 0]":	log_add(log_add(ra, log_and(ra, log_not(rb))), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[0, 1, 0, 1]":	log_add(log_add(log_or(ra, rb), log_and(ra, log_not(rb))), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[0, 1, 1, 0]":	log_sub(ra, rb),
	"[0, 1, 1, 1]":	log_and(ra, log_not(rb)),
	"[1, 0, 0, 0]": log_add(log_add(ra, log_and(ra, rb)), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 0, 0, 1]":	log_add(log_add(ra, rb), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 0, 1, 0]":	log_add(log_add(log_or(ra, log_not(rb)), log_and(ra, rb)), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 0, 1, 1]":	log_and(ra, rb),
	"[1, 1, 0, 0]":	log_add(log_add(ra, ra), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 1, 0, 1]":	log_add(log_add(log_or(ra, rb), ra), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 1, 1, 0]":	log_add(log_add(log_or(ra, log_not(rb)), ra), [0, 0, 0, 0, 0, 0, 0, 1]),
	"[1, 1, 1, 1]":	ra,
}

#Opcodes
def opc_jmp():
	global bus
	global pfl
	global pfh
	global ps
	read_adr = bin_to_dec(ps[6:])
	write_adr = bin_to_dec(ps[4:][:2])
	pfl[write_adr] = pfl[read_adr]
	pfh[write_adr] = pfh[read_adr]

def opc_sct():
	global bus
	global sct
	sct = bus

def opc_ps():
	global bus
	global ps
	ps = bus

def opc_pfl():
	global bus
	global pfl
	global ps
	write_adr = bin_to_dec(ps[4:][:2])
	pfl[write_adr] = bus

def opc_pfh():
	global bus
	global pfh
	global ps
	write_adr = bin_to_dec(ps[4:][:2])
	pfh[write_adr] = bus

def opc_resr():
	global bus
	global resr
	resr = bus

def opc_add():
	global bus
	global add
	global ps
	global add
	ps_val = bin_to_dec(ps[6:])
	print(ps_val)
	write_adr = bin_to_dec(pfh[ps_val] + pfl[ps_val])
	memory_sectors[bin_to_dec(sct[ps_val][4:])][write_adr] = bus

def opc_dvrr():
	global dvr
	dvr = [0, 0, 0, 0, 0, 0, 0, 0]

def opc_dvrl():
	global dvr
	global ir
	dvr = ir[4:]

def opc_dvrh():
	global dvr
	global ir
	dvr = ir[:4]

def opc_ra():
	global bus
	global ra
	ra = bus

def opc_rb():
	global bus
	global rb
	rb = bus

def opc_rc():
	global bus
	global rc
	rc = bus

def opc_intsi():
	global int_state_internal
	int_state_internal = 0

def opc_intso():
	global int_state_external
	int_state_external = 0 #unfinished

def opc_inte():
	global int_state_internal
	int_state_internal = 1

#Arguments
def arg_alu():
	global bus
	global dvr
	global alu_log
	global alu_ari
	global alu_ari_carry
	operation = str(dvr[4:])
	carryin = dvr[3]
	mode = dvr[2]
	if mode:
		bus = alu_log[operation]
	else:
		if carryin:
			bus = alu_ari[operation]
		else:
			bus = alu_ari_carry[operation]

def arg_sctps():
	global bus
	global sct
	global ps
	read_adr = bin_to_dec(ps[6:])
	bus = ps[4:] + sct[read_adr][4:]

def arg_rc():
	global bus
	global rc
	bus = rc

def arg_pfl():
	global bus
	global pfl
	global ps
	read_adr = bin_to_dec(ps[6:])
	bus = pfl[read_adr]

def arg_pfh():
	global bus
	global pfh
	global ps
	read_adr = bin_to_dec(ps[6:])
	bus = pfh[read_adr]

def arg_resr():
	global bus
	global resr
	bus = resr

def arg_add():
	global bus
	global add
	global ps
	global add
	ps_val = bin_to_dec(ps[4:])
	read_adr = bin_to_dec(pfh[ps_val] + pfl[ps_val])
	memory_sectors[bin_to_dec(sct[ps_val][4:])][read_adr] = bus

def arg_dvr():
	global bus
	global dvr
	bus = dvr

#Instructions table
opcodes = {
	"[0, 0, 0, 0]":	opc_jmp,
	"[0, 0, 0, 1]":	opc_sct,
	"[0, 0, 1, 0]":	opc_ps,
	"[0, 0, 1, 1]":	opc_pfl,
	"[0, 1, 0, 0]":	opc_pfh,
	"[0, 1, 0, 1]":	opc_resr,
	"[0, 1, 1, 0]":	opc_add,
	"[0, 1, 1, 1]":	opc_dvrr,
	"[1, 0, 0, 0]": opc_dvrl,
	"[1, 0, 0, 1]":	opc_dvrh,
	"[1, 0, 1, 0]":	opc_ra,
	"[1, 0, 1, 1]":	opc_rb,
	"[1, 1, 0, 0]":	opc_rc,
	"[1, 1, 0, 1]":	opc_intsi,
	"[1, 1, 1, 0]":	opc_intso,
	"[1, 1, 1, 1]":	opc_inte,
}

arguments = {
	"[0, 0, 0, 0]":	arg_alu,
	"[0, 0, 0, 1]":	arg_sctps,
	"[0, 0, 1, 0]":	arg_rc,
	"[0, 0, 1, 1]":	arg_pfl,
	"[0, 1, 0, 0]":	arg_pfh,
	"[0, 1, 0, 1]":	arg_resr,
	"[0, 1, 1, 0]":	arg_add,
	"[0, 1, 1, 1]":	arg_dvr,
}

#CPU instruction execution loop
executing = True
while executing:
	arg_dvr()
	opc_add()
	arg_add()
	print(bus)
	a = input()

