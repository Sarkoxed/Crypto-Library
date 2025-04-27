from random import getrandbits

from tqdm import tqdm

from hist_plotter import hist_plot

data = {i: 0 for i in range(1, 10)}
n = 10**6  # 2**32
for r in tqdm(range(1, n)):
    data[int(str(r)[0])] += 1

print(data)
hist_plot(data)

for i, k in data.items():
    print(f"{i}: {k/n}")
