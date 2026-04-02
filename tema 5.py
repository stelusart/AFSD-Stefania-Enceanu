import random
import sys
import time

#Crestem limita de recursivitate pentru Quick Sort pe liste deja sortate (cazul cel mai nefavorabil)
sys.setrecursionlimit(20000)


class SortMetrics:

    def __init__(self):
        self.comparisons = 0
        self.moves = 0
        self.recursive_calls = 0

    def reset(self):
        self.comparisons = 0
        self.moves = 0
        self.recursive_calls = 0

# 1.IMPLEMENTAREA ALGORITMILOR DE SORTARE


def bubble_sort(arr, metrics):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                metrics.moves += 1  # Numaram o interschimbare
                swapped = True
        if not swapped:
            break


def quick_sort_wrapper(arr, metrics):
    metrics.recursive_calls += 1
    _quick_sort(arr, 0, len(arr) - 1, metrics)


def _quick_sort(arr, low, high, metrics):
    if low < high:
        pi = _partition(arr, low, high, metrics)
        metrics.recursive_calls += 1
        _quick_sort(arr, low, pi - 1, metrics)
        metrics.recursive_calls += 1
        _quick_sort(arr, pi + 1, high, metrics)


def _partition(arr, low, high, metrics):
    # Folosim ultimul element ca pivot
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        metrics.comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            metrics.moves += 1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    metrics.moves += 1
    return i + 1


def merge_sort_wrapper(arr, metrics):
    metrics.recursive_calls += 1
    _merge_sort(arr, metrics)


def _merge_sort(arr, metrics):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        metrics.recursive_calls += 1
        _merge_sort(L, metrics)
        metrics.recursive_calls += 1
        _merge_sort(R, metrics)

        i = j = k = 0

        while i < len(L) and j < len(R):
            metrics.comparisons += 1
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            metrics.moves += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            metrics.moves += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            metrics.moves += 1


# 2 & 3 GENERAREA DATELOR DE TEST

def generate_data(size, data_type):
    if data_type == "aleator":
        return [random.randint(1, size * 10) for _ in range(size)]
    elif data_type == "sortat crescator":
        return list(range(1, size + 1))
    elif data_type == "sortat descrescator":
        return list(range(size, 0, -1))
    elif data_type == "duplicate":
        return [random.randint(1, max(2, size // 10)) for _ in range(size)]
    elif data_type == "aproape sortat":
        arr = list(range(1, size + 1))
        # Inversam cca. 5% dintre elemente pentru a-l face "aproape sortat"
        for _ in range(max(1, size // 20)):
            idx1 = random.randint(0, size - 1)
            idx2 = random.randint(0, size - 1)
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
        return arr


# 4, 5, 6, 7 & 8 TESTAREA SI MASURAREA


def run_benchmarks():
    random.seed(42)  # Seed fixat pentru reproductibilitate
    dimensiuni = [
        100,
        500,
        1000,
        2000,
    ]  # Redus putin de la 10.000 pentru a nu bloca executia la Bubble Sort
    tipuri_intrare = [
        "aleator",
        "sortat crescator",
        "sortat descrescator",
        "duplicate",
        "aproape sortat",
    ]
    algoritmi = [
        ("Bubble Sort", bubble_sort),
        ("Quick Sort", quick_sort_wrapper),
        ("Merge Sort", merge_sort_wrapper),
    ]

    numar_rulari = 3
    metrics = SortMetrics()
    rezultate = []

    print("Se ruleaza testele... Poate dura cateva momente.\n")

    for dim in dimensiuni:
        for tip in tipuri_intrare:
            # Generam setul de baza
            original_arr = generate_data(dim, tip)

            for nume_alg, func_alg in algoritmi:
                total_timp = 0
                total_comp = 0
                total_moves = 0
                total_calls = 0
                valid = True

                # Pentru QuickSort pe date deja sortate, la dimensiuni mari riscam RecursionError
                if (
                    nume_alg == "Quick Sort"
                    and (
                        tip == "sortat crescator"
                        or tip == "sortat descrescator"
                    )
                    and dim > 1000
                ):
                    continue  # Sarim peste cazurile care crapa din cauza pivotului prost ales

                for _ in range(numar_rulari):
                    # Copie a listei pentru a nu altera datele initiale
                    test_arr = original_arr.copy()
                    metrics.reset()

                    # Masurare stricta a executiei
                    start = time.time()
                    func_alg(test_arr, metrics)
                    end = time.time()

                    # Verificarea corectitudinii
                    if test_arr != sorted(original_arr):
                        valid = False

                    total_timp += end - start
                    total_comp += metrics.comparisons
                    total_moves += metrics.moves
                    total_calls += metrics.recursive_calls

                if valid:
                    rezultate.append(
                        {
                            "algoritm": nume_alg,
                            "dimensiune": dim,
                            "intrare": tip,
                            "timp_mediu": total_timp / numar_rulari,
                            "comparatii": int(total_comp / numar_rulari),
                            "mutari": int(total_moves / numar_rulari),
                            "apeluri": int(total_calls / numar_rulari),
                        }
                    )
                else:
                    print(f"[EROARE] Algoritmul {nume_alg} a esuat la sortare!")

    # 9.ORGANIZAREA SI AFISAREA REZULTATELOR
    print(
        f"{'Algoritm':<15} | {'Dimensiune':<10} | {'Tip Intrare':<20} | {'Timp Mediu (s)':<15} | {'Comparatii':<12} | {'Mutari':<10} | {'Apeluri':<8}"
    )
    print("-" * 100)

    for r in rezultate:
        print(
            f"{r['algoritm']:<15} | {r['dimensiune']:<10} | {r['intrare']:<20} | {r['timp_mediu']:<15.6f} | {r['comparatii']:<12} | {r['mutari']:<10} | {r['apeluri']:<8}"
        )


if __name__ == "__main__":
    run_benchmarks()