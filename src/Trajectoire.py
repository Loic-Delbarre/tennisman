import numpy as np
import const as cst
from scipy.integrate import solve_ivp
#pour minimaliser la charge de calcul repetitive 
# on va sortir de la fonction et les declarer en global les deux trois constantes variables
c=(cst.rho*np.pi*cst.d**2)/(8*cst.m)

def oderhs(t,y):
    p=np.array(y[:3],dtype=cst.dtype)
    v=np.array(y[3:6],dtype=cst.dtype)
    w=np.array(y[6:9],dtype=cst.dtype)
    normv=np.linalg.norm(v)
    if(normw :=np.linalg.norm(w)):
       cm=1/(2+(1.96*normv)/(normw*cst.d)) 
       Fm=(cm*c*normv**2)*np.cross(w/normw,v/normv) 
    else: 
       Fm=np.array([0,0,0],cst.dtype)
    Ft=(-1*cst.cd*c*normv**2)*(v/normv)
    Fd=np.array([0,0,cst.g])
    a=Fd+Ft+Fm
    alpha=np.zeros(3)
    return np.concatenate((v,a,alpha))

def  trajectoireFiletHorizontal(yInit,T,bouncing=True):
    tmp=np.arange(0,T,cst.precision)
    pos=solve_ivp(oderhs,(0,T),yInit,t_eval=tmp,events=evenement,rtol=cst.rtol,atol=cst.atol)
    #pos=method(oderhs,[0,T],yInit,events=evenement) 
    for i in range(pos.shape[1]):
        # si on n as pas encore passé le filet(la balle est du meme coté que la pos init)
        # si la posz de la balle est plus petite que le filet et que la balle descend
        # cela ne sert a rien , la balle ne passera pas le filet 
        if( pos[0][i]*pos[0][0]>0 and pos[5][i]>0 and pos[2][i]>cst.hf  ):
            return(0,0,0)
    #dans le cas d un deuxieme rebond il suffit de repartir de la derniere position et de redefinir la vitesse verticale comme multiplié par e 
    if( bouncing ):
        pos.y[5,-1]=pos.y[5,-1]*cst.e
        # pos shape donne la taile du tableau or le premier element contient la pos initale
        return trajectoireFiletHorizontal(pos.y[:,-1],T-(pos.y.shape[1]-1)*cst.precision,bouncing=False)
    return pos.y[:3,-1] 
def evenement(t,y):
    return y[2]
evenement.terminal=True


