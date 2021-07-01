import numpy as np

from anabel.abstract import ModelComponent
import anabel.backend as anp

class Node(ModelComponent):
    def __init__(self, model, name: str, ndf, xyz, mass=None):
        if mass is None: mass=0.0

        self.xyz = self.coords = np.array([xi for xi in xyz if xi is not None])

        self._tag = name if isinstance(name, int) else None
        self.xyz0 = self.xyz # coordinates in base configuration (unstrained, not necessarily unstressed).
        self.xyzi = self.xyz # coordinates in reference configuration.  

        self.x0: float = xyz[0] # x-coordinate in base configuration (unstrained, not necessarily unstressed).  
        self.y0: float = xyz[1] # y-coordinate in base configuration (unstrained, not necessarily unstressed).  
        # z-coordinate in base configuration (unstrained, not necessarily unstressed).  
        self.z0: float = xyz[2] if len(xyz) > 2 else None

        # Attributes for nonlinear analysis
        # self.xi: float = x # x-coordinate in reference configuration.  
        # self.yi: float = y # y-coordinate in reference configuration.  
        # self.zi: float = z # z-coordinate in reference configuration.  
        
        self.x: float = xyz[0]
        self.y: float = xyz[1]
        self.z: float = xyz[2] if len(xyz) > 2 else None

        
        self.rxns = [0]*ndf
        self.model = self._domain = model
        self.mass = mass
        self.elems = []

        self.p = {dof:0.0 for dof in model.ddof}

    @property
    def tag(self):
        if self._tag is not None:
            return self._tag
        else:
            return self.domain.nodes.index(self)

    def __repr__(self):
        return 'nd-{}'.format(self.tag)

    def p_vector(self):
        return np.array(list(self.p.values()))

        
    @property
    def dofs(self):
        """Nodal DOF array"""
        # if self.model.DOF == None: self.model.numDOF()
        idx = self.model.nodes.index(self)
        return np.asarray(self.model.DOF[idx],dtype=int)
    
    def dump_opensees(self):
        coords = " ".join(f"{x:10.8}" for x in self.xyz)
        return f"node {self.tag} {coords}"

