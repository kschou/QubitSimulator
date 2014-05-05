import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import time

##############################################
# Define general experiment class
##############################################

class Experiment: 
    
    def __init__(self, H_ti):
        self.H_ti = H_ti # time independent Hamiltonian
        
        self.c_ops = []
        self.outputs = []
        
    def define_time_dependence(self, time_dependence):
        '''
            Set up for time dependent components of experiment.

            Inputs: 
               - <time_dependence>: list describing the time dependent components of the requested experiment
                 Format: [[(H_td, td_coeff, args), (start_time, stop_time, num_pts)], [H_td2, (start_time, stop_time, num_pts)]...]

                <H_td> represents the Qobj with a time dependent amplitude, specified by <td_coeff>.
                <td_coeff> is a callback function with signature H_td(t, args), where <args> is specified as the next element.

                # TODO: this should arange the times so that overlapping time dependent H's are combined.
        '''
        
        self._H_td = []
        for [H_td_params, (start_time, stop_time, num_pts)] in time_dependence:
            
            if H_td_params is None: # no time dependent: unitary evolution
                H_td_params = (None, None, None)
            H_td, td_coeff, args = H_td_params
            self._H_td.append([H_td, td_coeff, args, np.linspace(start_time, stop_time, num_pts)])
        
        
    
    def setup_experiment(self, initial_state, c_ops=[], expects=[]):
        '''
            Defines parameters for master equation simulation:
            - <initial_state>: the initial quantum state, either as a ket or as a density matrix

            - <c_ops>: collapse operators, if none are requested, then input []

            - <expects>: list of expectation operators for the FINAL state 
            
        '''
        
        self.initial_state = initial_state
        self.c_ops = c_ops
        self.expects = expects
    
    def simulate(self):
        
        # setup time-dependent Hamiltonians sequentially
        psi0 = self.initial_state
        
        self.sim_states = []
        self.sim_tlist = []
        
        for [H_td, td_coeff, args, tlist] in self._H_td:
            if H_td is not None:
                H = [self.H_ti, [H_td, td_coeff]]
            else:
                H = self.H_ti
                args = None
                
            output = qt.mesolve(H, psi0, tlist, self.c_ops, [], args=args)
            
            # append all but the last step--will the initial step in the next simulation
            self.sim_states.extend(output.states[:-1])
            self.sim_tlist.extend(tlist[:-1])
            
            psi0 = output.states[-1]

        self.sim_states.extend([output.states[-1]])
        self.sim_tlist.extend([tlist[-1]])
            
        self.sim_states = np.array(self.sim_states)
        self.sim_tlist = np.array(self.sim_tlist)
        
    def calculate_expects(self):
        '''
        	requires: self.expects

            format: [[expectation for operator 1 for all times], [expectation for operator 1 for all times], ...]

            
        '''
        
        self.sim_expects = []
        for i, oper in enumerate(self.expects):
            expects = qt.expect(oper, self.sim_states)
            self.sim_expects.append(expects)

            
        self.sim_expects = np.array(self.sim_expects)
            
