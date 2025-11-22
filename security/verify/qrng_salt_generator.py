import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Letters A–Z + a–z, same as original
LETTERS = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]


def ourqrng(string: str, threshold_bins: int = 10) -> str:
    """
    Quantum RNG returning one character from `string`,
    following original logic: statevector, prob_1 → binned → index.
    """
    characters = string

    theta = np.random.uniform(0, np.pi)
    phi = np.random.uniform(0, 2 * np.pi)

    circuit = QuantumCircuit(1, 1)
    circuit.ry(theta, 0)
    circuit.rz(phi, 0)
    circuit.save_statevector()

    simulator = AerSimulator(method="statevector")
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    state = result.get_statevector(compiled_circuit)
    alpha, beta = state[0], state[1]
    prob_1 = np.abs(beta) ** 2

    bin_size = 1.0 / threshold_bins
    quantized_prob = int(prob_1 / bin_size) * bin_size

    index = int(quantized_prob * len(characters)) % len(characters)
    return characters[index]


def rotate_array(arr, n):
    """
    Original rotation logic: arr[n-1:] + arr[:n-1]
    Do NOT switch to standard rotation.
    """
    n = n % len(arr)
    return arr[n - 1:] + arr[:n - 1]


def _generate_salt_from_abc(a: int, b: int, c: int):
    """
    Core rotation + indexing logic with 2**a + 3**b + 4**c.
    We keep the structure as in the original code, only fix syntax.
    """
    arr1 = rotate_array(LETTERS, 2 ** a)
    arr2 = rotate_array(arr1, 3 ** b)
    arr3 = rotate_array(arr2, 4 ** c)

    index_base = (2 ** a + 3 ** b + 4 ** c) % len(arr3)
    arr4 = rotate_array(arr3, index_base)

    # slice from start up to index_base
    return arr4[:index_base]


def _gen_abc():
    """
    Original a,b,c selection using QRNG on '12345', '123', '12'.
    Non-digit → 0.
    """
    i = "12345"
    j = "123"
    k = "12"

    a_char = ourqrng(i, threshold_bins=10)
    b_char = ourqrng(j, threshold_bins=10)
    c_char = ourqrng(k, threshold_bins=10)

    a = int(a_char) if a_char.isdigit() else 0
    b = int(b_char) if b_char.isdigit() else 0
    c = int(c_char) if c_char.isdigit() else 0
    return a, b, c


def generate_salt() -> str:
    """
    Public salt generator:
    - generate a,b,c from QRNG
    - reject triples where (2**a + 3**b + 4**c - 3) % 26 == 0
      (original modulo condition, but with correct exponentiation)
    - cap attempts to avoid infinite loops
    - build salt from rotated LETTERS
    """
    max_attempts = 1000
    attempt = 0

    while True:
        a, b, c = _gen_abc()
        val = (2 ** a + 3 ** b + 4 ** c - 3) % 26

        if val != 0:
            # valid triple
            slice_arr = _generate_salt_from_abc(a, b, c)
            salt = "".join(slice_arr)
            if salt:  # non-empty
                return salt

        attempt += 1
        if attempt >= max_attempts:
            # fallback: deterministic simple salt if QRNG loop fails
            return "FallbackSaltQRNG"
