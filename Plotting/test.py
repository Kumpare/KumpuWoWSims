import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

if __name__ == "__main__":

    n_pulls = np.random.normal(loc=400, scale=100, size=142).astype('uint16')
    n_kills = np.clip(np.abs(np.random.normal(4*n_pulls/400, scale=1)), 0, 8)
    n_kills = np.concatenate([n_kills, [0]], axis=0)
    n_pulls = np.concatenate([n_pulls, [920]], axis=0)

    slope, intercept, r, *_ = linregress(n_pulls, n_kills)
    plt.suptitle(f'No. progression pulls and mythic boss kills', fontweight="bold")
    plt.title(f'Data reflects {n_pulls.shape[0]} log reports from WarcraftLogs on 28/12/2022 \n R\N{SUPERSCRIPT TWO}: {r**2:.5f}')
    plt.plot(n_pulls, intercept + slope*n_pulls, 'r')
    plt.legend()
    plt.xlim((0, 1000))
    plt.ylabel("Progression")
    plt.xlabel("Pulls")
    plt.text(850, 0.33, "Anvil Gaming")
    plt.scatter(n_pulls, n_kills)
    plt.tight_layout()
    plt.savefig('Anvil Gaming statistics.png')