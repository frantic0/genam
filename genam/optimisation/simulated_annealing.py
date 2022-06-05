from numpy.random import randn, rand
from math import exp

def simulated_annealing(objective, bounds, n_iterations, step_size, temperature, best = None):
    '''
        Stochastic global search optimization

        Maintains a single candidate solution, from which it takes steps of a random but constrained size in the search space. 

        If the new point is better than the current point, then the current point is replaced with the new point.

        If the new point is worse than the current candidate, it can still be accepted. The likelihood of accepting a solution worse than the current 
        is a function of the temperature of the search and how much worse the solution is than the current solution.

    '''
    if best == None:                                                                # if initial solution is not provided
        best = bounds[:, 0] + rand(len(bounds)) * ( bounds[:, 1] - bounds[:, 0] )   # sample a random initial point (uniform distribution)

    best_eval = objective(best)                                                     # evaluate the initial point   
    current, current_eval = best, best_eval                                         # keep current working solution
    scores = list()
    for i in range(n_iterations):
        candidate = current + randn(len(bounds)) * step_size                        # take a step, 'standard normal' distribution  99 percent of all steps taken will be within a distance of (step_size * 3) of a given point, e.g. three standard deviations.
        
        candidate_eval = objective(candidate)                                       # evaluate candidate point
        scores.append(best_eval)

        if candidate_eval < best_eval:                                              # check for new best solution
            best, best_eval = candidate, candidate_eval                             # store new best point
            
            d = candidate_eval - current_eval                                       # difference between candidate and current point evaluation
            
            metropolis = exp( -d / (temperature / float(i + 1)) )                   # calculate likelihood of accepting a solution with worse performance (metropolis acceptance criterion)
            
            if d < 0 or rand() < metropolis:
                current, current_eval = candidate, candidate_eval
	
    return [ best, best_eval, scores ]