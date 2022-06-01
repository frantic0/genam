
# Single objective GA with real, integer, and mixed form of variables

import numpy as np
import sys                    # For writing on the console
import time                   # for execute sleep function (for mwini case)
import matplotlib.pyplot as plt
import os.path

class geneticalgorithm():

################################################################
########### INITIALIZE PARAMETERS & VARIABLES
################################################################
    def __init__(self, function, dimension, variable_type='binary', \
                 variable_boundaries=None,\
                 variable_type_mixed=None, \
                 algorithm_parameters={'max_num_iteration': 50,\
                                       'population_size':20,\
                                       'mutation_probability':0.1,\
                                       'elit_ratio': 0.01,\
                                       'crossover_probability': 0.5,\
                                       'parents_portion': 0.3,\
                                       'crossover_type':'uniform',\
                                       'max_iteration_without_improv':None},\
                     convergence_curve=False,\
                         progress_bar=False):

        '''
        Here parent portion is the part of current gen population which is selected randomly 
        that moves to next generation
        rest other are developed through cross-over and mutation 

        Max: no of iteration selected based on variable size and population

        assert command is inserted to check the probability and some variable 
        Prompt error if assert fails

        best_funcition and best_variable are the desired values 
        '''
        
        # name the module 
        self.__name__=geneticalgorithm
       
        # input function
        self.f=function
        
        #dimension
        self.dim=int(dimension)
        
        # input variable type
        if variable_type_mixed is None: # if not mized type

            if variable_type=='real': 
                self.var_type=np.array([['real']]*self.dim)
                self.var_bound=variable_boundaries
            elif variable_type=='int':
                self.var_type=np.array([['int']]*self.dim)
                self.var_bound=variable_boundaries   
            elif variable_type=='binary': # for binary consider integer but boundary will be in 0,1
                self.var_type=np.array([['int']]*self.dim)
                self.var_bound= np.array([[0,1]]*self.dim)

        else:                           # if mixed type
            # check for the lenght of mixed form of variables: should be same as dimension
            assert (len(variable_type_mixed) == self.dim), \
                    "\n variable_type must have a length equal dimension."         

            self.var_type=variable_type_mixed
            self.var_bound=variable_boundaries
           
                       
        # Plot of convergence: 
        if convergence_curve==True:
            self.convergence_curve=True
        else:
            self.convergence_curve=False
     
        #progress_bar : to show GA running status
        if progress_bar==True:
            self.progress_bar=True
        else:
            self.progress_bar=False
     
        # input algorithm's parameters    
        self.param=algorithm_parameters

        # population size
        self.pop_s=int(self.param['population_size'])
          
        # parent population as portion of total pop
        self.par_s=int(self.param['parents_portion']*self.pop_s)
        trl=self.pop_s-self.par_s
        if trl % 2 != 0:
            self.par_s+=1
               
        # mutation probability
        self.prob_mut=self.param['mutation_probability']
        assert (self.prob_mut<=1 and self.prob_mut>=0), \
        "mutation_probability must be in range [0,1]"
        
        # xover type : default is uniform
        self.c_type=self.param['crossover_type']
       
        # xover probability
        self.prob_cross=self.param['crossover_probability']
        assert (self.prob_cross<=1 and self.prob_cross>=0), \
        "xover_probability must be in range [0,1]"
        
        # elit ratio( to determine elits : i.e. chromosomes which are copied as it is to next gen) 
        assert (self.param['elit_ratio']<=1 and self.param['elit_ratio']>=0),\
                           "elit_ratio must be in range [0,1]"                
        
        trl=self.pop_s*self.param['elit_ratio']
        if trl<1 and self.param['elit_ratio']>0:
            self.num_elit=1
        else:
            self.num_elit=int(trl)
            
        # for no of iterations (generations: if pop size is more then generations are less)
        if self.param['max_num_iteration']==None:
            self.iterate=0
            for i in range (0,self.dim):
                if self.var_type[i]=='int':
                    self.iterate+=(self.var_bound[i][1]-self.var_bound[i][0])*self.dim*(100/self.pop_s)
                else:
                    self.iterate+=(self.var_bound[i][1]-self.var_bound[i][0])*50*(100/self.pop_s)
            self.iterate=int(self.iterate)
            if (self.iterate*self.pop_s)>10000000:
                self.iterate=10000000/self.pop_s
        else:
            self.iterate=int(self.param['max_num_iteration'])
        
        
        # if there is no improvement in the function value for this number
        # (generally it is taken as greater than total generations)
        self.stop_mniwi=False
        if self.param['max_iteration_without_improv']==None:
            self.mniwi=self.iterate+1
        else: 
            self.mniwi=int(self.param['max_iteration_without_improv'])


        # population store (initialize)
        self.pop_store = np.array([np.zeros(self.dim)]*self.pop_s*(self.iterate+1))

