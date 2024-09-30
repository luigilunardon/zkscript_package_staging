from dataclasses import dataclass

import pytest
from elliptic_curves.fields.fq import base_field_from_modulus
from elliptic_curves.fields.quadratic_extension import quadratic_extension_from_base_field_and_non_residue
from elliptic_curves.models.curve import Curve
from elliptic_curves.models.ec import elliptic_curve_from_curve
from tx_engine import Context, Script

from src.zkscript.elliptic_curves.ec_operations_fq import EllipticCurveFq
from src.zkscript.elliptic_curves.ec_operations_fq2 import EllipticCurveFq2
from src.zkscript.elliptic_curves.ec_operations_fq_unrolled import EllipticCurveFqUnrolled
from src.zkscript.elliptic_curves.util import CurvePoint, FieldElement
from src.zkscript.fields.fq2 import Fq2 as Fq2ScriptModel
from src.zkscript.util.utility_scripts import nums_to_script, pick, roll
from tests.elliptic_curves.util import (
    generate_extended_list,
    generate_unlock,
    generate_verify_from_list,
    generate_verify_point,
    save_scripts,
)


@dataclass
class Secp256k1:
    modulus = 115792089237316195423570985008687907853269984665640564039457584007908834671663
    order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    Fq_k1 = base_field_from_modulus(q=modulus)
    Fr_k1 = base_field_from_modulus(q=order)
    secp256k1, _ = elliptic_curve_from_curve(curve=Curve(a=Fq_k1(0), b=Fq_k1(7)))
    degree = 1
    point_at_infinity = secp256k1.point_at_infinity()
    generator = secp256k1(
        x=Fq_k1(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798),
        y=Fq_k1(0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8),
    )
    test_script = EllipticCurveFq(q=modulus, curve_a=0)
    test_script_unrolled = EllipticCurveFqUnrolled(q=modulus, ec_over_fq=test_script)
    test_both_negations = False
    # Define filename for saving scripts
    filename = "secp256k1"
    # Test data
    P = secp256k1(
        x=Fq_k1(41215615274060316946324649613818309412392301453105041246304560830716313169400),
        y=Fq_k1(74117305601093926817905542912257614464261406761524109253393548124815807467650),
    )
    Q = secp256k1(
        x=Fq_k1(75022427023119710175388682918928560109160388746708368835324539025120909485774),
        y=Fq_k1(70716735503538187278140999937647087780607401911659658020223121861184446029572),
    )
    a = 64046112301879843941239178948101222343000413030798872646069227448863068996094
    test_data = {
        "test_algebraic_addition": [
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [5, 4, 3, 1],
                "expected": [],
            },
            {"P": P, "Q": Q, "move": roll, "positions": [5, 4, 3, 1], "expected": []},
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [5, 4, 3, 1],
                "expected": [],
            },
        ],
        "test_doubling": [
            {
                "P": P,
                "move": roll,
                "positions": [3, 2, 1],
                "expected": [],
            },
        ],
        "test_addition_unknown_points": [
            # {"P": P, "Q": Q, "expected": P + Q},
            {"P": P, "Q": -P, "expected": point_at_infinity},
            {"P": P, "Q": point_at_infinity, "expected": P},
            {"P": point_at_infinity, "Q": Q, "expected": Q},
        ],
        "test_multiplication_unrolled": [
            {"P": P, "a": a, "expected": P.multiply(a)},
            {"P": P, "a": 0, "expected": P.multiply(0)},
        ],
    }


