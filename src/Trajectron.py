import time
import numpy as np
import const as cst
#from scipy.integrate import solve_ivp
#pour minimaliser la charge de calcul repetitive 
# on va sortir de la fonction et les declarer en global les deux trois constantes variables
c=(cst.rho*np.pi*cst.d**2)/(8*cst.m)
#normalement oderhs retourne dy correctement
def oderhs(t,y):
    #    p=np.array(y[:3],dtype=cst.dtype)
    v = np.array(y[3:6], dtype=cst.dtype)
    w=np.array(y[6:9],dtype=cst.dtype)
    normv=np.linalg.norm(v)
    if(normw :=np.linalg.norm(w)):
        cm=1/(2+(1.96*normv)/(normw*cst.d)) 
        Fm=(cm*c*normv**2)*np.cross(w/normw,v/normv) 
    else: 
        Fm=0.0
    Ft=(-1*cst.cd*c*normv**2)*(v/normv)
    Fd=np.array([0,0,cst.g])
    a=Fd+Ft+Fm
    alpha=np.zeros(3)
    return np.concatenate((v,a,alpha))

def euler(f,t_span,y,events = None ):
    t=t_span[0]
    step=int(t_span[1]/cst.precision)
    # on alloue un tableau vide que l on remplira au fur et a mesure
    yt=np.empty((step+1,9),dtype=cst.dtype) 
    yt[0][:]=y
    #yt=np.array([y],dtype=cst.dtype)
    start_time= time.time() # definit le temps initial
    for i in range(step):
        dy=f(t,y)
        y=y+dy*cst.precision
        t=t+cst.precision 
        if events(t,y):
            print(i)
            yt=np.resize(yt,(i+1,9))# on recupere uniquement la partie interessante du tableau
            break
        yt[i+1][:]=y
        #yt=np.append(yt,[y],axis=0)
    print(time.time()-start_time) # affiche le temps d execution de la methode
    return yt 
def  trajectoireFiletHorizontal(yInit,T,bouncing=True):
    print(cst.precision)
    pos=euler(oderhs,[0,T],yInit,events=evenement) 
    print("end")
    for i in range(pos.shape[0]):
        # si on n as pas encore passé le filet(la balle est du meme coté que la pos init)
        # et si la posz de la balle est plus petite que le filet et que la balle descend
        # cela ne sert a rien , la balle ne passera pas le filet 
        if(pos[i][0]*pos[0][0]<0 and pos[i][5]>0 and pos[i][2]>cst.hf  ):
            return(0,0,0)
        #dans le cas d un deuxieme rebond il suffit de repartir de la derniere position et de redefinir la vitesse verticale comme multiplié par e 
    if bouncing:
        pos[-1][5]=pos[-1][5]*cst.e
        #pos shape donne la taile du tableau or le premier element contient la pos initale donc on a eu shape-1 tour de boucle
        return trajectoireFiletHorizontal(pos[-1][:],T-(pos.shape[0]-1)*cst.precision,bouncing=False)
    return tuple(pos[-1][:3]) 
def evenement(t,y):
    return 0>y[2]
evenement.terminal=True
#ytest=np.array([-1.189e+01,  0.000e+00,  2.000e+00 , 5.000e+01,  1.000e+00 , 0.000e+00, 3.000e-03 , 1.500e-03,  0.000e+00],dtype=cst.dtype)            
#a=trajectoireFiletHorizontal(ytest,0.8)     
#print(a) # la premiere valeur doit etre +- = a 16.678