##########################################################################
############# EXECUTE GA ALGORITHM #######################################
########################################################################## 
    def run(self):
        
        ###############################################
        ################### SAVE FILES ###############
        ##############################################

        # To save the variables in a file 
        save_path = "/SAN/uclic/ammdgop/data"
        file_name_1 = "final_results.out"
        complete_Name = os.path.join(save_path, file_name_1)
        file_object = open(complete_Name,"a+")
        #file_object = open("final_results.out","a+")

        # save file at every generations
        file_object.seek(0)
        file_object.write("\n")

        # GENERATION COUNTER
        t=1   

        # Append values
        dict1 = {"Generations": t-1, "Population_size":self.pop_s, "Lens_size (rxc)": self.dim, "count_id_lb":((t-1)*self.pop_s)+1 ,"count_id_ub":(t*self.pop_s)}
        str1 = repr(dict1)
        file_object.write("dict1 = " + str1 + "\n")
        file_object.write("\n")
        file_object.write("################################################")
        file_object.write("\n")
        

        ##########################################################
        ######### Initialize Population (real or integer form)
        ##########################################################
        self.integers=np.where(self.var_type=='int')
        self.reals=np.where(self.var_type=='real')
                
        # dummy variable for each generation (pop size is pop_s*dim+1: +1 is to store objective fun value
        pop=np.array([np.zeros(self.dim+1)]*self.pop_s)
        solo=np.zeros(self.dim+1)
        var=np.zeros(self.dim)       

        solo_1 = np.zeros(self.dim+2)

        # Initialize population (randomly between bounds)
        for p in range(0,self.pop_s): 
            for i in self.integers[0]:
                var[i]=np.random.randint(self.var_bound[i][0],\
                        self.var_bound[i][1]+1)  
                solo[i]=var[i].copy()
            for i in self.reals[0]:
                var[i]=self.var_bound[i][0]+np.random.random()*\
                (self.var_bound[i][1]-self.var_bound[i][0])    
                solo[i]=var[i].copy()

            # store the objective function value in pop as dim+1
            obj=self.sim(var)            
            solo[self.dim]=obj
            pop[p]=solo.copy()


            ###############################################
            ################### SAVE FILES ###############
            ##############################################
            
            solo_1[0:self.dim+1] = solo.copy()
            if obj < 0:
               solo_1[self.dim] = -1*obj
            solo_1[self.dim+1] = p+1
            file_object.write(repr(solo_1[:]).replace("\n", " "))
            file_object.write("\n")
            file_object.seek(0)
            file_object.write("\n")
        file_object.write("\n") 
       

        # Report
        self.report=[]
        self.test_obj=obj
        self.best_variable=var.copy()
        self.best_function=obj

        # store for every generation
        self.pop_store[((t-1)*self.pop_s):(t*self.pop_s),0:self.dim] = pop[:,0:self.dim]
           
        #############################################################  
        ############### GENERATION START ######################
        #############################################################              
       
        counter=0
        while t<=self.iterate:
            
            if self.progress_bar==True:
                self.progress(t,self.iterate,status="GA is running...")
            
            #Sort: in ascending order for minimum or maximum 
            # and select the first one as best objective function
            pop = pop[pop[:,self.dim].argsort()]
        

            # update the desired best fun and variable values
            if pop[0,self.dim]<self.best_function:
                counter=0
                self.best_function=pop[0,self.dim].copy()
                self.best_variable=pop[0,: self.dim].copy()
            else:
                counter+=1   #update this counter if no best function value is obtained than previous generation

        
            # Report (apend report: add the best function value in end to show convergence)
            self.report.append(pop[0,self.dim])
             
            # Normalizing objective function (norm to calculate probability)   
            normobj=np.zeros(self.pop_s)
            
            minobj=pop[0,self.dim]
            if minobj<0: # for maximization
                normobj=pop[:,self.dim]+abs(minobj)
                
            else:
                normobj=pop[:,self.dim].copy()
    
            maxnorm=np.amax(normobj)
            normobj=maxnorm-normobj+1

            # Calculate probability (for parent portion to next generation)
            sum_normobj=np.sum(normobj)
            prob=np.zeros(self.pop_s)
            prob=normobj/sum_normobj
            cumprob=np.cumsum(prob)
  
            # Select parents portion
            par=np.array([np.zeros(self.dim+1)]*self.par_s)
            
            # no of elits (the best elit variables proceed to next gen)
            for k in range(0,self.num_elit):
                par[k]=pop[k].copy()
            for k in range(self.num_elit,self.par_s):
                index=np.searchsorted(cumprob,np.random.random())
                par[k]=pop[index].copy()
                
            # the portion of current pop (parent pop portion which will undergo varibality)
            ef_par_list=np.array([False]*self.par_s)
            par_count=0
            while par_count==0:
                for k in range(0,self.par_s):
                    if np.random.random()<=self.prob_cross:
                        ef_par_list[k]=True
                        par_count+=1  
            ef_par=par[ef_par_list].copy()

            # Generation counter update
            t+=1
        
            # save file at every generations
            file_object.seek(0)
            file_object.write("\n")

            # Append values
            dict1 = {"Generations": t-1, "Population_size":self.pop_s, "Lens_size (rxc)": self.dim, "count_id_lb":((t-1)*self.pop_s)+1 ,"count_id_ub":(t*self.pop_s)-self.par_s}
            str1 = repr(dict1)
            file_object.write("dict1 = " + str1 + "\n")
            file_object.write("\n")
            file_object.write("################################################")
            file_object.write("\n")

    
            #############################################################  
            ############### Next generation update ######################
            #############################################################    
            pop=np.array([np.zeros(self.dim+1)]*self.pop_s)
            
            # parent portion carried from old generation
            for k in range(0,self.par_s):
                pop[k]=par[k].copy()


            # write the individuals into file before variability
            solo_2 = np.zeros(self.dim+2)
            pop_print=np.array([np.zeros(self.dim+2)]*self.par_s)

            for p1 in range(0,self.par_s):
                for p2 in range(0,self.dim+1):
                    solo_2[p2] = pop[p1,p2]
                solo_2[self.dim+1] = 0
                if solo_2[self.dim] < 0:
                   solo_2[self.dim] = -1*solo_2[self.dim]
                pop_print[p1] = solo_2.copy()
            
            for p3 in range(0,self.par_s):
                file_object.seek(0)
                file_object.write(repr(pop_print[p3,:]).replace("\n", " "))
                file_object.write("\n")
                file_object.seek(0) 
                file_object.write("\n")

            solo_3 = np.zeros(self.dim+2)

            # Variability (x-over and mutation)              
            for k in range(self.par_s, self.pop_s, 2):
                r1=np.random.randint(0,par_count)
                r2=np.random.randint(0,par_count)
                pvar1=ef_par[r1,: self.dim].copy()
                pvar2=ef_par[r2,: self.dim].copy()
                
                while flag_1 == 2:

                    ch=self.cross(pvar1,pvar2,self.c_type)
                    ch1=ch[0].copy()
                    ch2=ch[1].copy()
                    
                    ch1=self.mut(ch1)
                    ch2=self.mutmidle(ch2,pvar1,pvar2)

                    # compare with previous generations individuals
                    for p4 in range(0,self.pop_s*(self.iterate+1)):

                        comp_1 = np.array_equal(ch1[ch1.argsort()],self.pop_store[p4,self.pop_store[p4].argsort()])
                        comp_2 = np.array_equal(ch2[ch2.argsort()],self.pop_store[p4,self.pop_store[p4].argsort()])

                        if comp_1 or comp_2:
                            flag_1 = 2
                            break
                        else:
                            flag_1 = 1                

                solo[: self.dim]=ch1.copy()
                obj=self.sim(ch1)
                solo[self.dim]=obj
                pop[k]=solo.copy()     

                solo_3[0:self.dim+1] = solo.copy()
                if obj < 0:
                   solo_3[self.dim] = -1*obj
                solo_3[self.dim+1] = ((t-1)*self.pop_s) + 1 + k - self.par_s

                file_object.write(repr(solo_3[:]).replace("\n", " "))
                file_object.write("\n")
                file_object.seek(0)
                file_object.write("\n")
                

                solo[: self.dim]=ch2.copy()
                obj=self.sim(ch2)      
                solo[self.dim]=obj
                pop[k+1]=solo.copy()

                solo_3[0:self.dim+1] = solo.copy()
                if obj < 0:
                   solo_3[self.dim] = -1*obj
                solo_3[self.dim+1] = ((t-1)*self.pop_s) + 1 + 1 + k - self.par_s

                file_object.write(repr(solo_3[:]).replace("\n", " "))
                file_object.write("\n")
                file_object.seek(0)
                file_object.write("\n")

            file_object.write("\n")


            # store for every generation
            self.pop_store[((t-1)*self.pop_s):(t*self.pop_s),0:self.dim] = pop[:,0:self.dim]
       

            #############################################################     
            ########## Increase GENERATION NUMBER 
            #############################################################  
            #if the first pop is less than equal to best value
            #then terminate the while loop after checking for total generations +1 iterations
            ##################################################################  

            if counter > self.mniwi:
                pop = pop[pop[:,self.dim].argsort()]
                if pop[0,self.dim]<=self.best_function: 
                    t=self.iterate
                    if self.progress_bar==True:
                        self.progress(t,self.iterate,status="GA is running...")
                    time.sleep(2)
                    t+=1
                    self.stop_mniwi=True

        ##############################################################
        ############### END GENERATIONS ###########
        #############################################################
            
        #Sort (after while loop sort objective function)
        pop = pop[pop[:,self.dim].argsort()]
        self.final_pop = pop.copy()
        
        # update the desirable variables
        if pop[0,self.dim]<self.best_function:        
            self.best_function=pop[0,self.dim].copy()
            self.best_variable=pop[0,: self.dim].copy()
        
        # Report
        self.report.append(pop[0,self.dim])
        
        # displaye the final output
        self.output_dict={'variable': self.best_variable, 'function':\
                          self.best_function}
        
        # End results after total GENERATIONS
        if self.progress_bar==True:
            show=' '*100
            sys.stdout.write('\r%s' % (show))

        
        print("############################################")
        sys.stdout.write('\r Optimized variable:\n %s' % (self.best_variable))
        sys.stdout.write('\n\n Optimized objective fn:\n %s\n' % (self.best_function))
        sys.stdout.flush() 

        # plot the convergence curve
        re=np.array(self.report)
        if self.convergence_curve==True:
            plt.plot(re)
            plt.xlabel('Iteration')
            plt.ylabel('Objective function')
            plt.title('Genetic Algorithm')
            plt.show()
        
        # if no improvement met: GA is terminated
        if self.stop_mniwi==True:
            sys.stdout.write('\nWarning: GA is terminated due to the'+\
                             ' maximum number of iterations without improvement was met!')

        file_object.close()
