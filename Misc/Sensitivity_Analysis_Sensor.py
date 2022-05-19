import numpy as np
import matplotlib.pyplot as plt


concepts = np.array([[87, 43, 60, 25, 61],
                     [13, 57, 40, 75, 39]])

change = np.arange(4, 45, 4)
weight = np.array([26, 19, 16, 27, 12])


def calculate(weight, concept):
    return sum(weight/100*concept)


scores = []
for i in concepts:
    scores.append(calculate(weight, i))

allup = []
for x in change:
    for y in range(5):
        score = []
        weight = np.array([26, 19, 16, 27, 12])

        weight_temp = weight
        weight = weight-(x/4)
        weight[y] = weight_temp[y]+x
        # print(weight)
        for i in concepts:
            score.append(calculate(weight, i))
        # print(score.index(max(score)), x,y)

        allup.append(score.index(max(score)))

print(allup.count(0))
print(allup.count(1))
print(allup.count(2))

allup = []
change = np.arange(4, 17, 4)
for x in change:
    for y in range(5):
        for z in range(5):
            if y != z and y < z:
                score = []
                weight = np.array([26, 19, 16, 27, 12])

                weight_temp = weight
                weight = weight-(x/1.5)
                weight[y] = weight_temp[y]+x
                weight[z] = weight_temp[z]+x
                # print(weight)
                for i in concepts:
                    score.append(calculate(weight, i))
                # print(score.index(max(score)), x, y, z)
                allup.append(score.index(max(score)))
                # print(score)
print(allup.count(0))
print(allup.count(1))
print(allup.count(2))

tot = []
weight = np.array([26, 19, 16, 27, 12])
for i in range(len(concepts)):
    conc_score_rng = []
    for x in change:
        for y in range(5):
            score = []
            weight = np.array([26, 19, 16, 27, 12])

            weight_temp = weight
            weight = weight-(x/4)
            weight[y] = weight_temp[y]+x
            for l in concepts:
                score.append(calculate(weight, l))
            print(score.index(max(score)), x, y)

    # allup.append(score.index(max(score)))
            for j in range(len(concepts[i])):

                scoring = concepts[i]
                scoring_temp = scoring-(20/4)
                scoring_temp[j] = scoring[j]+20
                conc_score_rng.append(calculate(weight, scoring_temp))
                # print(scoring_temp)
            for k in range(len(concepts[i])):

                scoring = concepts[i]

                if min(scoring) < 20:
                    scoring_temp = scoring+(min(scoring)/4)
                    scoring_temp[k] = 0
                else:
                    scoring_temp = scoring+(20/4)
                    scoring_temp[k] = scoring[k]-20
                conc_score_rng.append(calculate(weight, scoring_temp))
    tot.append(conc_score_rng)

fig = plt.figure()

plt.bar(-0.125, max(tot[0]), color="#00A6D6",
        width=0.25, label="Maximum Score")
plt.text(-0.225, max(tot[0])/2, round(max(tot[0]), 1))
plt.hlines(scores[0], -0.25, 0.25, colors='k', linestyles='dashed')
plt.bar(0.875, max(tot[1]), color="#00A6D6", width=0.25)
plt.text(0.775, max(tot[1])/2, round(max(tot[1]), 1))
plt.text(0.1, scores[0]+0.2, round(scores[0], 1))
plt.text(1.1, scores[1]+0.2, round(scores[1], 1))
# plt.text(2.1, scores[2]+0.2, round(scores[2], 1))
plt.hlines(scores[1], 0.75, 1.25, colors='k',
           linestyles='dashed', label="Current Score")
# plt.hlines(scores[2], 1.75, 2.25, colors='k', linestyles='dashed')
# plt.bar(1.875, max(tot[2]), color="#00A6D6", width=0.25)
# plt.text(1.775, max(tot[2])/2, round(max(tot[2]), 1))
plt.bar(0.125, min(tot[0]), color="#EC6842", width=0.25, label="Minimum Score")
plt.text(0.025, min(tot[0])/2, round(min(tot[0]), 1))
plt.bar(1.125, min(tot[1]), color="#EC6842", width=0.25)
plt.text(1.025, min(tot[1])/2, round(min(tot[1]), 1))
# plt.bar(2.125, min(tot[2]), color="#EC6842", width=0.25)
# plt.text(2.025, min(tot[2])/2, round(min(tot[2]), 1))
plt.xticks([0, 1], ['Ground-Based', 'Canopy-Based'])
plt.legend()
plt.show()