@dataclass
class Secp256r1:
    modulus = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    order = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
    Fq_r1 = base_field_from_modulus(q=modulus)
    Fr_r1 = base_field_from_modulus(q=order)
    secp256r1, _ = elliptic_curve_from_curve(
        curve=Curve(
            a=Fq_r1(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC),
            b=Fq_r1(0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B),
        )
    )
    degree = 1
    point_at_infinity = secp256r1.point_at_infinity()
    generator = secp256r1(
        x=Fq_r1(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296),
        y=Fq_r1(0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5),
    )
    test_script = EllipticCurveFq(q=modulus, curve_a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC)
    test_script_unrolled = EllipticCurveFqUnrolled(q=modulus, ec_over_fq=test_script)
    test_both_negations = False
    # Define filename for saving scripts
    filename = "secp256r1"
    # Test data
    P = secp256r1(
        x=Fq_r1(11990862373011617163317646558408705408882310560667899835694339942976011369232),
        y=Fq_r1(80247255150202856195005696069978490751513498800937223995637125987523375481630),
    )
    Q = secp256r1(
        x=Fq_r1(64260480261783363550587538316957846447400713742342025589747159311266528268825),
        y=Fq_r1(68194036500363828464317082173162010818073467174652382578837906057865410662381),
    )
    a = 104614095137500434070196828944928516815982260532830080798264081596642730786155
    test_data = {
        "test_algebraic_addition": [
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [5, 4, 3, 1],
                "expected": [],
            },
            {"P": P, "Q": Q, "move": roll, "positions": [5, 4, 3, 1], "expected": []},
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [5, 4, 3, 1],
                "expected": [],
            },
        ],
        "test_doubling": [
            {
                "P": P,
                "move": roll,
                "positions": [3, 2, 1],
                "expected": [],
            },
        ],
        "test_addition_unknown_points": [
            # {"P": P, "Q": Q, "expected": P + Q},
            {"P": P, "Q": -P, "expected": point_at_infinity},
            {"P": P, "Q": point_at_infinity, "expected": P},
            {"P": point_at_infinity, "Q": Q, "expected": Q},
        ],
        "test_multiplication_unrolled": [{"P": P, "a": a, "expected": P.multiply(a)}],
    }


