import secrets
from random import randrange

from hist_plotter import hist_plot


class CenteredBinomSampler:
    def __init__(self, nu):
        self.nu = nu

    def __call__(self):
        return (
            secrets.randbits(self.nu).bit_count()
            - secrets.randbits(self.nu).bit_count()
        )


U = CenteredBinomSampler(7)
data = [U() for _ in range(100_000)]
hist_plot(data)#, "CBS")  # , "kickapoo")
