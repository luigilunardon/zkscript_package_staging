import sys, os, json, argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from tx_engine import Script, Context

from elliptic_curves.instantiations.mnt4_753.mnt4_753 import mnt4_753 as mnt4_753_curve, Fr

from zkscript.bilinear_pairings.mnt4_753.mnt4_753 import mnt4_753
from zkscript.util.utility_scripts import nums_to_script

q = mnt4_753_curve.q
r = mnt4_753_curve.r
g1 = mnt4_753_curve.g1
g2 = mnt4_753_curve.g2
val_miller_loop = mnt4_753_curve.val_miller_loop
exp_miller_loop = mnt4_753_curve.exp_miller_loop

# Utility functions for the tests
def generate_verify(z) -> Script:
    out = Script()
    for ix, el in enumerate(z.to_list()[::-1]):
        out += nums_to_script([el])
        if ix != len(z.to_list())-1:
            out += Script.parse_string('OP_EQUALVERIFY') 
        else:
            out += Script.parse_string('OP_EQUAL')

    return out

def generate_unlock(z) -> Script:
    out = nums_to_script(z.to_list())

    return out

# Json dictionary of the outputs
tests = [
    'triple pairing',
]

scripts = {test : {} for test in tests} 

type_of_script = [
    'unlocking',
    'locking script cleaning constants'
]

def test_triple_pairing():
    P1 = g1.multiply(n=Fr.generate_random_point().x)
    while P1.is_infinity():
        P1 = g1.multiply(n=Fr.generate_random_point().x)
    P2 = g1.multiply(n=Fr.generate_random_point().x)
    while P2.is_infinity():
        P2 = g1.multiply(n=Fr.generate_random_point().x)
    P3 = g1.multiply(n=Fr.generate_random_point().x)
    while P3.is_infinity():
        P3 = g1.multiply(n=Fr.generate_random_point().x)
    Q1 = g2.multiply(n=Fr.generate_random_point().x)
    while Q1.is_infinity():
        Q1 = g2.multiply(n=Fr.generate_random_point().x)
    Q2 = g2.multiply(n=Fr.generate_random_point().x)
    while Q2.is_infinity():
        Q2 = g2.multiply(n=Fr.generate_random_point().x)
    Q3 = g2.multiply(n=Fr.generate_random_point().x)
    while Q3.is_infinity():
        Q3 = g2.multiply(n=Fr.generate_random_point().x)

    output = mnt4_753_curve.triple_pairing(P1,P2,P3,Q1,Q2,Q3)
    
    unlock = mnt4_753.triple_pairing_input(
        P1=P1.to_list(),
        P2=P2.to_list(),
        P3=P3.to_list(),
        Q1=Q1.to_list(),
        Q2=Q2.to_list(),
        Q3=Q3.to_list(),
        lambdas_Q1_exp_miller_loop=[list(map(lambda s: s.to_list(),el)) for el in Q1.get_lambdas(exp_miller_loop)],
        lambdas_Q2_exp_miller_loop=[list(map(lambda s: s.to_list(),el)) for el in Q2.get_lambdas(exp_miller_loop)],
        lambdas_Q3_exp_miller_loop=[list(map(lambda s: s.to_list(),el)) for el in Q3.get_lambdas(exp_miller_loop)],
        miller_output_inverse=mnt4_753_curve.triple_miller_loop_on_twisted_curve(P1,P2,P3,Q1,Q2,Q3,'quadratic').invert().to_list()
    )
    
    # Check correct evaluation
    lock = mnt4_753.triple_pairing(modulo_threshold=1,check_constant=True,clean_constant=True)
    lock += generate_verify(output)

    context = Context(script = unlock + lock)
    assert(context.evaluate() and (len(context.get_stack()) == 1) and (len(context.get_altstack()) == 0))

    # Save scripts
    scripts[tests[0]][type_of_script[0]] = unlock
    scripts[tests[0]][type_of_script[1]] = lock

    return

parser = argparse.ArgumentParser("Triple pairing")
parser.add_argument('save_to_json', help = '0/1: save the unlocking and locking scripts to json file', type=int)
args = parser.parse_args()

test_triple_pairing()

if args.save_to_json == 1:
    # Save scripts to file
    scripts = {x : {y: str(scripts[x][y]) for y in scripts[x]} for x in scripts}
    if not os.path.exists('./scripts_json'):
        os.makedirs('./scripts_json')
    outfile = open('./scripts_json/triple_pairing.json','w')
    json.dump(scripts, outfile)


print('\nTriple pairing MNT4_753: all tests successful -------\n')