@dataclass
class Secp256k1Extension:
    modulus = Secp256k1.modulus
    order = Secp256k1.order
    Fq_k1 = Secp256k1.Fq_k1
    NON_RESIDUE_K1 = Fq_k1(3)
    Fq2_k1 = quadratic_extension_from_base_field_and_non_residue(base_field=Fq_k1, non_residue=NON_RESIDUE_K1)
    Fr_k1 = Secp256k1.Fr_k1
    secp256k1ext, _ = elliptic_curve_from_curve(curve=Curve(a=Fq2_k1.zero(), b=Fq2_k1(Fq_k1(7), Fq_k1.zero())))
    degree = 2
    point_at_infinity = secp256k1ext.point_at_infinity()
    test_script = EllipticCurveFq2(
        q=modulus, curve_a=[0, 0], fq2=Fq2ScriptModel(q=modulus, non_residue=NON_RESIDUE_K1.to_list()[0])
    )
    test_both_negations = True
    # Define filename for saving scripts
    filename = "secp256k1_extension"
    # Test data
    P = secp256k1ext(
        x=Fq2_k1(
            Fq_k1(0xB981DA1FE0F34CA56B4C7A15F7A33946DCD3E60C7A12727068D8ED449D15F70E),
            Fq_k1(0xFA2C34DA64A420D491AD1743D09445FAC971C28B03C203A7AF2768619391463C),
        ),
        y=Fq2_k1(
            Fq_k1(0xDAADB913FAFB7EEAC301D7F430AA98FC1EAA5CAED1FE66D3399074CCFAA78B32),
            Fq_k1(0x93620E1F5AE7B6F2B46ACA13F339BBAAFDBBA268F6A61E7571B5EA5F25C662A7),
        ),
    )
    Q = secp256k1ext(
        x=Fq2_k1(
            Fq_k1(0xFBD173BDFFC6C303177D831811800DAE3A7EDC335F420BE0FE3FC643E2019DDF),
            Fq_k1(0xB2CD8B5AF66F524BBC351B2A3EA4687408644A9871C6C00973C47F2CEFD03FA9),
        ),
        y=Fq2_k1(
            Fq_k1(0xC61512666F8EC06B462C3002045D59525C63BCD0BFC4E2BB83BA19E1111CD2DE),
            Fq_k1(0xC52748235BFD3380D1620DE3B2CD038BDDEBB98064902EA0303214E7B273C7D5),
        ),
    )
    test_data = {
        "test_algebraic_addition": [
            # Tests rolling P
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [10, 9, 7, 3],
                "expected": [],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [12, 11, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [16, 15, 13, 3],
                "expected": [
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [16, 15, 10, 6],
                "expected": [
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [21, 20, 14, 5],
                "expected": [
                    *[1] * 11,  # filler elements
                ],
            },
            # Tests picking P
            {
                "P": P,
                "Q": Q,
                "lam": P.get_lambda(Q),
                "move": pick,
                "positions": [10, 9, 7, 3],
                "expected": [*P.to_list()],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [12, 11, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [16, 15, 13, 3],
                "expected": [
                    *P.to_list(),
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [16, 15, 10, 6],
                "expected": [
                    *[1] * 3,  # filler elements
                    *P.to_list(),
                    *[1] * 3,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [21, 20, 14, 5],
                "expected": [
                    *[1] * 4,  # filler elements
                    *P.to_list(),
                    *[1] * 7,  # filler elements
                ],
                "is_addition": True,
            },
        ],
        "test_doubling": [
            # Tests rolling P
            {"P": P, "move": roll, "positions": [6, 5, 3], "expected": []},
            {
                "P": P,
                "move": roll,
                "positions": [8, 5, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [8, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [9, 7, 4],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [14, 10, 6],
                "expected": [
                    *[1] * 8,  # filler elements
                ],
            },
            # Tests picking P
            {"P": P, "move": pick, "positions": [6, 5, 3], "expected": [*P.to_list()]},
            {
                "P": P,
                "move": pick,
                "positions": [8, 5, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [8, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [9, 7, 4],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [14, 10, 6],
                "expected": [
                    *[1] * 5,  # filler elements
                    *P.to_list(),
                    *[1] * 3,  # filler elements
                ],
            },
        ],
        "test_negation": [
            {"P": P, "expected": -P},
            {"P": point_at_infinity, "expected": -point_at_infinity},
        ],
    }


@dataclass
class Secp256r1Extension:
    modulus = Secp256r1.modulus
    order = Secp256r1.order
    Fq_r1 = Secp256r1.Fq_r1
    NON_RESIDUE_R1 = Fq_r1(3)
    Fq2_r1 = quadratic_extension_from_base_field_and_non_residue(base_field=Fq_r1, non_residue=NON_RESIDUE_R1)
    Fr_r1 = Secp256r1.Fr_r1
    secp256r1ext, _ = elliptic_curve_from_curve(
        curve=Curve(
            a=Fq2_r1(Fq_r1(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC), Fq_r1.zero()),
            b=Fq2_r1(Fq_r1(0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B), Fq_r1.zero()),
        )
    )
    degree = 2
    point_at_infinity = secp256r1ext.point_at_infinity()
    test_script = EllipticCurveFq2(
        q=modulus,
        curve_a=[0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC, 0],
        fq2=Fq2ScriptModel(q=modulus, non_residue=NON_RESIDUE_R1.to_list()[0]),
    )
    test_both_negations = True
    # Define filename for saving scripts
    filename = "secp256r1_extension"
    # Test data
    P = secp256r1ext(
        x=Fq2_r1(
            Fq_r1(0x9D764123F35983906F6D4835B1843F8B842355BD1744B7CB1A28CFE182FB45F3),
            Fq_r1(0xD739D84ADA8F5C667F71179D87A811E3C81C13A373F2F147758E038B0AA4D173),
        ),
        y=Fq2_r1(
            Fq_r1(0xB76CF9D7E1FB44B9D229A7C1412AC648F1DFDAB223DE92E42E02C7E5057E390F),
            Fq_r1(0x2AC60E3EBC7F1E8EF6DB6D07009F6FAF10C7F3AA71FAEE13FE273DF57C174F9F),
        ),
    )
    Q = secp256r1ext(
        x=Fq2_r1(
            Fq_r1(0x6C3AC0A83056E2E5DD4C1883D69F9BD64A2ACB655D843F7B7695EFA2392E30F4),
            Fq_r1(0xBAA280A48466BB5BBD73ED70054947C4A929BF2529E20489E99490CFFE1E4EA6),
        ),
        y=Fq2_r1(
            Fq_r1(0xFEA7280CF96F9012ED154141E753047EEBD3D810469BAADA62CC43CE26B63858),
            Fq_r1(0x9C26432B2554E32601E74658E881AAE4A6285106CE5E943467FE30E7396446EB),
        ),
    )
    test_data = {
        "test_algebraic_addition": [
            # Tests rolling P
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [10, 9, 7, 3],
                "expected": [],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [12, 11, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [16, 15, 13, 3],
                "expected": [
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [16, 15, 10, 6],
                "expected": [
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": roll,
                "positions": [21, 20, 14, 5],
                "expected": [
                    *[1] * 11,  # filler elements
                ],
            },
            # Tests picking P
            {
                "P": P,
                "Q": Q,
                "lam": P.get_lambda(Q),
                "move": pick,
                "positions": [10, 9, 7, 3],
                "expected": [*P.to_list()],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [12, 11, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [16, 15, 13, 3],
                "expected": [
                    *P.to_list(),
                    *[1] * 6,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [16, 15, 10, 6],
                "expected": [
                    *[1] * 3,  # filler elements
                    *P.to_list(),
                    *[1] * 3,  # filler elements
                ],
            },
            {
                "P": P,
                "Q": Q,
                "move": pick,
                "positions": [21, 20, 14, 5],
                "expected": [
                    *[1] * 4,  # filler elements
                    *P.to_list(),
                    *[1] * 7,  # filler elements
                ],
                "is_addition": True,
            },
        ],
        "test_doubling": [
            # Tests rolling P
            {"P": P, "move": roll, "positions": [6, 5, 3], "expected": []},
            {
                "P": P,
                "move": roll,
                "positions": [8, 5, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [8, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [9, 7, 4],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": roll,
                "positions": [14, 10, 6],
                "expected": [
                    *[1] * 8,  # filler elements
                ],
            },
            # Tests picking P
            {"P": P, "move": pick, "positions": [6, 5, 3], "expected": [*P.to_list()]},
            {
                "P": P,
                "move": pick,
                "positions": [8, 5, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [8, 7, 3],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [9, 7, 4],
                "expected": [
                    1,  # filler element
                    1,  # filler element
                    *P.to_list(),
                    1,  # filler element
                ],
            },
            {
                "P": P,
                "move": pick,
                "positions": [14, 10, 6],
                "expected": [
                    *[1] * 5,  # filler elements
                    *P.to_list(),
                    *[1] * 3,  # filler elements
                ],
            },
        ],
        "test_negation": [
            {"P": P, "expected": -P},
            {"P": point_at_infinity, "expected": -point_at_infinity},
        ],
    }


def generate_test_cases(test_name):
    configurations = [Secp256k1, Secp256r1, Secp256k1Extension, Secp256r1Extension]

    out = []
    for config in configurations:
        if test_name in config.test_data:
            for test_data in config.test_data[test_name]:
                match test_name:
                    case "test_algebraic_addition":
                        out.append(
                            (
                                config,
                                test_data["P"],
                                test_data["Q"],
                                test_data["move"],
                                test_data["positions"],
                                test_data["expected"],
                            )
                        )
                    case "test_doubling":
                        out.append(
                            (
                                config,
                                test_data["P"],
                                test_data["move"],
                                test_data["positions"],
                                test_data["expected"],
                            )
                        )
                    case "test_negation":
                        out.append((config, test_data["P"], test_data["expected"]))
                    case "test_addition_unknown_points":
                        out.append((config, test_data["P"], test_data["Q"], test_data["expected"]))
                    case "test_multiplication_unrolled":
                        out.append((config, test_data["P"], test_data["a"], test_data["expected"]))

    return out


@pytest.mark.parametrize("negate_P", [True, False])
@pytest.mark.parametrize("negate_Q", [True, False])
@pytest.mark.parametrize(
    ("config", "P", "Q", "move", "positions", "expected"),
    generate_test_cases("test_algebraic_addition"),
)
def test_algebraic_addition(config, P, Q, negate_P, negate_Q, move, positions, expected, save_to_json_folder):  # noqa: N803
    P_for_result = -P if negate_P and config.test_both_negations else P
    Q_for_result = -Q if negate_Q else Q
    lam = P_for_result.get_lambda(Q_for_result)

    unlock = nums_to_script(
        generate_extended_list(
            elements=[[config.modulus], lam.to_list(), P.to_list(), Q.to_list()],
            positions_elements=positions,
            filler=1,
        )
    )

    lock = (
        config.test_script.point_algebraic_addition(
            take_modulo=True,
            check_constant=True,
            clean_constant=True,
            lam=FieldElement(positions[1], roll),
            P=CurvePoint(positions[2], negate_P, move),
            Q=CurvePoint(positions[3], negate_Q, roll),
        )
        if config.test_both_negations
        else config.test_script.point_algebraic_addition(
            take_modulo=True,
            check_constant=True,
            clean_constant=True,
            lam=FieldElement(positions[1], roll),
            P=CurvePoint(positions[2], False, move),
            Q=CurvePoint(positions[3], negate_Q, roll),
        )
    )

    lock += generate_verify_from_list([*expected, *(P_for_result + Q_for_result).to_list()])

    context = Context(script=unlock + lock)
    assert context.evaluate()
    assert len(context.get_stack()) == 1
    assert len(context.get_altstack()) == 0

    if save_to_json_folder:
        save_scripts(str(lock), str(unlock), save_to_json_folder, config.filename, "point addition")


@pytest.mark.parametrize("negate_P", [True, False])
@pytest.mark.parametrize(("config", "P", "move", "positions", "expected"), generate_test_cases("test_doubling"))
def test_doubling(config, P, negate_P, move, positions, expected, save_to_json_folder):  # noqa: N803
    P_for_result = -P if negate_P else P
    lam = P_for_result.get_lambda(P_for_result)

    unlock = nums_to_script(
        generate_extended_list(
            elements=[[config.modulus], lam.to_list(), P.to_list()], positions_elements=positions, filler=1
        )
    )

    lock = config.test_script.point_doubling(
        take_modulo=True,
        check_constant=True,
        clean_constant=True,
        lam=FieldElement(positions[1], roll),
        P=CurvePoint(positions[2], negate_P, move),
    )

    lock += generate_verify_from_list([*expected, *(P_for_result + P_for_result).to_list()])

    context = Context(script=unlock + lock)
    assert context.evaluate()
    assert len(context.get_stack()) == 1
    assert len(context.get_altstack()) == 0

    if save_to_json_folder:
        save_scripts(str(lock), str(unlock), save_to_json_folder, config.filename, "point doubling")


@pytest.mark.parametrize(("config", "P", "Q", "expected"), generate_test_cases("test_addition_unknown_points"))
def test_addition_unknown_points(config, P, Q, expected, save_to_json_folder):  # noqa: N803
    unlock = nums_to_script([config.modulus])

    # if config.point_at_infinity not in {P, Q, expected}:
    #     lam = P.get_lambda(Q)
    #     unlock += nums_to_script(lam.to_list())

    unlock += generate_unlock(P, degree=config.degree)
    unlock += generate_unlock(Q, degree=config.degree)

    lock = config.test_script.point_addition_with_unknown_points(
        take_modulo=True, check_constant=True, clean_constant=True
    )
    lock += generate_verify_point(expected, degree=config.degree)

    context = Context(script=unlock + lock)
    assert context.evaluate()
    assert len(context.get_stack()) == 1
    assert len(context.get_altstack()) == 0

    if save_to_json_folder:
        save_scripts(str(lock), str(unlock), save_to_json_folder, config.filename, "point addition with unknown points")


@pytest.mark.parametrize(("config", "P", "a", "expected"), generate_test_cases("test_multiplication_unrolled"))
def test_multiplication_unrolled(config, P, a, expected, save_to_json_folder):  # noqa: N803
    exp_a = [int(bin(a)[j]) for j in range(2, len(bin(a)))][::-1]

    unlock = config.test_script_unrolled.unrolled_multiplication_input(
        P=P.to_list(),
        a=a,
        lambdas=[[s.to_list() for s in el] for el in P.get_lambdas(exp_a)] if a else [],
        max_multiplier=config.order,
        load_modulus=True,
    )

    lock = config.test_script_unrolled.unrolled_multiplication(
        max_multiplier=config.order, modulo_threshold=1, check_constant=True, clean_constant=True
    )
    lock += generate_verify_point(expected, degree=config.degree) + Script.parse_string("OP_VERIFY")
    lock += generate_verify_point(P, degree=config.degree)

    context = Context(script=unlock + lock)
    assert context.evaluate()
    assert len(context.get_stack()) == 1
    assert len(context.get_altstack()) == 0

    if save_to_json_folder:
        save_scripts(str(lock), str(unlock), save_to_json_folder, config.filename, "unrolled multiplication")


@pytest.mark.parametrize(("config", "P", "expected"), generate_test_cases("test_negation"))
def test_negation(config, P, expected, save_to_json_folder):  # noqa: N803
    unlock = nums_to_script([config.modulus])
    unlock += generate_unlock(P, degree=config.degree)

    lock = config.test_script.point_negation(take_modulo=True, check_constant=True, is_constant_reused=False)
    lock += generate_verify_point(expected, degree=config.degree)

    context = Context(script=unlock + lock)
    assert context.evaluate()
    assert len(context.get_stack()) == 2
    assert len(context.get_altstack()) == 0

    if save_to_json_folder:
        save_scripts(str(lock), str(unlock), save_to_json_folder, config.filename, "point negation")
