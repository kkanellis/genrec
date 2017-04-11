import numpy as np

class TextureWindow:

    def __init__(self, windows, prev_windows, fft_length=512):
        self.windows = windows
        self.prev_windows = prev_windows
        self.fft_length = fft_length // 2 + 1

        self.fft_mags = np.array([
            np.absolute( np.fft.rfft(window) )
                for window in self.windows
        ])
        self.prev_fft_mags = np.array([
            np.absolute( np.fft.rfft(window) )
                for window in self.prev_windows
        ])

        #print( self._get_wnd_nrg( self.fft_mags[0]) )
        #q = np.array(windows[0], dtype=np.int64)
        #print( np.sum( q ** 2 ) )

    def centroid(self):
        f_arr = np.array([ f for f in range(self.fft_length) ])

        centroids = [ ]
        for fft_mag in self.fft_mags:
            centroids.append(
                np.dot(fft_mag, f_arr) / np.sum(fft_mag)
            )

        return np.mean(centroids), np.std(centroids)

    def rolloff(self):
        rolloffs = [ ]
        for i in range( len(self.fft_mags) ):
            roff = 0.85 * np.sum(self.fft_mags[i])

            # TODO: remove loop
            psum = 0
            for R in range(self.fft_length):
                if psum + self.fft_mags[i][R] > roff:
                    break
                psum += self.fft_mags[i][R]

            rolloffs.append(R)

        return np.mean(rolloffs), np.std(rolloffs)


    def flux(self):
        mags_norm = np.array([
            fft_mag / self._get_wnd_nrg(fft_mag)
            for fft_mag in self.fft_mags
        ])

        prev_mags_norm = np.array([
            fft_mag / self._get_wnd_nrg(fft_mag)
            for fft_mag in self.prev_fft_mags
        ])

        fluxes = [
            np.linalg.norm(curr - prev)
            for prev, curr in
                zip(prev_mags_norm, mags_norm)
        ]

        return np.mean(fluxes), np.std(fluxes)


        #print( np.sum(self.fft_mags[0]) )
        #print( self._get_wnd_nrg( self.fft_mags[0] ) )


    def zero_crossings(self):
        zc = [ ]
        for w in self.windows:
            zc.append(
                np.sum([
                    (w[i-1] < 0) != (w[i] < 0)
                    for i in range(1, len(w))
                ])
            )

        return np.mean(zc), np.std(zc)

    def low_energy(self):
        w_nrg = np.array([
            self._get_wnd_nrg(fft_w)
            for fft_w in self.fft_mags
        ])
        avg_nrg = np.mean(w_nrg)

        return np.sum(
            [ nrg < avg_nrg for nrg in w_nrg ]
        ) / len(w_nrg)

    def _get_wnd_nrg(self, fft_w):
        """
        Return the total energy of a window
        using FFT magnitude (Parseval's theorem)
        """
        return np.sum( (fft_w ** 2) / self.fft_length )

    def fv(self):
        mean_centroid, std_centroid = self.centroid()
        mean_rolloff, std_rolloff = self.rolloff()
        mean_flux, std_flux = self.flux()
        mean_zc, std_zc = self.zero_crossings()
        low_energy = self.low_energy()

        return np.array([
            mean_centroid,
            mean_rolloff,
            mean_flux,
            mean_zc,
            std_centroid,
            std_rolloff,
            std_flux,
            std_zc,
            low_energy
        ])


