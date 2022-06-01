from joblib import Parallel, delayed
import numpy as np
import time


def random_square(seed):
    np.random.seed(seed)
    random_num = np.random.randint(0, 10)
    return random_num**2


if __name__ == '__main__':
    start_time = time.time()

    inputs = range(10000000)

    # result = [random_square(i) for i in inputs]

    result = Parallel(n_jobs=4, backend='multiprocessing', verbose=1)(delayed(random_square)(i) for i in inputs)

    # print(result)
    print("--- %s seconds ---" % (time.time() - start_time))
