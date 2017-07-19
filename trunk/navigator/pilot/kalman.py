#!/usr/bin/env python3
import numpy as np
from numpy import dot, sum, tile, linalg
from numpy.linalg import inv


class Kalman():

    def __init__(self):
        dt = 0.08
        self.X = np.zeros(6,float)

        self.P = np.zeros((6,6),float)
        np.fill_diagonal(self.P,0.1)

        self.A = np.identity(6, float)
        self.A[0,3] = dt
        self.A[1,4] = dt
        self.A[2,5] = dt

        self.Q = np.identity(6, float)

        self.R = np.identity(3,float) #np.diag(np.empty(8).fill(0.01))

        self.H = np.zeros((3,6),float)
        np.fill_diagonal(self.H,1)


        #Y = np.zeros(6)

    def filter(self, x, y, z):
        Y = np.asarray((x, y, z))
        self.kf_predict()
        (X, IM, IS, LH) = self.kf_update(Y)
        return (X[0,0],X[1,0],X[2,0])
        

    def kf_predict(self):
        self.X = dot(self.A, self.X)
        self.P = dot(self.A, dot(self.P, self.A.T)) + self.Q


    def kf_update(self, Y):
        IM = dot(self.H, self.X)
        IS = self.R + dot(self.H, dot(self.P, self.H.T))
        K = dot(self.P, dot(self.H.T, inv(IS)))
        self.X = self.X + dot(K, (Y-IM))
        self.P = self.P - dot(K, dot(IS, K.T))
        #LH = self.gauss_pdf(Y, IM, IS)
        LH = None
        return (K,IM,IS,LH)


    def gauss_pdf(self, X, M, S):
        if M.shape()[1] == 1:
            DX = X - tile(M, X.shape()[1])
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
            self.P = exp(-E)
        elif X.shape()[1] == 1:
            DX = tile(X, M.shape()[1])- M
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
            self.P = exp(-E)
        else:
            DX = X-M
            E = 0.5 * dot(DX.T, dot(inv(S), DX))
            E = E + 0.5 * M.shape()[0] * log(2 * pi) + 0.5 * log(det(S))
            self.P = exp(-E)
        return (self.P[0],E[0]) 