##############################################################################
##### Dependent functions (croosover, mutations, objective function calculation)         
##############################################################################         
    def cross(self,x,y,c_type):
         
        ofs1=x.copy()
        ofs2=y.copy()
        
        if c_type=='one_point':
            ran=np.random.randint(0,self.dim)
            for i in range(0,ran):
                ofs1[i]=y[i].copy()
                ofs2[i]=x[i].copy()
  
        if c_type=='two_point':
                
            ran1=np.random.randint(0,self.dim)
            ran2=np.random.randint(ran1,self.dim)
                
            for i in range(ran1,ran2):
                ofs1[i]=y[i].copy()
                ofs2[i]=x[i].copy()
            
        if c_type=='uniform':
                
            for i in range(0, self.dim):
                ran=np.random.random()
                if ran <0.5:
                    ofs1[i]=y[i].copy()
                    ofs2[i]=x[i].copy() 
                   
        return np.array([ofs1,ofs2])

###############################################################################  
    def mut(self,x):
        
        for i in self.integers[0]:
            ran=np.random.random()
            if ran < self.prob_mut:
                
                x[i]=np.random.randint(self.var_bound[i][0],\
                 self.var_bound[i][1]+1) 
                    
        

        for i in self.reals[0]:                
            ran=np.random.random()
            if ran < self.prob_mut:   

               x[i]=self.var_bound[i][0]+np.random.random()*\
                (self.var_bound[i][1]-self.var_bound[i][0])    
            
        return x

