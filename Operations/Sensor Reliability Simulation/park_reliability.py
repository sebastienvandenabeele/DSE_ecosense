import numpy as np
import time
import pandas as pd
import scipy.optimize as sco


def get_reliability(M):
    reliability = np.random.uniform(0.5, 0.75, M)
    return reliability


def get_concentrations(M):
    np.random.seed(seed=100)
    concentration = np.random.random(M)
    return concentration/np.sum(concentration)


def value_ranking(array):
    rank_temp = array.argsort()
    ranking_array = np.empty_like(rank_temp)
    ranking_array[rank_temp] = np.arange(len(array))
    return ranking_array


def get_score(array_a, array_b, diff):
    score = 0
    for i in range(len(array_a)):
        if np.abs(array_a[i]-array_b[i])/array_b[i] <= diff:
            score = score + 1
    return score


def run_fun(reliability_temp):
    global M, park_df, concentration_map, concentration_ranks
    result = np.dot(reliability_temp, concentration_map)
    rank_reliability = value_ranking(reliability_temp)
    match_score = np.sum(np.sqrt((rank_reliability-concentration_ranks)**2))
    return match_score


def get_reliability(probability_range, likelihood):
    return probability_range[0] + likelihood*(probability_range[1]-probability_range[0])



start_time = time.time()

N = 10000  # Number of iterations
M = 2000   # Number of tiles

df = pd.read_csv("../Flight_software/data/prob_density.csv")
likelihood = df["likelihood"].values
probabilities = df["fire_prob"].values
df["prob_req"] = get_reliability((55, 75), likelihood)

print(np.dot(df["prob_req"].values, probabilities))

# park_df = pd.DataFrame(columns=np.arange(M), index=np.arange(N))

# result = np.empty(N)
# match_score = np.empty(N)
# reliability_arr = np.empty((N, M))
# reliability = np.empty(M)

# single_result = 0
# final_reliability = np.empty(M)

# concentration_map = get_concentrations(M)
# np.random.seed()
# concentration_ranks = value_ranking(concentration_map)

# for i in range(N):
#     # print(f"Running try no. {i}")
#     reliability_temp = get_reliability(M)
#     park_df.loc[i] = reliability_temp
#     result[i] = np.dot(reliability_temp, concentration_map)
#     rank_reliability = value_ranking(reliability_temp)
#     match_score[i] = np.sum(np.sqrt((rank_reliability-concentration_ranks)**2))
#     # match_score[i] = get_score(rank_reliability, concentration_ranks, 0.05)


# park_df["match_score"] = match_score
# park_df["result"] = result
# best_match_row = park_df.loc[park_df['match_score']
#                              == park_df['match_score'].min()]
# print(best_match_row)

# bounds = tuple([(0.5, 0.74) for i in range(len(final_reliability))])

# final_result = sco.minimize(
#     run_fun, best_match_row.values[0][:M], method="SLSQP", bounds=bounds)

# print(final_result)
print("--- %s seconds ---" % (time.time() - start_time))
