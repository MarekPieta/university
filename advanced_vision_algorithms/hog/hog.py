import numpy as np
import math

def hog(I):
    YY, XX, ZZ = I.shape
    SXY = np.zeros([YY,XX], np.int32)
    DIR = np.zeros([YY,XX], np.float32)
    I_i32 = np.int32(I)
    for jj in range(1,YY-1):
        for ii in range (1,XX-1):
            SXY_max = 0;
            SX_max = 0;
            SY_max = 0;
            for k in range(0,3):
                SX_k = I_i32[jj,ii-1,k] - I_i32[jj,ii+1,k]  # poziom
                SY_k = I_i32[jj-1,ii,k] - I_i32[jj+1,ii,k]  # pion
                SXY_k = np.sqrt(math.pow(SX_k,2) + math.pow(SY_k,2))
                if SXY_k > SXY_max:
                    SXY_max = SXY_k
                    SX_max = SX_k
                    SY_max = SY_k
            # Przypisanie koncowe
            SXY[jj,ii] = SXY_max
            DIR[jj,ii] = math.degrees(math.atan2(SY_max,SX_max))

    # Obliczenia histogramow
    cellSize = 8  # rozmiar komorki
    YY_cell= np.int32(YY/cellSize)
    XX_cell= np.int32(XX/cellSize)
    # Kontener na histogramy - zakladamy, ze jest 9 przedzialow
    hist = np.zeros([YY_cell,XX_cell,9],np.float32)
    # Iteracja po komorkach na obrazie
    for jj in range(0,YY_cell):
        for ii in range(0,XX_cell):
            # Wyciecie komorki
            M = SXY[jj*cellSize:(jj+1)*cellSize,ii*cellSize:(ii+1)*cellSize]
            T = DIR[jj*cellSize:(jj+1)*cellSize,ii*cellSize:(ii+1)*cellSize]
            M = M.flatten()
            T = T.flatten()

            # Obliczenie histogramu
            for k in range(0,cellSize*cellSize):
                m = M[k];
                t = T[k];
                # Usuniecie ujemnych kata (zalozenie katy w stopniach)
                if(t < 0):
                    t = t + 180
                # Wyliczenie przezdialu
                t0 = np.floor((t-10)/20 )*20 +10 # Przedzial ma rozmiar 20, srodek to 20
                # Przypadek szczegolny tj. t0 ujemny
                if (t0 < 0):
                    t0 = 170
                # Wyznaczenie indeksow przedzialu
                i0 = (t0-10)/20;
                i1 = i0+1;
                # Zawijanie
                if i1 == 9:
                    i1=0;
                # Obliczenie odleglosci do srodka przedzialu
                d = min(abs(t-t0), 180 -abs(t-t0))/20

                # Aktualizacja histogramu
                hist[jj,ii,int(i0)] = hist[jj,ii,int(i0)] + m*(1-d)
                hist[jj,ii,int(i1)] = hist[jj,ii,int(i1)] + m*(d)

    # Normalizacja w blokach
    e = math.pow(0.00001,2)
    F = []
    for jj in range(0,YY_cell-1):
        for ii in range(0,XX_cell-1):
            H0 = hist[jj,ii,:]
            H1 = hist[jj,ii+1,:]
            H2 = hist[jj+1,ii,:]
            H3 = hist[jj+1,ii+1,:]
            H = np.concatenate((H0, H1, H2, H3))
            n = np.linalg.norm(H)
            Hn = H/np.sqrt(math.pow(n,2)+e)
            F = np.concatenate((F,Hn))
    return F