###############################################################################
    def mutmidle(self, x, p1, p2):
        for i in self.integers[0]:
            ran=np.random.random()
            if ran < self.prob_mut:
                if p1[i]<p2[i]:
                    x[i]=np.random.randint(p1[i],p2[i])
                elif p1[i]>p2[i]:
                    x[i]=np.random.randint(p2[i],p1[i])
                else:
                    x[i]=np.random.randint(self.var_bound[i][0],\
                 self.var_bound[i][1]+1)
                        
        for i in self.reals[0]:                
            ran=np.random.random()
            if ran < self.prob_mut:   
                if p1[i]<p2[i]:
                    x[i]=p1[i]+np.random.random()*(p2[i]-p1[i])  
                elif p1[i]>p2[i]:
                    x[i]=p2[i]+np.random.random()*(p1[i]-p2[i])
                else:
                    x[i]=self.var_bound[i][0]+np.random.random()*\
                (self.var_bound[i][1]-self.var_bound[i][0]) 
        return x
###############################################################################     
    def sim(self,X):
        self.temp=X.copy()
        obj= self.f(self.temp) 
        return obj

###############################################################################
    def progress(self, count, total, status=''):
        bar_len = 50
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '|' * filled_len + '_' * (bar_len - filled_len)

        sys.stdout.write('\r%s %s%s %s' % (bar, percents, '%', status))
        sys.stdout.flush()     
###############################################################################            
###############################################################################
            
             
            
            