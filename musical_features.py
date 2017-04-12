import librosa
import numpy as np
import matplotlib.pyplot as plt


class TextureWindow:

    def __init__(self, tex_wnd, fft_len=512, sr=22050):
        # split texture window to analysis windows
        self.tex_wnd = tex_wnd
        self.tex_wnds = self._split_tex_wnd(tex_wnd, fft_len)

        self.an_wnd_len = fft_len
        self.sr = sr

        #plt.magnitude_spectrum(np.array(windows).ravel(), Fs=sampling_rate)
        #plt.show()

        """
        self._fft_tex_wnds = np.array([
            np.abs(librosa.stft(
                y=wnd,
                n_fft=fft_len,
                hop_length=fft_len+1,
            )).ravel()
            for wnd in self.tex_wnds
        ])
        #print(self._fft_tex_wnds)

        """
        # TODO: check FFT coefficients correctness
        self.fft_tex_wnds = np.abs(
            librosa.stft(
                y=tex_wnd,
                n_fft=fft_len,
                hop_length=fft_len,
            )
        )
        """
        print(self.fft_tex_wnds.T)
        print( (self._fft_tex_wnds == self.fft_tex_wnds.T) )
        plt.figure(1)
        plt.plot(self.fft_tex_wnds)
        plt.show()
        """

    def centroid(self):
        centroids = librosa.feature.spectral_centroid(
            S=self.fft_tex_wnds
        ).ravel()
        return np.mean(centroids), np.std(centroids)


    def rolloff(self):
        rolloffs = librosa.feature.spectral_rolloff(
            S=self.fft_tex_wnds
        ).ravel()
        return np.mean(rolloffs), np.std(rolloffs)


    def flux(self):
        fft_tex_wnds_T = self.fft_tex_wnds.T
        w_nrg = librosa.feature.rmse(
            S=self.fft_tex_wnds,
            frame_length=self.an_wnd_len,
            hop_length=self.an_wnd_len
        ).ravel()

        # normalize via energy
        for i in range(len(fft_tex_wnds_T)):
            fft_tex_wnds_T[i] /= w_nrg[i]

        fluxes = np.empty(
            shape=(len(fft_tex_wnds_T) - 1,),
            dtype=np.float64,
        )
        for i in range(1, len(fft_tex_wnds_T)):
            fluxes[i-1] = np.sum(
                (fft_tex_wnds_T[i-1] - fft_tex_wnds_T[i]) ** 2
            )

        return np.mean(fluxes), np.std(fluxes)


    def zero_crossings(self):
        zc = librosa.feature.zero_crossing_rate(
            y=self.tex_wnd,
            frame_length=self.an_wnd_len,
            hop_length=self.an_wnd_len,
        ).ravel()
        return np.mean(zc), np.std(zc)


    def low_energy(self):
        w_nrg = librosa.feature.rmse(
            S=self.fft_tex_wnds,
            frame_length=self.an_wnd_len,
            hop_length=self.an_wnd_len
        ).ravel()
        avg_nrg = np.mean(w_nrg)

        return np.sum(
            [ nrg < avg_nrg for nrg in w_nrg ]
        ) / len(w_nrg)


    def mfcc(self, n_mfcc=5):
        mfccs = librosa.feature.mfcc(
            S=self.fft_tex_wnds,
            frame_length=self.an_wnd_len,
            hop_length=self.an_wnd_len,
            n_mfcc=n_mfcc,
        )

        return np.mean(mfccs, axis=1), np.std(mfccs, axis=1)


    def _split_tex_wnd(self, tex_wnd, chunk_sz):
        wnds = [ ]
        for i in range(0, len(tex_wnd) - 1, chunk_sz):
            wnds.append(
                tex_wnd[i:i+chunk_sz]
            )

        # last wnd is smaller
        if len(wnds[-1]) < chunk_sz:
            wnds[-1] = np.array(
                list(wnds[-1]) + (chunk_sz - len(wnds[-1])) * [0.0]
            )

        return wnds

    def fv(self):
        mean_centroid, std_centroid = self.centroid()
        mean_rolloff, std_rolloff = self.rolloff()
        mean_flux, std_flux = self.flux()
        mean_zc, std_zc = self.zero_crossings()
        mean_mfcc, std_mfcc = self.mfcc()
        low_energy = self.low_energy()

        return np.array([
            mean_centroid,
            mean_rolloff,
            mean_flux,
            mean_zc,
            *mean_mfcc,
            std_centroid,
            std_rolloff,
            std_flux,
            std_zc,
            *std_mfcc,
            low_energy,
        ])

